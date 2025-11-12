from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://vacafacil_user:sua_senha_aqui@localhost/vacafacil"
    
    # JWT
    secret_key: str = "sua_chave_secreta_super_segura_aqui"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()