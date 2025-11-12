from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, vacas, subscriptions

settings = get_settings()

app = FastAPI(
    title="VacaFácil API",
    description="API para gestão de fazendas leiteiras",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(vacas.router)
app.include_router(subscriptions.router)

@app.get("/")
def read_root():
    return {"message": "VacaFácil API - Sistema de Gestão de Fazendas Leiteiras"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}