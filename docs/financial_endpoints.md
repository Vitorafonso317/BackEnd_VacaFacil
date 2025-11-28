# 💰 Financeiro - Endpoints

**Autenticação:** Requer token JWT

## POST /financeiro/receitas
**Descrição:** Registrar receita

**Body:**
```json
{
  "categoria": "venda_leite",
  "valor": 1500.00,
  "data": "2024-01-15",
  "descricao": "Venda de leite"
}
```

**Response 200:**
```json
{
  "id": 1,
  "categoria": "venda_leite",
  "valor": 1500.00,
  "data": "2024-01-15",
  "descricao": "Venda de leite",
  "user_id": 1
}
```

---

## GET /financeiro/receitas
**Descrição:** Listar receitas

**Query Params:**
- `data_inicio`: Data inicial
- `data_fim`: Data final
- `categoria`: Filtrar por categoria

**Response 200:**
```json
[
  {
    "id": 1,
    "categoria": "venda_leite",
    "valor": 1500.00,
    "data": "2024-01-15",
    "descricao": "Venda de leite"
  }
]
```

---

## POST /financeiro/despesas
**Descrição:** Registrar despesa

**Body:**
```json
{
  "categoria": "racao",
  "valor": 500.00,
  "data": "2024-01-15",
  "descricao": "Compra de ração"
}
```

**Response 200:**
```json
{
  "id": 1,
  "categoria": "racao",
  "valor": 500.00,
  "data": "2024-01-15",
  "descricao": "Compra de ração",
  "user_id": 1
}
```

---

## GET /financeiro/despesas
**Descrição:** Listar despesas

**Query Params:**
- `data_inicio`: Data inicial
- `data_fim`: Data final
- `categoria`: Filtrar por categoria

**Response 200:**
```json
[
  {
    "id": 1,
    "categoria": "racao",
    "valor": 500.00,
    "data": "2024-01-15",
    "descricao": "Compra de ração"
  }
]
```
