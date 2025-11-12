from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VacaBase(BaseModel):
    nome: str
    raca: str
    idade: Optional[int] = None
    peso: Optional[float] = None
    producao_media: Optional[float] = None
    status: str = "ativa"
    observacoes: Optional[str] = None

class VacaCreate(VacaBase):
    pass

class VacaUpdate(BaseModel):
    nome: Optional[str] = None
    raca: Optional[str] = None
    idade: Optional[int] = None
    peso: Optional[float] = None
    producao_media: Optional[float] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None

class VacaResponse(VacaBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True