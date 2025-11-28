# 🥛 Produção - Endpoints

**Autenticação:** Requer token JWT

## GET /producao/
**Descrição:** Listar registros de produção

**Query Params:**
- `vaca_id`: Filtrar por vaca
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)
- `skip`: Paginação (default: 0)
- `limit`: Limite (default: 100)

**Response 200:**
```json
[
  {
    "id": 1,
    "vaca_id": 1,
    "data": "2024-01-15",
    "quantidade_manha": 12.5,
    "quantidade_tarde": 13.0,
    "quantidade_total": 25.5,
    "observacoes": "Produção normal",
    "user_id": 1
  }
]
```

---

## POST /producao/
**Descrição:** Registrar produção de leite

**Body:**
```json
{
  "vaca_id": 1,
  "data": "2024-01-15",
  "quantidade_manha": 12.5,
  "quantidade_tarde": 13.0,
  "observacoes": "Produção normal"
}
```

**Response 200:**
```json
{
  "id": 1,
  "vaca_id": 1,
  "data": "2024-01-15",
  "quantidade_manha": 12.5,
  "quantidade_tarde": 13.0,
  "quantidade_total": 25.5,
  "observacoes": "Produção normal",
  "user_id": 1
}
```

**Erros:**
- 404: Vaca não encontrada
- 409: Produção já registrada para esta data

---

## PUT /producao/{id}
**Descrição:** Atualizar registro de produção

**Body:**
```json
{
  "quantidade_manha": 13.0,
  "quantidade_tarde": 14.0,
  "observacoes": "Produção aumentada"
}
```

**Response 200:**
```json
{
  "id": 1,
  "quantidade_manha": 13.0,
  "quantidade_tarde": 14.0,
  "quantidade_total": 27.0,
  "observacoes": "Produção aumentada"
}
```
