from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserResponse, Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se usuário já existe
    db_user = db.query(User).filter(User.email.ilike(user.email)).first()
    if db_user:
        raise HTTPException(
            status_code=409,
            detail="Email já está em uso"
        )
    
    # Criar usuário
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        nome=user.nome,
        telefone=user.telefone,
        fazenda=user.fazenda,
        hashed_password=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Criar assinatura gratuita padrão
        from app.models.subscription_model import Subscription, PlanType
        default_subscription = Subscription(
            user_id=db_user.id,
            plan_type=PlanType.FREE,
            price=0.0
        )
        db.add(default_subscription)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar usuário: {str(e)}"
        )
    
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor"
        )
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Log tentativa de login inválida (sem expor dados sensíveis)
        import logging
        logging.warning(f"Tentativa de login inválida para usuário")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}