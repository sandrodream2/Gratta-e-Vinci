"""Metadati dell'app: banner di trasparenza, disclaimer e link alle fonti ufficiali."""

from fastapi import APIRouter

from ..config import (
    DATA_NOTE,
    DISCLAIMER_BANNER,
    DISCLAIMER_STATS,
    DISCLAIMER_VERIFY,
    LINKS,
    NO_LUCKY_NUMBERS,
    PAYOUT_MASSIMO_PERCENT,
    PROBABILITA_MEDIA_ADM,
)
from ..schemas import MetaResponse
from ..utils import format_number_it

router = APIRouter()


@router.get("", response_model=MetaResponse)
def meta():
    return MetaResponse(
        app_name="GrattaData",
        disclaimer_banner=DISCLAIMER_BANNER,
        disclaimer_stats=DISCLAIMER_STATS,
        disclaimer_verify=DISCLAIMER_VERIFY,
        no_lucky_numbers=NO_LUCKY_NUMBERS,
        official_average_label=f"1 su {format_number_it(PROBABILITA_MEDIA_ADM)}",
        payout_max_percent=PAYOUT_MASSIMO_PERCENT,
        links=LINKS,
        data_note=DATA_NOTE,
    )
