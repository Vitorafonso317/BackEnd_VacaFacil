from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnuncioBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descricao: str = Field(..., min_length=10)
    tipo: str = Field(..., pattern="^(venda|procura)$")
    categoria: Optional[str] = "vaca"  # vaca, equipamento, insumo
    raca: Optional[str] = None
    idade: Optional[int] = Field(None, ge=0)
    producao_diaria: Optional[float] = Field(None, ge=0)
    preco: float = Field(..., ge=0)
    imagem_url: Optional[str] = None
    contato: Optional[str] = None
    localizacao: Optional[str] = None

class AnuncioCreate(AnuncioBase):
    pass

class AnuncioUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    producao_diaria: Optional[float] = None
    contato: Optional[str] = None
    localizacao: Optional[str] = None
    ativo: Optional[bool] = None

class AnuncioResponse(AnuncioBase):
    id: int
    user_id: int
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True