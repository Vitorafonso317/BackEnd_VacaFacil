from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        email = verify_token(token)
        if email is None:
            print(f"❌ Token inválido ou expirado")
            raise credentials_exception
        
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            print(f"❌ Usuário não encontrado: {email}")
            raise credentials_exception
        
        print(f"✅ Usuário autenticado: {email}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro na autenticação: {str(e)}")
        raise credentials_exception