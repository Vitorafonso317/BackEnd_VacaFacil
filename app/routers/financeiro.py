from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.user import User
from app.models.financeiro import Receita, Despesa
from app.schemas.financeiro import ReceitaCreate, ReceitaResponse, DespesaCreate, DespesaResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/financeiro", tags=["financeiro"])

@router.post("/receitas", response_model=ReceitaResponse)
def create_receita(
    receita: ReceitaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_receita = Receita(**receita.dict(), user_id=current_user.id)
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita

@router.get("/receitas", response_model=List[ReceitaResponse])
def get_receitas(
    data_inicio: date = Query(None),
    data_fim: date = Query(None),
    categoria: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Receita).filter(Receita.user_id == current_user.id)
    
    if data_inicio:
        query = query.filter(Receita.data >= data_inicio)
    if data_fim:
        query = query.filter(Receita.data <= data_fim)
    if categoria:
        query = query.filter(Receita.categoria == categoria)
    
    return query.all()

@router.post("/despesas", response_model=DespesaResponse)
def create_despesa(
    despesa: DespesaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_despesa = Despesa(**despesa.dict(), user_id=current_user.id)
    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa

@router.get("/despesas", response_model=List[DespesaResponse])
def get_despesas(
    data_inicio: date = Query(None),
    data_fim: date = Query(None),
    categoria: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Despesa).filter(Despesa.user_id == current_user.id)
    
    if data_inicio:
        query = query.filter(Despesa.data >= data_inicio)
    if data_fim:
        query = query.filter(Despesa.data <= data_fim)
    if categoria:
        query = query.filter(Despesa.categoria == categoria)
    
    return query.all()