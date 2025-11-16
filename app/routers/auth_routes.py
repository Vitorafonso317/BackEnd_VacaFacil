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

@router.post("/test-register")
def test_register(user: UserCreate):
    return {"message": "Dados recebidos", "email": user.email, "nome": user.nome}

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    import traceback
    print(f"\n=== DADOS RECEBIDOS ===")
    print(f"Email: {user.email}")
    print(f"Nome: {user.nome}")
    print(f"Password: {'*' * len(user.password)}")
    print(f"Telefone: {user.telefone}")
    print(f"Fazenda: {user.fazenda}")
    print(f"========================\n")
    try:
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
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"ERRO NO REGISTRO: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

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