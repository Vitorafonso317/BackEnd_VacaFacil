from pydantic import BaseModel, validator
from functools import lru_cache
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

class Settings(BaseModel):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./vacafacil.db")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 horas
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if v == "CHANGE_ME_IN_PRODUCTION":
            import warnings
            warnings.warn("⚠️ Usando SECRET_KEY padrão. Configure no .env para produção!")
        return v
    
    # CORS
    allowed_origins: list = ["http://localhost:5173", "http://localhost:3000"]

@lru_cache()
def get_settings():
    return Settings()