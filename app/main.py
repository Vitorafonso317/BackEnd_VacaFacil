from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth_routes, user_routes, cattle_routes, production_routes, financial_routes, reproduction_routes, marketplace_routes, subscription_routes, ml_routes
from app.utils.exception_handlers import validation_exception_handler, http_exception_handler, general_exception_handler

# Criar tabelas
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title="VacaFácil API",
    description="API para gestão de fazendas leiteiras",
    version="1.0.0"
)

# Exception Handlers
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(cattle_routes.router)
app.include_router(production_routes.router)
app.include_router(financial_routes.router)
app.include_router(reproduction_routes.router)
app.include_router(marketplace_routes.router)
app.include_router(subscription_routes.router)
app.include_router(ml_routes.router)

@app.get("/")
def read_root():
    return {"message": "VacaFácil API - Sistema de Gestão de Fazendas Leiteiras"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}