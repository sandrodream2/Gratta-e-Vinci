"""GrattaData - backend FastAPI.

Avvio in sviluppo:
    cd backend
    python -m uvicorn app.main:app --reload --port 8000

In produzione il backend serve anche il build del frontend (frontend/dist).
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .db import init_db, seed_if_empty
from .routers import games, meta, stats, verify

REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = REPO_ROOT / "frontend" / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_if_empty()
    yield


app = FastAPI(
    title="GrattaData API",
    version="1.0.0",
    description=(
        "Consultazione delle probabilità ufficiali dei Gratta e Vinci (fonte ADM) "
        "e verifica formale/simulata dei biglietti. Nessuna funzione predittiva: "
        "le probabilità sono casuali e uguali ovunque."
    ),
    lifespan=lifespan,
)

# CORS aperto: in sviluppo il frontend Vite gira su un'altra porta (proxy configurata)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(verify.router, prefix="/api/verify", tags=["verify"])
app.include_router(meta.router, prefix="/api/meta", tags=["meta"])


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve il build statico del frontend (npm run build) se presente.
# Le route /api sono registrate prima del mount, quindi hanno priorità.
if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
