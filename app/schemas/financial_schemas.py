from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ReceitaBase(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria: str = "venda_leite"
    observacoes: Optional[str] = None

class ReceitaCreate(ReceitaBase):
    pass

class ReceitaResponse(ReceitaBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DespesaBase(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria: str
    observacoes: Optional[str] = None

class DespesaCreate(DespesaBase):
    pass

class DespesaResponse(DespesaBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True