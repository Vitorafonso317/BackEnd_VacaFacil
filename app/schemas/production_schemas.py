from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class ProducaoBase(BaseModel):
    vaca_id: int
    data: date
    quantidade_manha: float = 0
    quantidade_tarde: float = 0
    observacoes: Optional[str] = None
    
    @validator('quantidade_manha', 'quantidade_tarde')
    def validate_quantities(cls, v):
        if v < 0:
            raise ValueError('Quantidade não pode ser negativa')
        if v > 100:
            raise ValueError('Quantidade muito alta (máximo 100L)')
        return v

class ProducaoCreate(ProducaoBase):
    pass

class ProducaoUpdate(BaseModel):
    quantidade_manha: Optional[float] = None
    quantidade_tarde: Optional[float] = None
    observacoes: Optional[str] = None
    
    @validator('quantidade_manha', 'quantidade_tarde')
    def validate_quantities(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError('Quantidade não pode ser negativa')
            if v > 100:
                raise ValueError('Quantidade muito alta (máximo 100L)')
        return v

class ProducaoResponse(ProducaoBase):
    id: int
    user_id: int
    quantidade_total: float
    
    class Config:
        from_attributes = True