from fastapi import FastAPI

from backend.routers import raw_materials, settings

from .database import Base, engine
from . import models
from .routers import products, categories, essences, bases, raw_materials, kits, settings, auth


# =========================================================
# APLICAÇÃO
# =========================================================

app = FastAPI(
    title="Star Limp Catálogo API",
    description="Backend exclusivo do catálogo da Star Limp.",
    version="1.0.0",
)

# =========================================================
# BANCO DE DADOS
# =========================================================

Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(essences.router)
app.include_router(bases.router)
app.include_router(raw_materials.router)
app.include_router(kits.router)
app.include_router(settings.router)
app.include_router(auth.router)

# =========================================================
# ROTA DE TESTE
# =========================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "project": "Star Limp Catálogo",
        "version": "1.0.0",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "database": "catalog.db",
    }

    from .routers import (
    products,
    categories,
    essences,
    bases,
    raw_materials,
    kits,
    settings,
    auth,
)