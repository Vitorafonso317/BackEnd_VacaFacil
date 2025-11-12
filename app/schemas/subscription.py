from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.subscription import PlanType, SubscriptionStatus

class PlanBase(BaseModel):
    name: str
    price: float
    max_vacas: int
    features: dict

class SubscriptionCreate(BaseModel):
    plan_type: PlanType
    payment_method: Optional[str] = None

class SubscriptionUpdate(BaseModel):
    plan_type: Optional[PlanType] = None
    status: Optional[SubscriptionStatus] = None

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_type: PlanType
    status: SubscriptionStatus
    start_date: datetime
    end_date: Optional[datetime]
    price: float
    
    class Config:
        from_attributes = True

class UsageLimits(BaseModel):
    vacas: dict
    producao: dict
    relatorios: dict
    exportacoes: dict