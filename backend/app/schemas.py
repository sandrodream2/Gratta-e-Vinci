"""Schemi Pydantic per le richieste e le risposte dell'API."""

from pydantic import BaseModel, Field


class GameOut(BaseModel):
    id: int
    name: str
    price: float
    odds_win: float | None
    odds_win_label: str | None
    odds_top: float | None
    odds_top_label: str | None
    top_prize: float | None
    top_prize_label: str | None
    active: bool
    source_url: str
    source_label: str
    notes: str | None


class PosRow(BaseModel):
    name: str
    city: str
    region: str
    tickets_sold: int
    wins_recorded: int
    wins_per_1000: float
    data_note: str


class WhereWinsResponse(BaseModel):
    disclaimer: str
    simulated_data: bool
    rows: list[PosRow]


class StatsOverview(BaseModel):
    games_count: int
    avg_odds_win: float | None
    avg_odds_win_label: str | None
    best_odds_win_label: str | None
    official_average_label: str
    payout_max_percent: int


class VerifySerialRequest(BaseModel):
    serial: str = Field(..., description="Numero di serie digitato dall'utente")


class VerifyScanRequest(BaseModel):
    code: str = Field(..., description="Codice letto dallo scanner (barcode/QR)")
    code_type: str = Field("unknown", description="Tipo di codice rilevato (QR_CODE, CODE_128, ...)")


class VerifyResponse(BaseModel):
    simulated: bool
    valid: bool
    status: str
    message: str
    warning: str
    reasons: list[str] = []


class MetaResponse(BaseModel):
    app_name: str
    disclaimer_banner: str
    disclaimer_stats: str
    disclaimer_verify: str
    no_lucky_numbers: str
    official_average_label: str
    payout_max_percent: int
    links: dict[str, str]
    data_note: str
