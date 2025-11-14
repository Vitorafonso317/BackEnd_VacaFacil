from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.user_model import User
from app.models.reproduction_model import Reproducao
from app.schemas.reproduction_schemas import ReproducaoCreate, ReproducaoResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/reproducao", tags=["reproducao"])

@router.post("/", response_model=ReproducaoResponse)
def create_reproducao(
    reproducao: ReproducaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_reproducao = Reproducao(**reproducao.dict(), user_id=current_user.id)
        db.add(db_reproducao)
        db.commit()
        db.refresh(db_reproducao)
        return db_reproducao
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar reprodução: {str(e)}")

@router.get("/", response_model=List[ReproducaoResponse])
def get_reproducoes(
    vaca_id: int = Query(None),
    tipo: str = Query(None),
    data_inicio: date = Query(None),
    data_fim: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        query = db.query(Reproducao).filter(Reproducao.user_id == current_user.id)
        
        if vaca_id:
            query = query.filter(Reproducao.vaca_id == vaca_id)
        if tipo:
            query = query.filter(Reproducao.tipo == tipo)
        if data_inicio:
            query = query.filter(Reproducao.data >= data_inicio)
        if data_fim:
            query = query.filter(Reproducao.data <= data_fim)
        
        return query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar reproduções: {str(e)}")