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
    subscription_routes, ml_routes, chat_routes, notification_routes
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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://front-vacafacil.vercel.app",
        "*"  # Fallback para qualquer origem
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    expose_headers=["*"],
    max_age=3600,
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
app.include_router(notification_routes.router)

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handler para requisições OPTIONS (CORS preflight)"""
    return {"message": "OK"}

@app.get("/")
@app.head("/")
def root():
    return {"message": "VacaFácil API", "version": "1.0.0"}

@app.get("/health")
@app.head("/health")
def health():
    return {"status": "healthy"}
