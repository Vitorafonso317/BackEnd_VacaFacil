from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth_routes, user_routes, cattle_routes, production_routes, financial_routes, reproduction_routes, marketplace_routes, subscription_routes, ml_routes
from app.utils.exception_handlers import validation_exception_handler, http_exception_handler, general_exception_handler
from app.middleware.security_middleware import SecurityMiddleware

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Criar tabelas
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {str(e)}")
    raise RuntimeError(f"Falha crítica ao inicializar banco: {str(e)}")

logger.info("=== VacaFacil API ===")
try:
    connection = engine.connect()
    db_type = "PostgreSQL" if "postgresql" in settings.database_url else "SQLite"
    logger.info(f"Banco de dados {db_type} conectado com sucesso!")
    
    if "postgresql" in settings.database_url:
        logger.info("Usando PostgreSQL em produção")
    else:
        logger.info("Usando SQLite para desenvolvimento")
    
    connection.close()
except Exception as e:
    logger.error(f"Conexão com banco falhou: {str(e)}")
    logger.info("Verifique as configurações do banco de dados")

print("[INFO] Servidor iniciando...")
print("[INFO] Documentacao: http://localhost:8000/docs")

app = FastAPI(
    title="VacaFácil API",
    description="API para gestão de fazendas leiteiras",
    version="1.0.0"
)

# Exception Handlers
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Middleware de segurança
app.add_middleware(SecurityMiddleware)

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
    try:
        # Testar conexão com banco
        connection = engine.connect()
        connection.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Serviço indisponível")