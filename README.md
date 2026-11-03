# GrattaData

App web (frontend + backend) per consultare le **probabilità ufficiali** dei Gratta e Vinci
italiani (fonte: **ADM – Agenzia delle Dogane e dei Monopoli**) e per **verificare un biglietto**
via scanner (fotocamera) o numero di serie.

> ⚠️ **Trasparenza:** le probabilità sono casuali e uguali ovunque. **Nessuna app può prevedere
> se un biglietto è vincente prima di grattarlo.** GrattaData non suggerisce "lotti fortunati" né
> numeri di serie vincenti: è impossibile. Per l'esito certo, gratta il biglietto e verifica con
> l'app ufficiale **My Lotteries**.
>
> Gioco vietato ai minori di 18 anni. Gioca responsabilmente.

## Stack

- **Backend:** Python 3.12 + FastAPI + SQLite (stdlib `sqlite3`)
- **Frontend:** React 18 + Vite + Tailwind CSS 4
- **Scanner:** `@zxing/browser` (lettura barcode/QR via fotocamera, lato client)
- **Database:** SQLite (`backend/grattadata.db`, creato e popolato automaticamente)

## Struttura

```
├── database/
│   ├── schema.sql          # schema del DB (tabelle games, points_of_sale, verification_logs)
│   └── seed.sql            # INSERT iniziali (generato da backend/app/data_games.py)
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py         # entrypoint FastAPI (serve anche il build del frontend)
│       ├── config.py       # disclaimer e link ufficiali
│       ├── db.py           # connessione SQLite + init schema
│       ├── data_games.py   # dati dei giochi con fonti ADM
│       ├── seed.py         # popolamento DB (anche --dump-sql)
│       ├── schemas.py      # modelli Pydantic
│       └── routers/        # games, stats, verify, meta
└── frontend/
    ├── index.html
    ├── vite.config.js      # proxy /api -> localhost:8000 in sviluppo
    └── src/
        ├── App.jsx         # tab: Catalogo | Dove si vince di più? | Verifica | Fonti
        ├── api.js          # client HTTP
        └── components/     # Banner, CatalogPage, StatsPage, VerifyPage, SourcesPage
```

## Avvio in locale (sviluppo)

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed                # crea e popola il database (solo la prima volta)
python -m uvicorn app.main:app --reload --port 8000
```

API su `http://localhost:8000` — documentazione interattiva su `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Apri `http://localhost:5173` (il proxy gira `/api` verso il backend sulla porta 8000).

## Popolare / aggiornare il database

I dati dei giochi sono in `backend/app/data_games.py` (ogni gioco riporta `source_url` ADM).
Per aggiornarli:

1. modifica `data_games.py` con i valori della scheda ufficiale ADM del gioco;
2. rigenera il file SQL: `cd backend && python -m app.seed --dump-sql > ../database/seed.sql`;
3. per ripopolare da zero: cancella `backend/grattadata.db` e riavvia il backend
   (oppure `sqlite3 grattadata.db < ../database/schema.sql < ../database/seed.sql`).

## Deployment locale "produzione" (un solo processo)

```bash
cd frontend && npm install && npm run build && cd ..
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

Il backend serve automaticamente `frontend/dist` su `http://localhost:8000`.

## API

| Metodo | Endpoint | Descrizione |
|---|---|---|
| GET | `/api/games?q=&price_min=&price_max=&max_odds=&sort=&order=` | Catalogo con filtri e ordinamento (`sort`: price, odds_win, odds_top, top_prize, name) |
| GET | `/api/games/{id}` | Dettaglio gioco |
| GET | `/api/games/meta/prices` | Prezzi distinti dei biglietti |
| GET | `/api/stats/overview` | Panoramica: nº giochi, media ufficiale ADM (1 su 3,60), payout max 75% |
| GET | `/api/stats/where-wins?limit=10` | Punti vendita con più vincite (dati di esempio) + disclaimer di correlazione statistica |
| POST | `/api/verify/serial` | Verifica **formale** del numero di serie (body: `{"serial": "..."}`) → 422 se formato non valido |
| POST | `/api/verify/scan` | Esito **simulato** dello scan (body: `{"code": "...", "code_type": "QR_CODE"}`) |
| GET | `/api/meta` | Disclaimer, link ufficiali (ADM, concessionario, My Lotteries) |
| GET | `/api/health` | Health check |

Gli endpoint sono pensati per essere interrogati anche da un agente AI tramite tool calling:
sono stateless, restituiscono JSON strutturato e codici di errore chiari (422 con `reasons`).

## Verifica biglietto

- **Scanner:** la fotocamera legge barcode/QR (ZXing nel browser); il codice viene inviato a
  `POST /api/verify/scan`, che restituisce un esito di esempio:
  *"Biglietto valido – verifica presso il punto vendita"* (simulazione, chiaramente etichettata).
- **Manuale:** `POST /api/verify/serial` controlla solo il formato (10-20 caratteri
  alfanumerici, almeno 8 cifre) e risponde: *"Numero di serie registrato. Per l'esito certo,
  gratta il biglietto e verifica con l'app ufficiale My Lotteries"*.
- Nessun endpoint controlla vincite reali: non esistono API pubbliche che lo permettano prima
  di grattare, e i log salvano solo l'hash SHA-256 del codice, mai il codice in chiaro.

## Fonte dei dati

- [ADM – Note sulle probabilità di vincita](https://www.adm.gov.it/portale/monopoli/giochi/lotterie/lotterie_istananee/lot_ist_note) (probabilità media 1 su 3,60; payout fino al 75%)
- [ADM – Lotterie istantanee attive](https://www.adm.gov.it/portale/monopoli/giochi/lotterie/lotterie_istananee)
- [Portale del concessionario – Probabilità di vincita](https://www.grattaevinci.com/probabilita-di-vincita)
- [App My Lotteries](https://www.mylotteriesplay.it/) per la verifica ufficiale delle vincite

I valori nel catalogo sono indicativi e possono cambiare: verifica sempre la scheda ufficiale
del singolo gioco su `adm.gov.it`.
