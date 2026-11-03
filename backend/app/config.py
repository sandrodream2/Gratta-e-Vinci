"""Costanti dell'applicazione: avvertenze di trasparenza e link ufficiali."""

# Riesportate da data_games (fonte: note ufficiali ADM)
from .data_games import PAYOUT_MASSIMO_PERCENT, PROBABILITA_MEDIA_ADM  # noqa: F401

DISCLAIMER_BANNER = (
    "Le probabilità sono casuali e uguali ovunque. "
    "Nessuna app può prevedere se un biglietto è vincente prima di grattarlo."
)

DISCLAIMER_STATS = (
    "Questi dati sono aggregati di esempio: più biglietti venduti = più probabilità "
    "che escano premi. Si tratta di correlazione statistica, NON di predizione. "
    "La distribuzione dei biglietti vincenti è casuale e identica in ogni punto vendita."
)

DISCLAIMER_VERIFY = (
    "La verifica è solo formale (controllo del formato) o simulata: "
    "non esistono liste pubbliche di numeri di serie o lotti vincenti. "
    "Per l'esito certo, gratta il biglietto e verifica con l'app ufficiale My Lotteries."
)

NO_LUCKY_NUMBERS = (
    "È impossibile sapere quali lotti o quali numeri di serie sono vincenti prima di grattare: "
    "l'esito di ogni biglietto è predeterminato e nascosto prima della vendita (regolamento ADM)."
)

LINKS = {
    "adm_lotterie_istananee": "https://www.adm.gov.it/portale/monopoli/giochi/lotterie/lotterie_istananee",
    "adm_note_probabilita": "https://www.adm.gov.it/portale/monopoli/giochi/lotterie/lotterie_istananee/lot_ist_note",
    "concessionario_probabilita": "https://www.grattaevinci.com/probabilita-di-vincita",
    "mylotteries_app": "https://www.mylotteriesplay.it/",
    "gioco_responsabile": "https://www.adm.gov.it/portale/gioco-responsabile",
}

DATA_NOTE = (
    "Dati indicativi basati sulle schede ufficiali ADM e del concessionario. "
    "I giochi attivi cambiano nel tempo: verifica sempre la scheda ufficiale su adm.gov.it."
)
