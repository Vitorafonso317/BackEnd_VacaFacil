from functools import wraps
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.services.subscription_service import SubscriptionService
from app.utils.dependencies import get_current_user

def check_subscription_limit(resource: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extrair dependências dos kwargs
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            
            if db and current_user:
                try:
                    service = SubscriptionService(db)
                    
                    if not service.check_limits(current_user.id, resource):
                        raise HTTPException(
                            status_code=403,
                            detail=f"Limite de assinatura atingido para {resource}. Faça upgrade do seu plano."
                        )
                except HTTPException:
                    raise
                except Exception as e:
                    # Em caso de erro na verificação, permitir acesso
                    import logging
                    logging.error(f"Subscription check error: {str(e)}")
                    pass
            
            return func(*args, **kwargs)
        return wrapper
    return decorator