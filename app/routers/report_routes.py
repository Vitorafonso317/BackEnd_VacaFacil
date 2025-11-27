from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from io import BytesIO
from app.database import get_db
from app.models.user_model import User
from app.models.production_model import Producao
from app.models.financial_model import Receita, Despesa
from app.models.cattle_model import Vaca
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

@router.get("/producao/json")
def relatorio_producao_json(
    data_inicio: str = Query(None),
    data_fim: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Relatório de produção em JSON"""
    query = db.query(Producao).filter(Producao.user_id == current_user.id)
    
    if data_inicio:
        query = query.filter(Producao.data >= datetime.fromisoformat(data_inicio).date())
    if data_fim:
        query = query.filter(Producao.data <= datetime.fromisoformat(data_fim).date())
    
    producoes = query.all()
    
    # Calcular estatísticas
    total_producao = sum(p.quantidade_total for p in producoes)
    media_diaria = total_producao / len(producoes) if producoes else 0
    
    # Agrupar por vaca
    por_vaca = {}
    for p in producoes:
        if p.vaca_id not in por_vaca:
            vaca = db.query(Vaca).filter(Vaca.id == p.vaca_id).first()
            por_vaca[p.vaca_id] = {
                "vaca_nome": vaca.nome if vaca else "Desconhecida",
                "total": 0,
                "registros": 0
            }
        por_vaca[p.vaca_id]["total"] += p.quantidade_total
        por_vaca[p.vaca_id]["registros"] += 1
    
    return {
        "periodo": {
            "inicio": data_inicio or "Início",
            "fim": data_fim or "Hoje"
        },
        "resumo": {
            "total_producao": round(total_producao, 2),
            "media_diaria": round(media_diaria, 2),
            "total_registros": len(producoes)
        },
        "por_vaca": por_vaca,
        "registros": [
            {
                "data": p.data.isoformat(),
                "vaca_id": p.vaca_id,
                "quantidade_manha": p.quantidade_manha,
                "quantidade_tarde": p.quantidade_tarde,
                "quantidade_total": p.quantidade_total
            }
            for p in producoes
        ]
    }

@router.get("/financeiro/json")
def relatorio_financeiro_json(
    data_inicio: str = Query(None),
    data_fim: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Relatório financeiro em JSON"""
    # Receitas
    query_receitas = db.query(Receita).filter(Receita.user_id == current_user.id)
    if data_inicio:
        query_receitas = query_receitas.filter(Receita.data >= datetime.fromisoformat(data_inicio).date())
    if data_fim:
        query_receitas = query_receitas.filter(Receita.data <= datetime.fromisoformat(data_fim).date())
    receitas = query_receitas.all()
    
    # Despesas
    query_despesas = db.query(Despesa).filter(Despesa.user_id == current_user.id)
    if data_inicio:
        query_despesas = query_despesas.filter(Despesa.data >= datetime.fromisoformat(data_inicio).date())
    if data_fim:
        query_despesas = query_despesas.filter(Despesa.data <= datetime.fromisoformat(data_fim).date())
    despesas = query_despesas.all()
    
    # Calcular totais
    total_receitas = sum(r.valor for r in receitas)
    total_despesas = sum(d.valor for d in despesas)
    saldo = total_receitas - total_despesas
    
    # Agrupar por categoria
    receitas_por_categoria = {}
    for r in receitas:
        if r.categoria not in receitas_por_categoria:
            receitas_por_categoria[r.categoria] = 0
        receitas_por_categoria[r.categoria] += r.valor
    
    despesas_por_categoria = {}
    for d in despesas:
        if d.categoria not in despesas_por_categoria:
            despesas_por_categoria[d.categoria] = 0
        despesas_por_categoria[d.categoria] += d.valor
    
    return {
        "periodo": {
            "inicio": data_inicio or "Início",
            "fim": data_fim or "Hoje"
        },
        "resumo": {
            "total_receitas": round(total_receitas, 2),
            "total_despesas": round(total_despesas, 2),
            "saldo": round(saldo, 2),
            "margem": round((saldo / total_receitas * 100) if total_receitas > 0 else 0, 2)
        },
        "receitas_por_categoria": {k: round(v, 2) for k, v in receitas_por_categoria.items()},
        "despesas_por_categoria": {k: round(v, 2) for k, v in despesas_por_categoria.items()},
        "receitas": [
            {
                "data": r.data.isoformat(),
                "categoria": r.categoria,
                "valor": r.valor,
                "descricao": r.descricao
            }
            for r in receitas
        ],
        "despesas": [
            {
                "data": d.data.isoformat(),
                "categoria": d.categoria,
                "valor": d.valor,
                "descricao": d.descricao
            }
            for d in despesas
        ]
    }

@router.get("/completo/json")
def relatorio_completo_json(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Relatório completo da fazenda"""
    # Últimos 30 dias
    data_inicio = (datetime.now() - timedelta(days=30)).date()
    
    # Vacas
    vacas = db.query(Vaca).filter(Vaca.user_id == current_user.id).all()
    
    # Produção
    producoes = db.query(Producao).filter(
        Producao.user_id == current_user.id,
        Producao.data >= data_inicio
    ).all()
    
    # Financeiro
    receitas = db.query(Receita).filter(
        Receita.user_id == current_user.id,
        Receita.data >= data_inicio
    ).all()
    despesas = db.query(Despesa).filter(
        Despesa.user_id == current_user.id,
        Despesa.data >= data_inicio
    ).all()
    
    return {
        "periodo": "Últimos 30 dias",
        "rebanho": {
            "total_vacas": len(vacas),
            "vacas_ativas": len([v for v in vacas if v.ativa])
        },
        "producao": {
            "total": round(sum(p.quantidade_total for p in producoes), 2),
            "media_diaria": round(sum(p.quantidade_total for p in producoes) / 30, 2),
            "registros": len(producoes)
        },
        "financeiro": {
            "receitas": round(sum(r.valor for r in receitas), 2),
            "despesas": round(sum(d.valor for d in despesas), 2),
            "saldo": round(sum(r.valor for r in receitas) - sum(d.valor for d in despesas), 2)
        }
    }
