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

@router.get("/producao")
def get_relatorio_producao(
    periodo: str = Query("30d"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    periodo_map = {"semanal": 7, "mensal": 30, "trimestral": 90, "anual": 365}
    dias = periodo_map.get(periodo, int(periodo.replace('d', '')) if 'd' in periodo else 30)
    data_inicio = (datetime.now() - timedelta(days=dias)).date()
    
    producoes = db.query(Producao).filter(
        Producao.user_id == current_user.id,
        Producao.data >= data_inicio
    ).all()
    
    if not producoes:
        return {"totalPeriodo": 0, "mediaDiaria": 0, "melhorDia": None, "piorDia": None}
    
    total = sum(p.quantidade_total for p in producoes)
    por_dia = {}
    for p in producoes:
        dia = p.data.isoformat()
        por_dia[dia] = por_dia.get(dia, 0) + p.quantidade_total
    
    melhor = max(por_dia.items(), key=lambda x: x[1])
    pior = min(por_dia.items(), key=lambda x: x[1])
    
    return {
        "totalPeriodo": round(total, 2),
        "mediaDiaria": round(total / dias, 2),
        "melhorDia": {"data": melhor[0], "producao": round(melhor[1], 2)},
        "piorDia": {"data": pior[0], "producao": round(pior[1], 2)}
    }

@router.get("/ranking")
def get_ranking_vacas(
    periodo: str = Query("30d"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    periodo_map = {"semanal": 7, "mensal": 30, "trimestral": 90, "anual": 365}
    dias = periodo_map.get(periodo, int(periodo.replace('d', '')) if 'd' in periodo else 30)
    data_inicio = (datetime.now() - timedelta(days=dias)).date()
    
    producoes = db.query(Producao).filter(
        Producao.user_id == current_user.id,
        Producao.data >= data_inicio
    ).all()
    
    ranking = {}
    for p in producoes:
        if p.vaca_id not in ranking:
            vaca = db.query(Vaca).filter(Vaca.id == p.vaca_id).first()
            ranking[p.vaca_id] = {
                "vaca": vaca.nome if vaca else "Desconhecida",
                "producao": 0,
                "registros": 0
            }
        ranking[p.vaca_id]["producao"] += p.quantidade_total
        ranking[p.vaca_id]["registros"] += 1
    
    result = sorted(ranking.values(), key=lambda x: x["producao"], reverse=True)
    for i, item in enumerate(result, 1):
        item["posicao"] = i
        item["media"] = round(item["producao"] / item["registros"], 2) if item["registros"] > 0 else 0
        item["producao"] = round(item["producao"], 2)
        del item["registros"]
    
    return result

@router.get("/lucratividade")
def get_lucratividade(
    periodo: str = Query("30d"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    periodo_map = {"semanal": 7, "mensal": 30, "trimestral": 90, "anual": 365}
    dias = periodo_map.get(periodo, int(periodo.replace('d', '')) if 'd' in periodo else 30)
    data_inicio = (datetime.now() - timedelta(days=dias)).date()
    
    receitas = db.query(Receita).filter(
        Receita.user_id == current_user.id,
        Receita.data >= data_inicio
    ).all()
    
    despesas = db.query(Despesa).filter(
        Despesa.user_id == current_user.id,
        Despesa.data >= data_inicio
    ).all()
    
    total_receita = sum(r.valor for r in receitas)
    total_custos = sum(d.valor for d in despesas)
    lucro = total_receita - total_custos
    margem = (lucro / total_receita * 100) if total_receita > 0 else 0
    
    return {
        "receita": round(total_receita, 2),
        "custos": round(total_custos, 2),
        "lucro": round(lucro, 2),
        "margem": round(margem, 2)
    }

@router.get("/reproducao")
def get_reproducao(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.reproduction_model import Reproducao
    
    eventos = db.query(Reproducao).filter(
        Reproducao.user_id == current_user.id
    ).all()
    
    total = len(eventos)
    prenhas = len([e for e in eventos if e.tipo_evento == "prenhez"])
    partos = len([e for e in eventos if e.tipo_evento == "parto"])
    
    return {
        "taxaPrenhez": round((prenhas / total * 100) if total > 0 else 0, 2),
        "intervaloPartos": 365,
        "partosEsperados": partos
    }
