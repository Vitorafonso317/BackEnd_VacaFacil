from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nome: str
    telefone: Optional[str] = None
    fazenda: Optional[str] = None

class UserCreate(UserBase):
    password: str

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