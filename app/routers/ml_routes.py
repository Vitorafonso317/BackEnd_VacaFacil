from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.schemas.ml_schemas import (
    PredictionRequest, MLPredictionResult, PerformanceAnalysis,
    AnomalyDetection, RecommendationResult, FinancialForecast
)
try:
    from app.services.ml_service import MLService
except ImportError:
    from app.services.ml_service_simple import MLServiceSimple as MLService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/ml", tags=["machine-learning"])

@router.post("/predict-production", response_model=MLPredictionResult)
def predict_milk_production(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Prediz produção de leite usando ML"""
    try:
        ml_service = MLService(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inicializar ML: {str(e)}")
    
    # Verificar se a vaca pertence ao usuário
    from app.models.cattle_model import Vaca
    vaca = db.query(Vaca).filter(
        Vaca.id == request.vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    try:
        # Tentar método completo, senão usar simples
        if hasattr(ml_service, 'predict_milk_production'):
            result = ml_service.predict_milk_production(request.vaca_id, request.days_ahead)
        else:
            result = ml_service.predict_milk_production_simple(request.vaca_id, request.days_ahead)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@router.get("/analyze-performance", response_model=PerformanceAnalysis)
def analyze_cattle_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Análise de performance do rebanho com ML"""
    try:
        ml_service = MLService(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inicializar ML: {str(e)}")
    try:
        # Tentar método completo, senão usar simples
        if hasattr(ml_service, 'analyze_cattle_performance'):
            result = ml_service.analyze_cattle_performance(current_user.id)
        else:
            result = ml_service.analyze_performance_simple(current_user.id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.get("/detect-anomalies", response_model=AnomalyDetection)
def detect_production_anomalies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Detecta anomalias na produção usando ML"""
    try:
        ml_service = MLService(db)
        result = ml_service.detect_anomalies(current_user.id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na detecção: {str(e)}")

@router.get("/recommendations", response_model=RecommendationResult)
def get_smart_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recomendações inteligentes baseadas em ML"""
    try:
        ml_service = MLService(db)
        result = ml_service.recommend_actions(current_user.id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro nas recomendações: {str(e)}")

@router.get("/financial-forecast", response_model=FinancialForecast)
def get_financial_forecast(
    price_per_liter: float = Query(2.50, description="Preço por litro de leite"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Previsão financeira baseada na produção"""
    try:
        ml_service = MLService(db)
        result = ml_service.financial_forecast(current_user.id, price_per_liter)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na previsão: {str(e)}")

@router.get("/insights")
def get_ml_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dashboard com insights de ML"""
    try:
        ml_service = MLService(db)
        
        # Combinar várias análises com tratamento individual
        results = {"status": "success"}
        
        try:
            performance = ml_service.analyze_cattle_performance(current_user.id)
            results["performance"] = performance if "error" not in performance else None
        except Exception as e:
            import logging
            logging.warning(f"Performance analysis error: {str(e)}")
            results["performance"] = None
        
        try:
            recommendations = ml_service.recommend_actions(current_user.id)
            results["recommendations"] = recommendations if "error" not in recommendations else None
        except Exception as e:
            import logging
            logging.warning(f"Recommendations error: {str(e)}")
            results["recommendations"] = None
        
        try:
            forecast = ml_service.financial_forecast(current_user.id)
            results["forecast"] = forecast if "error" not in forecast else None
        except Exception as e:
            import logging
            logging.warning(f"Financial forecast error: {str(e)}")
            results["forecast"] = None
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro nos insights: {str(e)}")