# 📚 Documentação da API VacaFácil

## Índice de Endpoints

### 🔐 Autenticação
- [auth_endpoints.md](auth_endpoints.md) - 2 endpoints
  - POST /auth/register
  - POST /auth/login

### 👤 Usuários
- [user_endpoints.md](user_endpoints.md) - 3 endpoints
  - GET /users/me
  - PUT /users/me
  - DELETE /users/me

### 🐄 Vacas
- [cattle_endpoints.md](cattle_endpoints.md) - 5 endpoints
  - GET /vacas/
  - POST /vacas/
  - GET /vacas/{id}
  - PUT /vacas/{id}
  - DELETE /vacas/{id}

### 🥛 Produção
- [production_endpoints.md](production_endpoints.md) - 3 endpoints
  - GET /producao/
  - POST /producao/
  - PUT /producao/{id}

### 💰 Financeiro
- [financial_endpoints.md](financial_endpoints.md) - 4 endpoints
  - POST /financeiro/receitas
  - GET /financeiro/receitas
  - POST /financeiro/despesas
  - GET /financeiro/despesas

### 🔔 Notificações
- [notifications_endpoints.md](notifications_endpoints.md) - 6 endpoints
  - POST /notifications/send
  - GET /notifications/
  - PUT /notifications/{id}
  - PUT /notifications/mark-all-read
  - DELETE /notifications/{id}
  - GET /notifications/unread/count

### 📊 Relatórios
- [reports_endpoints.md](reports_endpoints.md) - 3 endpoints
  - GET /relatorios/producao/json
  - GET /relatorios/financeiro/json
  - GET /relatorios/completo/json

### 🤖 Machine Learning
- [ml_endpoints.md](ml_endpoints.md) - 6 endpoints
  - POST /ml/predict-production
  - GET /ml/analyze-performance
  - GET /ml/detect-anomalies
  - GET /ml/recommendations
  - GET /ml/financial-forecast
  - GET /ml/insights

## Total de Endpoints: 32+

## Autenticação

Todos os endpoints (exceto `/auth/register` e `/auth/login`) requerem autenticação JWT.

**Header:**
```
Authorization: Bearer {seu_token}
```

## Base URL

**Desenvolvimento:** http://localhost:5000
**Produção:** https://seu-app.onrender.com

## Documentação Interativa

- **Swagger UI:** http://localhost:5000/docs
- **ReDoc:** http://localhost:5000/redoc
