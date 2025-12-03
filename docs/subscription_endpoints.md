# 💳 Assinaturas - Endpoints

**Autenticação:** Requer token JWT

## GET /subscriptions/plans
**Descrição:** Listar planos disponíveis

**Response 200:**
```json
[
  {
    "name": "FREE",
    "price": 0.00,
    "max_cattle": 5,
    "features": [
      "5 vacas",
      "Histórico 30 dias",
      "Relatórios básicos"
    ]
  },
  {
    "name": "BASIC",
    "price": 29.90,
    "max_cattle": 50,
    "features": [
      "50 vacas",
      "Histórico 1 ano",
      "Marketplace",
      "Relatórios completos"
    ]
  },
  {
    "name": "PRO",
    "price": 59.90,
    "max_cattle": null,
    "features": [
      "Vacas ilimitadas",
      "Histórico ilimitado",
      "Machine Learning",
      "Suporte prioritário"
    ]
  }
]
```

---

## POST /subscriptions/subscribe
**Descrição:** Criar ou atualizar assinatura

**Body:**
```json
{
  "plan_type": "BASIC",
  "payment_method": "credit_card"
}
```

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "plan_type": "BASIC",
  "price": 29.90,
  "status": "active",
  "start_date": "2024-01-15",
  "end_date": "2024-02-15"
}
```

---

## GET /subscriptions/status
**Descrição:** Obter status da assinatura atual

**Response 200:**
```json
{
  "id": 1,
  "plan_type": "BASIC",
  "price": 29.90,
  "status": "active",
  "start_date": "2024-01-15",
  "end_date": "2024-02-15",
  "days_remaining": 15,
  "max_cattle": 50
}
```

---

## PUT /subscriptions/upgrade
**Descrição:** Fazer upgrade de plano

**Body:**
```json
{
  "new_plan": "PRO"
}
```

**Response 200:**
```json
{
  "id": 1,
  "plan_type": "PRO",
  "price": 59.90,
  "status": "active",
  "message": "Upgrade realizado com sucesso"
}
```

---

## DELETE /subscriptions/cancel
**Descrição:** Cancelar assinatura

**Response 200:**
```json
{
  "message": "Assinatura cancelada com sucesso",
  "end_date": "2024-02-15",
  "note": "Você ainda tem acesso até o fim do período pago"
}
```

---

## Planos Disponíveis

### FREE (Gratuito)
- 5 vacas
- Histórico 30 dias
- Relatórios básicos

### BASIC (R$ 29,90/mês)
- 50 vacas
- Histórico 1 ano
- Marketplace
- Relatórios completos

### PRO (R$ 59,90/mês)
- Vacas ilimitadas
- Histórico ilimitado
- Machine Learning
- Análises avançadas
- Suporte prioritário
