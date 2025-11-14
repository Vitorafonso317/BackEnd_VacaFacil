from sqlalchemy.orm import Session
from app.models.subscription_model import Subscription, Payment, PlanType, SubscriptionStatus
from app.models.cattle_model import Vaca
from app.schemas.subscription_schemas import SubscriptionCreate
from datetime import datetime, timedelta

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        
    def create_subscription(self, user_id: int, subscription_data: SubscriptionCreate):
        try:
            # Verificar se já tem assinatura
            existing = self.db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
            
            if existing:
                return self.upgrade_subscription(user_id, subscription_data.plan_type)
            
            # Criar nova assinatura
            end_date = None
            if subscription_data.plan_type != PlanType.FREE:
                end_date = datetime.now() + timedelta(days=30)
        except Exception as e:
            raise ValueError(f"Erro ao criar assinatura: {str(e)}")
        
        try:
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
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Erro ao salvar assinatura: {str(e)}")
    
    def upgrade_subscription(self, user_id: int, new_plan: PlanType):
        try:
            subscription = self.db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
            
            if not subscription:
                raise ValueError("Assinatura não encontrada")
            
            subscription.plan_type = new_plan
            subscription.price = self.get_plan_price(new_plan)
            subscription.updated_at = datetime.now()
            
            if new_plan != PlanType.FREE:
                subscription.end_date = datetime.now() + timedelta(days=30)
            else:
                subscription.end_date = None
            
            self.db.commit()
            return subscription
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Erro ao fazer upgrade: {str(e)}")
    
    def cancel_subscription(self, user_id: int):
        try:
            subscription = self.db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
            
            if not subscription:
                raise ValueError("Assinatura não encontrada")
            
            subscription.status = SubscriptionStatus.CANCELLED
            self.db.commit()
            
            return {"message": "Assinatura cancelada com sucesso"}
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Erro ao cancelar assinatura: {str(e)}")
    
    def check_limits(self, user_id: int, resource: str, current_count: int = None):
        try:
            subscription = self.db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).first()
        except Exception as e:
            import logging
            logging.error(f"Database error in check_limits: {str(e)}")
            return False  # Em caso de erro, negar acesso
        
        if not subscription:
            try:
                # Se não tem assinatura, criar uma gratuita
                subscription = Subscription(
                    user_id=user_id,
                    plan_type=PlanType.FREE,
                    price=0.0
                )
                self.db.add(subscription)
                self.db.commit()
            except Exception as e:
                import logging
                logging.error(f"Error creating default subscription: {str(e)}")
                self.db.rollback()
                return False
        
        limits = self.get_plan_limits(subscription.plan_type)
        
        if resource == "vacas":
            if current_count is None:
                current_count = self.db.query(Vaca).filter(
                    Vaca.user_id == user_id
                ).count()
            
            max_vacas = limits.get("max_vacas", 0)
            return max_vacas == -1 or current_count <= max_vacas
        
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