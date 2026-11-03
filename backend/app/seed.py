"""Popolamento del database con i dati dei giochi e i punti vendita di esempio.

Uso:
    python -m app.seed              # crea lo schema e inserisce i dati (se vuoto)
    python -m app.seed --dump-sql   # stampa gli INSERT SQL su stdout (per database/seed.sql)
"""

import sqlite3
import sys

from .data_games import GAMES, POINTS_OF_SALE_SAMPLE
from .db import get_conn, init_db


def _sql_str(value: str | None) -> str:
    return "NULL" if value is None else "'" + value.replace("'", "''") + "'"


def seed_all(conn: sqlite3.Connection) -> None:
    """Inserisce giochi e punti vendita (esempio) nel database."""
    conn.executemany(
        """
        INSERT INTO games (name, price, odds_win, odds_top, top_prize, active,
                           source_url, source_label, notes)
        VALUES (:name, :price, :odds_win, :odds_top, :top_prize, 1,
                :source_url, :source_label, :notes)
        """,
        GAMES,
    )
    conn.executemany(
        """
        INSERT INTO points_of_sale (name, city, region, tickets_sold, wins_recorded, data_note)
        VALUES (:name, :city, :region, :tickets_sold, :wins_recorded,
                'Dati aggregati di esempio (simulati) - non dati reali')
        """,
        POINTS_OF_SALE_SAMPLE,
    )
    conn.commit()


def dump_sql() -> str:
    """Genera gli INSERT SQL equivalentes (usati per database/seed.sql)."""
    lines = ["-- GrattaData - dati iniziali (generati da backend/app/data_games.py)"]
    lines.append("-- Eseguire dopo schema.sql:  sqlite3 grattadata.db < database/seed.sql")
    lines.append("")
    for g in GAMES:
        lines.append(
            "INSERT INTO games (name, price, odds_win, odds_top, top_prize, active, source_url, source_label, notes) "
            "VALUES ({}, {}, {}, {}, {}, 1, {}, {}, {});".format(
                _sql_str(g["name"]),
                g["price"],
                "NULL" if g["odds_win"] is None else repr(g["odds_win"]),
                "NULL" if g["odds_top"] is None else repr(g["odds_top"]),
                "NULL" if g["top_prize"] is None else repr(g["top_prize"]),
                _sql_str(g["source_url"]),
                _sql_str(g["source_label"]),
                _sql_str(g["notes"]),
            )
        )
    lines.append("")
    for p in POINTS_OF_SALE_SAMPLE:
        lines.append(
            "INSERT INTO points_of_sale (name, city, region, tickets_sold, wins_recorded, data_note) "
            "VALUES ({}, {}, {}, {}, {}, 'Dati aggregati di esempio (simulati) - non dati reali');".format(
                _sql_str(p["name"]), _sql_str(p["city"]), _sql_str(p["region"]),
                p["tickets_sold"], p["wins_recorded"],
            )
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if "--dump-sql" in sys.argv:
        print(dump_sql(), end="")
    else:
        init_db()
        conn = get_conn()
        (count,) = conn.execute("SELECT COUNT(*) FROM games").fetchone()
        if count == 0:
            seed_all(conn)
            print(f"Database popolato: {len(GAMES)} giochi, {len(POINTS_OF_SALE_SAMPLE)} punti vendita.")
        else:
            print(f"Database già popolato ({count} giochi): nessuna modifica.")
