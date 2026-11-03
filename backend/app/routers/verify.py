"""Verifica dei biglietti: numero di serie (controllo formale) e scanner (simulato).

IMPORTANTE: nessun endpoint può dire se un biglietto è vincente prima di grattarlo.
La verifica è solo formale (regex sul formato) o una simulazione.
"""

import hashlib
import re

from fastapi import APIRouter, HTTPException

from ..config import DISCLAIMER_VERIFY, NO_LUCKY_NUMBERS
from ..db import get_conn
from ..schemas import VerifyResponse, VerifyScanRequest, VerifySerialRequest

router = APIRouter()

# Numero di serie: 10-20 caratteri alfanumerici (maiuscoli dopo normalizzazione),
# con almeno 8 cifre. È un controllo FORMALE, non una verifica di vincita.
_SERIAL_RE = re.compile(r"^[A-Z0-9]{10,20}$")
_MIN_DIGITS = 8

# Codice scanner (barcode/QR): 8-64 caratteri stampabili.
_SCAN_MIN, _SCAN_MAX = 8, 64
_SCAN_RE = re.compile(r"^[\x20-\x7E]{8,64}$")


def _log(kind: str, code: str, valid: bool) -> None:
    """Salva solo l'hash SHA-256 del codice, mai il codice in chiaro."""
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
    get_conn().execute(
        "INSERT INTO verification_logs (kind, code_hash, valid) VALUES (?, ?, ?)",
        (kind, digest, 1 if valid else 0),
    )
    get_conn().commit()


def _normalize_serial(serial: str) -> str:
    return re.sub(r"[\s\-–.]", "", serial.strip().upper())


def _validate_serial(serial: str) -> list[str]:
    reasons = []
    if not serial:
        reasons.append("Il numero di serie è vuoto.")
        return reasons
    if not _SERIAL_RE.match(serial):
        reasons.append(
            "Formato non valido: sono ammesse solo lettere maiuscole e cifre "
            f"(10-20 caratteri, senza spazi o trattini)."
        )
    digits = sum(c.isdigit() for c in serial)
    if 0 < len(serial) and digits < _MIN_DIGITS:
        reasons.append(f"Il numero di serie deve contenere almeno {_MIN_DIGITS} cifre (trovate: {digits}).")
    return reasons


@router.post("/serial", response_model=VerifyResponse)
def verify_serial(payload: VerifySerialRequest):
    """Verifica FORMALE del numero di serie inserito manualmente.

    Non verifica vincite: restituisce solo se il formato è corretto.
    """
    normalized = _normalize_serial(payload.serial)
    reasons = _validate_serial(normalized)
    valid = not reasons
    _log("serial", normalized, valid)
    if not valid:
        raise HTTPException(
            status_code=422,
            detail={
                "reasons": reasons,
                "message": "Numero di serie non valido (controllo di formato fallito).",
            },
        )
    return VerifyResponse(
        simulated=True,
        valid=True,
        status="formato_valido",
        message=(
            "Numero di serie registrato (controllo di formato superato). "
            "Per l'esito certo, gratta il biglietto e verifica con l'app ufficiale My Lotteries."
        ),
        warning=f"{DISCLAIMER_VERIFY} {NO_LUCKY_NUMBERS}",
        reasons=[],
    )


@router.post("/scan", response_model=VerifyResponse)
def verify_scan(payload: VerifyScanRequest):
    """Riceve il codice letto dallo scanner (barcode/QR) e restituisce un esito SIMULATO.

    Nessun database ufficiale viene consultato: l'esito certo esiste solo dopo
    aver grattato il biglietto e averlo verificato con gli strumenti ufficiali.
    """
    code = payload.code.strip()
    reasons = []
    if not code:
        reasons.append("Nessun codice rilevato: OCR/scanner non riuscito.")
    elif not _SCAN_RE.match(code):
        reasons.append(
            f"Codice non leggibile: devono essere 8-{_SCAN_MAX} caratteri stampabili "
            f"(ricevuti {len(code)})."
        )
    valid = not reasons
    _log("scan", code, valid)
    if not valid:
        raise HTTPException(
            status_code=422,
            detail={
                "reasons": reasons,
                "message": "Scansione non riuscita: codice non valido o non leggibile.",
            },
        )
    return VerifyResponse(
        simulated=True,
        valid=True,
        status="biglietto_valido",
        message="Biglietto valido - verifica presso il punto vendita.",
        warning=(
            f"Esito di ESEMPIO (simulazione): nessun registro ufficiale è stato consultato. "
            f"{DISCLAIMER_VERIFY}"
        ),
        reasons=[],
    )
