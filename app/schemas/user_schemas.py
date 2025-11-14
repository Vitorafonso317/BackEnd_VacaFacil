from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nome: str
    telefone: Optional[str] = None
    fazenda: Optional[str] = None
    
    @validator('nome')
    def nome_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if not v:
            raise ValueError('Senha é obrigatória')
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    fazenda: Optional[str] = None
    foto_perfil: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    foto_perfil: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None