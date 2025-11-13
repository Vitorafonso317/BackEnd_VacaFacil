from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.schemas.ml_schemas import (
    PredictionRequest, MLPredictionResult, PerformanceAnalysis,
    AnomalyDetection, RecommendationResult, FinancialForecast
)
from app.services.ml_service import MLService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/ml", tags=["machine-learning"])

@router.post("/predict-production", response_model=MLPredictionResult)
def predict_milk_production(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Prediz produção de leite usando ML"""
    ml_service = MLService(db)
    
    # Verificar se a vaca pertence ao usuário
    from app.models.cattle_model import Vaca
    vaca = db.query(Vaca).filter(
        Vaca.id == request.vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    result = ml_service.predict_milk_production(request.vaca_id, request.days_ahead)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/analyze-performance", response_model=PerformanceAnalysis)
def analyze_cattle_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Análise de performance do rebanho com ML"""
    ml_service = MLService(db)
    result = ml_service.analyze_cattle_performance(current_user.id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/detect-anomalies", response_model=AnomalyDetection)
def detect_production_anomalies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Detecta anomalias na produção usando ML"""
    ml_service = MLService(db)
    result = ml_service.detect_anomalies(current_user.id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/recommendations", response_model=RecommendationResult)
def get_smart_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recomendações inteligentes baseadas em ML"""
    ml_service = MLService(db)
    result = ml_service.recommend_actions(current_user.id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/financial-forecast", response_model=FinancialForecast)
def get_financial_forecast(
    price_per_liter: float = Query(2.50, description="Preço por litro de leite"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Previsão financeira baseada na produção"""
    ml_service = MLService(db)
    result = ml_service.financial_forecast(current_user.id, price_per_liter)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/insights")
def get_ml_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dashboard com insights de ML"""
    ml_service = MLService(db)
    
    # Combinar várias análises
    performance = ml_service.analyze_cattle_performance(current_user.id)
    recommendations = ml_service.recommend_actions(current_user.id)
    forecast = ml_service.financial_forecast(current_user.id)
    
    return {
        "performance": performance if "error" not in performance else None,
        "recommendations": recommendations if "error" not in recommendations else None,
        "forecast": forecast if "error" not in forecast else None,
        "status": "success"
    }