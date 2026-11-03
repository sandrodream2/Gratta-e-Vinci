"""Endpoint statistici (NON predittivi): panoramica e 'dove si vince di più'."""

from fastapi import APIRouter

from ..config import (
    DISCLAIMER_STATS,
    PAYOUT_MASSIMO_PERCENT,
    PROBABILITA_MEDIA_ADM,
)
from ..db import get_conn
from ..schemas import PosRow, StatsOverview, WhereWinsResponse
from ..utils import format_number_it, format_odds

router = APIRouter()


@router.get("/overview", response_model=StatsOverview)
def overview():
    conn = get_conn()
    (games_count,) = conn.execute(
        "SELECT COUNT(*) FROM games WHERE active = 1"
    ).fetchone()
    (avg_odds,) = conn.execute(
        "SELECT AVG(odds_win) FROM games WHERE active = 1 AND odds_win IS NOT NULL"
    ).fetchone()
    (best_odds,) = conn.execute(
        "SELECT MIN(odds_win) FROM games WHERE active = 1 AND odds_win IS NOT NULL"
    ).fetchone()
    return StatsOverview(
        games_count=games_count,
        avg_odds_win=avg_odds,
        avg_odds_win_label=format_odds(avg_odds),
        best_odds_win_label=format_odds(best_odds),
        official_average_label=f"1 su {format_number_it(PROBABILITA_MEDIA_ADM)}",
        payout_max_percent=PAYOUT_MASSIMO_PERCENT,
    )


@router.get("/where-wins", response_model=WhereWinsResponse)
def where_wins(limit: int = 10):
    """Punti vendita con più vincite registrate (dati aggregati di ESEMPIO).

    Restituisce sempre un disclaimer: è correlazione statistica, non predizione.
    """
    if limit < 1 or limit > 100:
        limit = 10
    rows = get_conn().execute(
        """
        SELECT name, city, region, tickets_sold, wins_recorded, data_note
        FROM points_of_sale
        ORDER BY wins_recorded DESC, tickets_sold DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    pos = [
        PosRow(
            name=r["name"],
            city=r["city"],
            region=r["region"],
            tickets_sold=r["tickets_sold"],
            wins_recorded=r["wins_recorded"],
            wins_per_1000=round(r["wins_recorded"] / r["tickets_sold"] * 1000, 2),
            data_note=r["data_note"],
        )
        for r in rows
    ]
    return WhereWinsResponse(disclaimer=DISCLAIMER_STATS, simulated_data=True, rows=pos)
