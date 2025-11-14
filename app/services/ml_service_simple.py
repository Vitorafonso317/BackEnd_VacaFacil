"""
Versão simplificada do ML Service sem dependências pesadas
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.cattle_model import Vaca
from app.models.production_model import Producao

class MLServiceSimple:
    def __init__(self, db: Session):
        self.db = db
    
    def predict_milk_production_simple(self, vaca_id: int, days_ahead: int = 7):
        """Predição simples baseada em média móvel"""
        
        # Buscar últimas produções
        producoes = self.db.query(Producao).filter(
            Producao.vaca_id == vaca_id
        ).order_by(Producao.data.desc()).limit(7).all()
        
        if len(producoes) < 3:
            return {"error": "Dados insuficientes"}
        
        # Calcular média simples
        media = sum(p.quantidade_total for p in producoes) / len(producoes)
        
        # Gerar predições
        predictions = []
        for i in range(days_ahead):
            future_date = datetime.now().date() + timedelta(days=i+1)
            # Variação simples baseada no dia da semana
            variation = 1.0 + (future_date.weekday() % 3 - 1) * 0.1
            pred_value = media * variation
            
            predictions.append({
                'data': future_date.isoformat(),
                'producao_prevista': round(max(0, pred_value), 2)
            })
        
        return {
            'vaca_id': vaca_id,
            'predicoes': predictions,
            'confiabilidade': min(0.8, len(producoes) / 7),
            'metodo': 'media_movel_simples'
        }
    
    def analyze_performance_simple(self, user_id: int):
        """Análise simples de performance"""
        
        vacas = self.db.query(Vaca).filter(Vaca.user_id == user_id).all()
        
        if not vacas:
            return {"error": "Nenhuma vaca encontrada"}
        
        results = []
        
        for vaca in vacas:
            producoes = self.db.query(Producao).filter(
                Producao.vaca_id == vaca.id
            ).all()
            
            if len(producoes) < 2:
                continue
            
            # Métricas simples
            total = sum(p.quantidade_total for p in producoes)
            media = total / len(producoes)
            
            # Classificação simples
            if media > 20:
                performance = "excelente"
            elif media > 15:
                performance = "boa"
            elif media > 10:
                performance = "regular"
            else:
                performance = "baixa"
            
            results.append({
                'vaca_id': vaca.id,
                'nome': vaca.nome,
                'media_producao': round(media, 2),
                'total_producao': round(total, 2),
                'performance': performance,
                'dias_analisados': len(producoes)
            })
        
        return {
            'total_vacas': len(results),
            'media_geral': round(sum(r['media_producao'] for r in results) / len(results), 2) if results else 0,
            'vacas': results,
            'metodo': 'analise_simples'
        }
    
    def get_recommendations_simple(self, user_id: int):
        """Recomendações simples baseadas em regras"""
        
        performance = self.analyze_performance_simple(user_id)
        
        if 'error' in performance:
            return performance
        
        recommendations = []
        
        for vaca in performance['vacas']:
            if vaca['performance'] == 'baixa':
                recommendations.append({
                    'tipo': 'alerta',
                    'vaca': vaca['nome'],
                    'recomendacao': 'Produção baixa - verificar alimentação e saúde',
                    'prioridade': 'alta'
                })
        
        if performance['media_geral'] < 15:
            recommendations.append({
                'tipo': 'geral',
                'recomendacao': 'Média do rebanho abaixo do ideal - revisar manejo',
                'prioridade': 'média'
            })
        
        return {
            'total_recomendacoes': len(recommendations),
            'recomendacoes': recommendations,
            'metodo': 'regras_simples'
        }