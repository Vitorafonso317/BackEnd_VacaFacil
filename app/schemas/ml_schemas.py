from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PredictionRequest(BaseModel):
    vaca_id: int
    days_ahead: int = 7

class PredictionResponse(BaseModel):
    data: str
    producao_prevista: float

class MLPredictionResult(BaseModel):
    vaca_id: int
    predicoes: List[PredictionResponse]
    confiabilidade: float

class CattlePerformance(BaseModel):
    vaca_id: int
    nome: str
    media_producao: float
    total_producao: float
    tendencia: str
    performance: str
    dias_analisados: int

class PerformanceAnalysis(BaseModel):
    total_vacas: int
    media_geral: float
    vacas: List[CattlePerformance]

class Anomaly(BaseModel):
    data: str
    vaca_id: int
    producao: float
    desvio: float
    tipo: str

class AnomalyDetection(BaseModel):
    total_anomalias: int
    media_producao: float
    desvio_padrao: float
    anomalias: List[Anomaly]

class Recommendation(BaseModel):
    tipo: str
    vaca: Optional[str] = None
    recomendacao: str
    prioridade: str

class RecommendationResult(BaseModel):
    total_recomendacoes: int
    recomendacoes: List[Recommendation]

class FinancialProjection(BaseModel):
    producao: float
    receita: float

class FinancialForecast(BaseModel):
    producao_media_diaria: float
    receita_media_diaria: float
    preco_litro: float
    projecoes: dict