from sqlalchemy.orm import Session
from app.models.subscription_model import Subscription, Payment, PlanType, SubscriptionStatus
from app.models.cattle_model import Vaca
from app.schemas.subscription_schemas import SubscriptionCreate
from datetime import datetime, timedelta

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        
    def create_subscription(self, user_id: int, subscription_data: SubscriptionCreate):
        # Verificar se já tem assinatura
        existing = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if existing:
            return self.upgrade_subscription(user_id, subscription_data.plan_type)
        
        # Criar nova assinatura
        end_date = None
        if subscription_data.plan_type != PlanType.FREE:
            end_date = datetime.utcnow() + timedelta(days=30)
        
        subscription = Subscription(
            user_id=user_id,
            plan_type=subscription_data.plan_type,
            end_date=end_date,
            price=self.get_plan_price(subscription_data.plan_type),
            payment_method=subscription_data.payment_method
        )
        
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        return subscription
    
    def upgrade_subscription(self, user_id: int, new_plan: PlanType):
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            raise ValueError("Subscription not found")
        
        subscription.plan_type = new_plan
        subscription.price = self.get_plan_price(new_plan)
        subscription.updated_at = datetime.utcnow()
        
        if new_plan != PlanType.FREE:
            subscription.end_date = datetime.utcnow() + timedelta(days=30)
        else:
            subscription.end_date = None
        
        self.db.commit()
        return subscription
    
    def cancel_subscription(self, user_id: int):
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            raise ValueError("Subscription not found")
        
        subscription.status = SubscriptionStatus.CANCELLED
        self.db.commit()
        
        return {"message": "Subscription cancelled successfully"}
    
    def check_limits(self, user_id: int, resource: str, current_count: int = None):
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            return False
        
        limits = self.get_plan_limits(subscription.plan_type)
        
        if resource == "vacas":
            if current_count is None:
                current_count = self.db.query(Vaca).filter(
                    Vaca.user_id == user_id
                ).count()
            
            max_vacas = limits.get("max_vacas", 0)
            return max_vacas == -1 or current_count < max_vacas
        
        return True
    
    def get_plan_price(self, plan_type: PlanType) -> float:
        prices = {
            PlanType.FREE: 0.0,
            PlanType.BASIC: 29.90,
            PlanType.PRO: 59.90
        }
        return prices.get(plan_type, 0.0)
    
    def get_plan_limits(self, plan_type: PlanType) -> dict:
        limits = {
            PlanType.FREE: {
                "max_vacas": 5,
                "producao_historico": 30,
                "relatorios_mes": 5,
                "exportacoes_mes": 2
            },
            PlanType.BASIC: {
                "max_vacas": 50,
                "producao_historico": 365,
                "relatorios_mes": 50,
                "exportacoes_mes": 20
            },
            PlanType.PRO: {
                "max_vacas": -1,
                "producao_historico": -1,
                "relatorios_mes": -1,
                "exportacoes_mes": -1
            }
        }
        return limits.get(plan_type, {})