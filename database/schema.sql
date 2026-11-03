-- GrattaData - schema del database SQLite
-- Le tabelle vengono create automaticamente all'avvio del backend
-- (backend/app/db.py legge questo file), ma possono essere ricreate a mano con:
--   sqlite3 grattadata.db < database/schema.sql

-- Catalogo dei giochi (Gratta e Vinci) con le probabilità ufficiali pubblicate da ADM.
-- odds_win / odds_top sono DENOMINATORI: "1 su odds_win" = probabilità di vincita (premi > costo),
-- "1 su odds_top" = probabilità del premio massimo. Valori NULL = dato non disponibile.
CREATE TABLE IF NOT EXISTS games (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    price         REAL    NOT NULL,              -- prezzo del biglietto in euro
    odds_win      REAL,                          -- es. 7.84 significa "1 su 7,84"
    odds_top      REAL,                          -- es. 6000000 significa "1 su 6.000.000"
    top_prize     REAL,                          -- premio massimo in euro (NULL se non disponibile)
    active        INTEGER NOT NULL DEFAULT 1,    -- 1 = gioco attivo, 0 = ritirato
    source_url    TEXT    NOT NULL,              -- fonte ufficiale (pagina ADM o concessionario)
    source_label  TEXT    NOT NULL,              -- etichetta leggibile della fonte
    notes         TEXT,                          -- note aggiuntive sulle probabilità
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_games_price    ON games (price);
CREATE INDEX IF NOT EXISTS idx_games_odds_win ON games (odds_win);

-- Punti vendita con dati aggregati di vendita/vincite (ESEMPIO / SIMULATI).
-- Usati solo per la sezione "Dove si vince di più?" con disclaimer di correlazione statistica.
CREATE TABLE IF NOT EXISTS points_of_sale (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    city           TEXT    NOT NULL,
    region         TEXT    NOT NULL,
    tickets_sold   INTEGER NOT NULL,             -- biglietti venduti (aggregato storico)
    wins_recorded  INTEGER NOT NULL,             -- vincite registrate (aggregato storico)
    data_note      TEXT    NOT NULL DEFAULT 'Dati aggregati di esempio (simulati) - non dati reali'
);

-- Log delle verifiche (solo hash SHA-256 del codice, mai il codice in chiaro).
CREATE TABLE IF NOT EXISTS verification_logs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    kind       TEXT    NOT NULL,                 -- 'serial' oppure 'scan'
    code_hash  TEXT    NOT NULL,                 -- sha256 del codice inviato
    valid      INTEGER NOT NULL,                 -- 1 = formato valido, 0 = non valido
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
