from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.user import User
from app.models.reproducao import Reproducao
from app.schemas.reproducao import ReproducaoCreate, ReproducaoResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/reproducao", tags=["reproducao"])

@router.post("/", response_model=ReproducaoResponse)
def create_reproducao(
    reproducao: ReproducaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_reproducao = Reproducao(**reproducao.dict(), user_id=current_user.id)
    db.add(db_reproducao)
    db.commit()
    db.refresh(db_reproducao)
    return db_reproducao

@router.get("/", response_model=List[ReproducaoResponse])
def get_reproducoes(
    vaca_id: int = Query(None),
    tipo: str = Query(None),
    data_inicio: date = Query(None),
    data_fim: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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