"""Endpoint del catalogo dei giochi: elenco con filtri/ordinamento e dettaglio."""

from fastapi import APIRouter, HTTPException, Query

from ..db import get_conn
from ..schemas import GameOut
from ..utils import format_eur, format_number_it, format_odds

router = APIRouter()

SORTABLE = {
    "name": "name",
    "price": "price",
    "odds_win": "odds_win",
    "odds_top": "odds_top",
    "top_prize": "top_prize",
}


def _serialize(row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "odds_win": row["odds_win"],
        "odds_win_label": format_odds(row["odds_win"]),
        "odds_top": row["odds_top"],
        "odds_top_label": format_odds(row["odds_top"]),
        "top_prize": row["top_prize"],
        "top_prize_label": format_eur(row["top_prize"]),
        "active": bool(row["active"]),
        "source_url": row["source_url"],
        "source_label": row["source_label"],
        "notes": row["notes"],
    }


@router.get("", response_model=list[GameOut])
def list_games(
    q: str | None = Query(None, description="Ricerca testuale nel nome"),
    price_min: float | None = Query(None, ge=0),
    price_max: float | None = Query(None, ge=0),
    max_odds: float | None = Query(
        None, gt=0,
        description="Tieni solo i giochi con probabilità di vincita almeno '1 su N' (N più alto = più probabile)",
    ),
    active_only: bool = Query(True),
    sort: str = Query("price", description="price | odds_win | odds_top | top_prize | name"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    if sort not in SORTABLE:
        raise HTTPException(422, detail=f"Ordinamento non valido: {sort}. Valori: {sorted(SORTABLE)}")

    where, params = [], []
    if q:
        where.append("name LIKE ?")
        params.append(f"%{q}%")
    if price_min is not None:
        where.append("price >= ?")
        params.append(price_min)
    if price_max is not None:
        where.append("price <= ?")
        params.append(price_max)
    if max_odds is not None:
        where.append("(odds_win IS NULL OR odds_win <= ?)")
        params.append(max_odds)
    if active_only:
        where.append("active = 1")

    sql = "SELECT * FROM games"
    if where:
        sql += " WHERE " + " AND ".join(where)
    # I NULL vanno sempre in fondo, a prescindere dall'ordinamento
    sql += f" ORDER BY {SORTABLE[sort]} IS NULL, {SORTABLE[sort]} {order.upper()}, name ASC"

    rows = get_conn().execute(sql, params).fetchall()
    return [_serialize(r) for r in rows]


@router.get("/{game_id}", response_model=GameOut)
def get_game(game_id: int):
    row = get_conn().execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    if row is None:
        raise HTTPException(404, detail=f"Gioco con id {game_id} non trovato")
    return _serialize(row)


@router.get("/meta/prices", response_model=list[float])
def distinct_prices():
    """Prezzi distinti dei biglietti: utile per popolare i filtri del frontend."""
    rows = get_conn().execute(
        "SELECT DISTINCT price FROM games WHERE active = 1 ORDER BY price"
    ).fetchall()
    return [r["price"] for r in rows]
