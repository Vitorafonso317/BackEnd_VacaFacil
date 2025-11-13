from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ReproducaoBase(BaseModel):
    vaca_id: int
    tipo: str  # inseminacao, cobertura, parto
    data: date
    data_prevista_parto: Optional[date] = None
    sucesso: Optional[bool] = None
    observacoes: Optional[str] = None

class ReproducaoCreate(ReproducaoBase):
    pass

class ReproducaoResponse(ReproducaoBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True