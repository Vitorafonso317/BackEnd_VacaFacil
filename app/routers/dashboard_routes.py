from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user_model import User
from app.models.cattle_model import Vaca
from app.models.production_model import Producao
from app.models.financial_model import Receita, Despesa
from app.utils.dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Estatísticas gerais do dashboard"""
    
    # Total de vacas
    total_vacas = db.query(Vaca).filter(Vaca.user_id == current_user.id).count()
    
    # Produção hoje
    hoje = datetime.now().date()
    producao_hoje = db.query(func.sum(Producao.quantidade)).filter(
        Producao.user_id == current_user.id,
        func.date(Producao.data) == hoje
    ).scalar() or 0
    
    # Produção mês
    inicio_mes = datetime.now().replace(day=1)
    producao_mes = db.query(func.sum(Producao.quantidade)).filter(
        Producao.user_id == current_user.id,
        Producao.data >= inicio_mes
    ).scalar() or 0
    
    # Receitas e despesas do mês
    receitas_mes = db.query(func.sum(Receita.valor)).filter(
        Receita.user_id == current_user.id,
        Receita.data >= inicio_mes
    ).scalar() or 0
    
    despesas_mes = db.query(func.sum(Despesa.valor)).filter(
        Despesa.user_id == current_user.id,
        Despesa.data >= inicio_mes
    ).scalar() or 0
    
    saldo_mes = float(receitas_mes) - float(despesas_mes)
    
    # Média de produção por vaca
    media_por_vaca = round(producao_hoje / total_vacas, 2) if total_vacas > 0 else 0
    
    return {
        "total_vacas": total_vacas,
        "producao_hoje": float(producao_hoje),
        "producao_mes": float(producao_mes),
        "media_por_vaca": media_por_vaca,
        "receitas_mes": float(receitas_mes),
        "despesas_mes": float(despesas_mes),
        "saldo_mes": saldo_mes
    }

@router.get("/producao-semanal")
def get_producao_semanal(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Produção dos últimos 7 dias"""
    
    dados = []
    for i in range(6, -1, -1):
        dia = datetime.now().date() - timedelta(days=i)
        producao = db.query(func.sum(Producao.quantidade)).filter(
            Producao.user_id == current_user.id,
            func.date(Producao.data) == dia
        ).scalar() or 0
        
        dados.append({
            "data": dia.strftime("%d/%m"),
            "quantidade": float(producao)
        })
    
    return dados

@router.get("/top-vacas")
def get_top_vacas(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Top vacas produtoras do mês"""
    
    inicio_mes = datetime.now().replace(day=1)
    
    top_vacas = db.query(
        Vaca.nome,
        Vaca.brinco,
        func.sum(Producao.quantidade).label("total")
    ).join(
        Producao, Producao.vaca_id == Vaca.id
    ).filter(
        Vaca.user_id == current_user.id,
        Producao.data >= inicio_mes
    ).group_by(
        Vaca.id
    ).order_by(
        func.sum(Producao.quantidade).desc()
    ).limit(limit).all()
    
    return [
        {
            "nome": vaca.nome,
            "brinco": vaca.brinco,
            "producao_total": float(vaca.total)
        }
        for vaca in top_vacas
    ]
