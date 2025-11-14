from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.subscription_model import Subscription, PlanType
from app.schemas.subscription_schemas import SubscriptionCreate, SubscriptionResponse, UsageLimits
from app.utils.dependencies import get_current_user
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.get("/plans")
def get_plans():
    """Listar todos os planos disponíveis"""
    return {
        "free": {
            "name": "Gratuito",
            "price": 0,
            "max_vacas": 5,
            "features": {
                "producao_historico": 30,
                "relatorios": "basico",
                "marketplace": False,
                "analytics": False
            }
        },
        "basic": {
            "name": "Básico",
            "price": 29.90,
            "max_vacas": 50,
            "features": {
                "producao_historico": 365,
                "relatorios": "completo",
                "marketplace": True,
                "analytics": "basico"
            }
        },
        "pro": {
            "name": "Pro",
            "price": 59.90,
            "max_vacas": -1,
            "features": {
                "producao_historico": -1,
                "relatorios": "avancado",
                "marketplace": True,
                "analytics": "avancado",
                "api_access": True,
                "backup": True
            }
        }
    }

@router.post("/subscribe", response_model=SubscriptionResponse)
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        service = SubscriptionService(db)
        return service.create_subscription(current_user.id, subscription)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/status", response_model=SubscriptionResponse)
def get_subscription_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        subscription = db.query(Subscription).filter(
            Subscription.user_id == current_user.id
        ).first()
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Assinatura não encontrada")
        
        return subscription
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar assinatura: {str(e)}")

@router.put("/upgrade", response_model=SubscriptionResponse)
def upgrade_subscription(
    new_plan: PlanType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        service = SubscriptionService(db)
        return service.upgrade_subscription(current_user.id, new_plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/cancel")
def cancel_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        service = SubscriptionService(db)
        return service.cancel_subscription(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao cancelar assinatura: {str(e)}")