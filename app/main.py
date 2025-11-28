from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import get_settings
from app.database import engine, Base
from app.logging_config import setup_logging
# Importar todos os modelos para criar as tabelas
from app.models import *
from app.routers import (
    auth_routes, user_routes, cattle_routes, production_routes,
    financial_routes, reproduction_routes, marketplace_routes,
    subscription_routes, ml_routes, chat_routes
)

setup_logging()
settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VacaFácil API",
    description="API para gestão de fazendas leiteiras",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (uploads locais)
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(cattle_routes.router)
app.include_router(production_routes.router)
app.include_router(financial_routes.router)
app.include_router(reproduction_routes.router)
app.include_router(marketplace_routes.router)
app.include_router(subscription_routes.router)
app.include_router(ml_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def root():
    return {"message": "VacaFácil API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
