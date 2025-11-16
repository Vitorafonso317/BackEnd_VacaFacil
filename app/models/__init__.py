# Importar todos os modelos para garantir que sejam registrados no SQLAlchemy
from .user_model import User
from .cattle_model import Vaca
from .production_model import Producao
from .reproduction_model import Reproducao
from .financial_model import Receita, Despesa
from .marketplace_model import Anuncio
from .subscription_model import Subscription, Payment

__all__ = [
    "User",
    "Vaca", 
    "Producao",
    "Reproducao",
    "Receita",
    "Despesa",
    "Anuncio",
    "Subscription",
    "Payment"
]