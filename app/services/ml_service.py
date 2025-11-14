import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.cattle_model import Vaca
from app.models.production_model import Producao

class MLService:
    def __init__(self, db: Session):
        self.db = db
        self.models_path = "ml_models"
        os.makedirs(self.models_path, exist_ok=True)
    
    def predict_milk_production(self, vaca_id: int, days_ahead: int = 7):
        """Prediz produção de leite para os próximos dias"""
        try:
            # Buscar dados históricos da vaca
            producoes = self.db.query(Producao).filter(
                Producao.vaca_id == vaca_id
            ).order_by(Producao.data.desc()).limit(30).all()
            
            if len(producoes) < 5:
                return {"error": "Dados insuficientes para predição"}
        except Exception as e:
            return {"error": f"Erro ao buscar dados: {str(e)}"}
        
        # Preparar dados
        df = pd.DataFrame([{
            'quantidade_total': p.quantidade_total,
            'dia_semana': p.data.weekday(),
            'dias_desde_inicio': (datetime.now().date() - p.data).days
        } for p in producoes])
        
        try:
            # Treinar modelo simples
            X = df[['dia_semana', 'dias_desde_inicio']]
            y = df['quantidade_total']
            
            if len(X) == 0 or len(y) == 0:
                return {"error": "Dados insuficientes para treinar modelo"}
            
            model = LinearRegression()
            model.fit(X, y)
        except Exception as e:
            return {"error": f"Erro ao treinar modelo: {str(e)}"}
        
        try:
            # Fazer predições
            predictions = []
            for i in range(min(days_ahead, 30)):  # Limitar a 30 dias
                future_date = datetime.now().date() + timedelta(days=i+1)
                pred_data = [[future_date.weekday(), i+1]]
                pred_value = model.predict(pred_data)[0]
                
                predictions.append({
                    'data': future_date.isoformat(),
                    'producao_prevista': round(max(0, pred_value), 2)
                })
        except Exception as e:
            return {"error": f"Erro ao fazer predições: {str(e)}"}
        
        return {
            'vaca_id': vaca_id,
            'predicoes': predictions,
            'confiabilidade': min(0.95, len(producoes) / 30)
        }
    
    def analyze_cattle_performance(self, user_id: int):
        """Análise de performance do rebanho com ML"""
        try:
            # Buscar vacas do usuário
            vacas = self.db.query(Vaca).filter(Vaca.user_id == user_id).all()
            
            if not vacas:
                return {"error": "Nenhuma vaca encontrada"}
        except Exception as e:
            return {"error": f"Erro ao buscar vacas: {str(e)}"}
        
        results = []
        
        for vaca in vacas:
            try:
                # Buscar produções da vaca
                producoes = self.db.query(Producao).filter(
                    Producao.vaca_id == vaca.id
                ).all()
            except Exception:
                continue  # Pular vaca com erro
            
            if len(producoes) < 3:
                continue
            
            # Calcular métricas
            total_producao = sum(p.quantidade_total for p in producoes)
            media_producao = total_producao / len(producoes)
            
            # Tendência (regressão linear simples)
            dias = [(p.data - producoes[0].data).days for p in producoes]
            producao_values = [p.quantidade_total for p in producoes]
            
            if len(dias) > 1:
                coef = np.polyfit(dias, producao_values, 1)[0]
                tendencia = "crescente" if coef > 0.1 else "decrescente" if coef < -0.1 else "estável"
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
        
        # Ordenar por performance
        results.sort(key=lambda x: x['media_producao'], reverse=True)
        
        return {
            'total_vacas': len(results),
            'media_geral': round(sum(r['media_producao'] for r in results) / len(results), 2) if results else 0,
            'vacas': results
        }
    
    def detect_anomalies(self, user_id: int):
        """Detecta anomalias na produção usando ML"""
        try:
            # Buscar todas as produções do usuário
            producoes = self.db.query(Producao).filter(
                Producao.user_id == user_id
            ).order_by(Producao.data.desc()).limit(100).all()
            
            if len(producoes) < 10:
                return {"error": "Dados insuficientes para análise de anomalias"}
        except Exception as e:
            return {"error": f"Erro ao buscar produções: {str(e)}"}
        
        # Preparar dados
        values = [p.quantidade_total for p in producoes]
        
        # Calcular estatísticas
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        # Detectar outliers (valores fora de 2 desvios padrão)
        anomalies = []
        
        for p in producoes:
            if std_val > 0:
                z_score = abs(p.quantidade_total - mean_val) / std_val
            else:
                z_score = 0
            
            if z_score > 2:  # Anomalia
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
            'anomalias': anomalies[:10]  # Últimas 10 anomalias
        }
    
    def recommend_actions(self, user_id: int):
        """Recomendações inteligentes baseadas em ML"""
        
        # Análise de performance
        performance = self.analyze_cattle_performance(user_id)
        
        if 'error' in performance:
            return performance
        
        recommendations = []
        
        # Recomendações baseadas na performance
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
        
        # Recomendações gerais
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
        return {"error": f"Erro ao gerar recomendações: {str(e)}"}
    
    def financial_forecast(self, user_id: int, price_per_liter: float = 2.50):
        """Previsão financeira baseada na produção"""
        try:
            # Buscar produções recentes
            producoes = self.db.query(Producao).filter(
                Producao.user_id == user_id
            ).order_by(Producao.data.desc()).limit(30).all()
            
            if len(producoes) < 7:
                return {"error": "Dados insuficientes para previsão financeira"}
        except Exception as e:
            return {"error": f"Erro ao buscar dados: {str(e)}"}
        
        # Calcular médias
        producao_diaria = sum(p.quantidade_total for p in producoes) / len(producoes)
        receita_diaria = producao_diaria * price_per_liter
        
        # Projeções
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