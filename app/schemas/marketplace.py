from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnuncioBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    categoria: str  # vaca, equipamento, insumo
    preco: float
    localizacao: Optional[str] = None
    telefone: Optional[str] = None

class AnuncioCreate(AnuncioBase):
    pass

class AnuncioUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    localizacao: Optional[str] = None
    telefone: Optional[str] = None
    ativo: Optional[bool] = None

class AnuncioResponse(AnuncioBase):
    id: int
    user_id: int
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True