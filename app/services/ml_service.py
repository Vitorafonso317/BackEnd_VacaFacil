"""
ML Service - Versão otimizada sem dependências pesadas
Usa apenas Python puro e matemática básica
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.cattle_model import Vaca
from app.models.production_model import Producao
import statistics

class MLService:
    def __init__(self, db: Session):
        self.db = db
    
    def predict_milk_production(self, vaca_id: int, days_ahead: int = 7):
        """Prediz produção de leite usando regressão linear simples"""
        try:
            producoes = self.db.query(Producao).filter(
                Producao.vaca_id == vaca_id
            ).order_by(Producao.data.desc()).limit(30).all()
            
            if len(producoes) < 5:
                return {"error": "Dados insuficientes para predição"}
            
            # Preparar dados para regressão linear
            base_date = producoes[-1].data
            x_values = [(p.data - base_date).days for p in producoes]
            y_values = [p.quantidade_total for p in producoes]
            
            # Calcular regressão linear manualmente
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            sum_x2 = sum(x * x for x in x_values)
            
            # Coeficientes da reta y = a + bx
            b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            a = (sum_y - b * sum_x) / n
            
            # Fazer predições
            predictions = []
            last_day = max(x_values)
            
            for i in range(min(days_ahead, 30)):
                future_day = last_day + i + 1
                pred_value = a + b * future_day
                future_date = base_date + timedelta(days=future_day)
                
                predictions.append({
                    'data': future_date.isoformat(),
                    'producao_prevista': round(max(0, pred_value), 2)
                })
            
            return {
                'vaca_id': vaca_id,
                'predicoes': predictions,
                'confiabilidade': min(0.95, len(producoes) / 30)
            }
        except Exception as e:
            return {"error": f"Erro na predição: {str(e)}"}
    
    def analyze_cattle_performance(self, user_id: int):
        """Análise de performance do rebanho"""
        try:
            vacas = self.db.query(Vaca).filter(Vaca.user_id == user_id).all()
            
            if not vacas:
                return {"error": "Nenhuma vaca encontrada"}
            
            results = []
            
            for vaca in vacas:
                producoes = self.db.query(Producao).filter(
                    Producao.vaca_id == vaca.id
                ).all()
                
                if len(producoes) < 3:
                    continue
                
                # Calcular métricas
                total_producao = sum(p.quantidade_total for p in producoes)
                media_producao = total_producao / len(producoes)
                
                # Calcular tendência (regressão linear simples)
                if len(producoes) > 1:
                    base_date = producoes[0].data
                    x_values = [(p.data - base_date).days for p in producoes]
                    y_values = [p.quantidade_total for p in producoes]
                    
                    n = len(x_values)
                    sum_x = sum(x_values)
                    sum_y = sum(y_values)
                    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
                    sum_x2 = sum(x * x for x in x_values)
                    
                    if n * sum_x2 - sum_x * sum_x != 0:
                        coef = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                        tendencia = "crescente" if coef > 0.1 else "decrescente" if coef < -0.1 else "estável"
                    else:
                        tendencia = "estável"
                else:
                    tendencia = "estável"
                
                # Classificação de performance
                if media_producao > 20:
                    performance = "excelente"
                elif media_producao > 15:
                    performance = "boa"
                elif media_producao > 10:
                    performance = "regular"
                else:
                    performance = "baixa"
                
                results.append({
                    'vaca_id': vaca.id,
                    'nome': vaca.nome,
                    'media_producao': round(media_producao, 2),
                    'total_producao': round(total_producao, 2),
                    'tendencia': tendencia,
                    'performance': performance,
                    'dias_analisados': len(producoes)
                })
            
            results.sort(key=lambda x: x['media_producao'], reverse=True)
            
            return {
                'total_vacas': len(results),
                'media_geral': round(sum(r['media_producao'] for r in results) / len(results), 2) if results else 0,
                'vacas': results
            }
        except Exception as e:
            return {"error": f"Erro na análise: {str(e)}"}
    
    def detect_anomalies(self, user_id: int):
        """Detecta anomalias na produção"""
        try:
            producoes = self.db.query(Producao).filter(
                Producao.user_id == user_id
            ).order_by(Producao.data.desc()).limit(100).all()
            
            if len(producoes) < 10:
                return {"error": "Dados insuficientes para análise de anomalias"}
            
            values = [p.quantidade_total for p in producoes]
            
            # Calcular média e desvio padrão manualmente
            mean_val = statistics.mean(values)
            std_val = statistics.stdev(values) if len(values) > 1 else 0
            
            # Detectar outliers (valores fora de 2 desvios padrão)
            anomalies = []
            
            for p in producoes:
                if std_val > 0:
                    z_score = abs(p.quantidade_total - mean_val) / std_val
                else:
                    z_score = 0
                
                if z_score > 2:
                    anomalies.append({
                        'data': p.data.isoformat(),
                        'vaca_id': p.vaca_id,
                        'producao': p.quantidade_total,
                        'desvio': round(z_score, 2),
                        'tipo': 'alta' if p.quantidade_total > mean_val else 'baixa'
                    })
            
            return {
                'total_anomalias': len(anomalies),
                'media_producao': round(mean_val, 2),
                'desvio_padrao': round(std_val, 2),
                'anomalias': anomalies[:10]
            }
        except Exception as e:
            return {"error": f"Erro na detecção: {str(e)}"}
    
    def recommend_actions(self, user_id: int):
        """Recomendações inteligentes"""
        try:
            performance = self.analyze_cattle_performance(user_id)
            
            if 'error' in performance:
                return performance
            
            recommendations = []
            
            for vaca in performance['vacas']:
                if vaca['performance'] == 'baixa':
                    recommendations.append({
                        'tipo': 'alerta',
                        'vaca': vaca['nome'],
                        'recomendacao': 'Verificar saúde e alimentação - produção abaixo da média',
                        'prioridade': 'alta'
                    })
                
                if vaca['tendencia'] == 'decrescente':
                    recommendations.append({
                        'tipo': 'atenção',
                        'vaca': vaca['nome'],
                        'recomendacao': 'Produção em declínio - avaliar condições',
                        'prioridade': 'média'
                    })
            
            if performance['media_geral'] < 15:
                recommendations.append({
                    'tipo': 'geral',
                    'recomendacao': 'Média do rebanho baixa - revisar manejo nutricional',
                    'prioridade': 'alta'
                })
            
            return {
                'total_recomendacoes': len(recommendations),
                'recomendacoes': recommendations
            }
        except Exception as e:
            return {"error": f"Erro nas recomendações: {str(e)}"}
    
    def financial_forecast(self, user_id: int, price_per_liter: float = 2.50):
        """Previsão financeira"""
        try:
            producoes = self.db.query(Producao).filter(
                Producao.user_id == user_id
            ).order_by(Producao.data.desc()).limit(30).all()
            
            if len(producoes) < 7:
                return {"error": "Dados insuficientes para previsão financeira"}
            
            producao_diaria = sum(p.quantidade_total for p in producoes) / len(producoes)
            receita_diaria = producao_diaria * price_per_liter
            
            projecoes = {
                'semanal': {
                    'producao': round(producao_diaria * 7, 2),
                    'receita': round(receita_diaria * 7, 2)
                },
                'mensal': {
                    'producao': round(producao_diaria * 30, 2),
                    'receita': round(receita_diaria * 30, 2)
                },
                'anual': {
                    'producao': round(producao_diaria * 365, 2),
                    'receita': round(receita_diaria * 365, 2)
                }
            }
            
            return {
                'producao_media_diaria': round(producao_diaria, 2),
                'receita_media_diaria': round(receita_diaria, 2),
                'preco_litro': price_per_liter,
                'projecoes': projecoes
            }
        except Exception as e:
            return {"error": f"Erro na previsão: {str(e)}"}
