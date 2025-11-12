from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.user import User
from app.models.producao import Producao
from app.schemas.producao import ProducaoCreate, ProducaoUpdate, ProducaoResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/producao", tags=["producao"])

@router.post("/", response_model=ProducaoResponse)
def create_producao(
    producao: ProducaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quantidade_total = producao.quantidade_manha + producao.quantidade_tarde
    
    db_producao = Producao(
        **producao.dict(),
        user_id=current_user.id,
        quantidade_total=quantidade_total
    )
    db.add(db_producao)
    db.commit()
    db.refresh(db_producao)
    return db_producao

@router.get("/", response_model=List[ProducaoResponse])
def get_producoes(
    vaca_id: int = Query(None),
    data_inicio: date = Query(None),
    data_fim: date = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Producao).filter(Producao.user_id == current_user.id)
    
    if vaca_id:
        query = query.filter(Producao.vaca_id == vaca_id)
    if data_inicio:
        query = query.filter(Producao.data >= data_inicio)
    if data_fim:
        query = query.filter(Producao.data <= data_fim)
    
    return query.offset(skip).limit(limit).all()

@router.put("/{producao_id}", response_model=ProducaoResponse)
def update_producao(
    producao_id: int,
    producao_update: ProducaoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    producao = db.query(Producao).filter(
        Producao.id == producao_id,
        Producao.user_id == current_user.id
    ).first()
    
    if not producao:
        raise HTTPException(status_code=404, detail="Producao not found")
    
    for field, value in producao_update.dict(exclude_unset=True).items():
        setattr(producao, field, value)
    
    producao.quantidade_total = producao.quantidade_manha + producao.quantidade_tarde
    
    db.commit()
    db.refresh(producao)
    return producao