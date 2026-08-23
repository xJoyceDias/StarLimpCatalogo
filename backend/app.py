from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import products, categories


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