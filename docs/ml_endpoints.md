# 🤖 Machine Learning - Endpoints

**Autenticação:** Requer token JWT

## POST /ml/predict-production
**Descrição:** Prever produção de leite

**Body:**
```json
{
  "vaca_id": 1,
  "days_ahead": 7
}
```

**Response 200:**
```json
{
  "vaca_id": 1,
  "predicoes": [
    {
      "data": "2024-01-16",
      "producao_prevista": 25.30
    }
  ],
  "confiabilidade": 0.85
}
```

---

## GET /ml/analyze-performance
**Descrição:** Análise de performance do rebanho

**Response 200:**
```json
{
  "total_vacas": 10,
  "media_geral": 23.50,
  "vacas": [
    {
      "vaca_id": 1,
      "nome": "Mimosa",
      "media_producao": 25.50,
      "total_producao": 765.00,
      "tendencia": "crescente",
      "performance": "excelente",
      "dias_analisados": 30
    }
  ]
}
```

---

## GET /ml/detect-anomalies
**Descrição:** Detectar anomalias na produção

**Response 200:**
```json
{
  "total_anomalias": 3,
  "media_producao": 24.50,
  "desvio_padrao": 3.20,
  "anomalias": [
    {
      "data": "2024-01-15",
      "vaca_id": 1,
      "producao": 35.00,
      "desvio": 3.28,
      "tipo": "alta"
    }
  ]
}
```

---

## GET /ml/recommendations
**Descrição:** Recomendações inteligentes

**Response 200:**
```json
{
  "total_recomendacoes": 2,
  "recomendacoes": [
    {
      "tipo": "alerta",
      "vaca": "Mimosa",
      "recomendacao": "Verificar saúde - produção abaixo da média",
      "prioridade": "alta"
    }
  ]
}
```

---

## GET /ml/financial-forecast
**Descrição:** Previsão financeira

**Query Params:**
- `price_per_liter`: Preço por litro (default: 2.50)

**Response 200:**
```json
{
  "producao_media_diaria": 25.00,
  "receita_media_diaria": 62.50,
  "preco_litro": 2.50,
  "projecoes": {
    "semanal": {
      "producao": 175.00,
      "receita": 437.50
    },
    "mensal": {
      "producao": 750.00,
      "receita": 1875.00
    },
    "anual": {
      "producao": 9125.00,
      "receita": 22812.50
    }
  }
}
```

---

## GET /ml/insights
**Descrição:** Dashboard com insights de ML

**Response 200:**
```json
{
  "status": "success",
  "performance": {...},
  "recommendations": {...},
  "forecast": {...}
}
```
