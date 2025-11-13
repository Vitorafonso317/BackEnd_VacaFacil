from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./vacafacil.db")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "sua_chave_secreta_super_segura_aqui")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    allowed_origins: list = ["http://localhost:5173", "http://localhost:3000"]

@lru_cache()
def get_settings():
    return Settings()