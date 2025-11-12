from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProducaoBase(BaseModel):
    vaca_id: int
    data: date
    quantidade_manha: float = 0
    quantidade_tarde: float = 0
    observacoes: Optional[str] = None

class ProducaoCreate(ProducaoBase):
    pass

class ProducaoUpdate(BaseModel):
    quantidade_manha: Optional[float] = None
    quantidade_tarde: Optional[float] = None
    observacoes: Optional[str] = None

class ProducaoResponse(ProducaoBase):
    id: int
    user_id: int
    quantidade_total: float
    
    class Config:
        from_attributes = True