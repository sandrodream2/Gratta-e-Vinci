"""Gestione della connessione SQLite e inizializzazione dello schema."""

import os
import sqlite3
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "database" / "schema.sql"
DB_PATH = Path(os.environ.get("GRATTA_DATA_DB", REPO_ROOT / "backend" / "grattadata.db"))

_lock = threading.Lock()
_conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    """Restituisce la connessione singleton al database SQLite."""
    global _conn
    if _conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA foreign_keys = ON")
    return _conn


def init_db() -> None:
    """Crea le tabelle leggendo database/schema.sql (idempotente)."""
    with _lock:
        conn = get_conn()
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()


def seed_if_empty() -> None:
    """Popola il database solo se la tabella dei giochi è vuota."""
    from .seed import seed_all

    with _lock:
        conn = get_conn()
        (count,) = conn.execute("SELECT COUNT(*) FROM games").fetchone()
        if count == 0:
            seed_all(conn)
