from pydantic import BaseModel, validator
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
    
    @validator('nome')
    def nome_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()
    
    @validator('idade')
    def idade_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Idade deve ser positiva')
        return v
    
    @validator('peso')
    def peso_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Peso deve ser positivo')
        return v
    
    @validator('producao_media')
    def producao_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Produção média deve ser positiva')
        return v
    
    @validator('status')
    def status_must_be_valid(cls, v):
        valid_status = ['ativa', 'inativa', 'vendida', 'morta']
        if v not in valid_status:
            raise ValueError(f'Status deve ser um de: {valid_status}')
        return v

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