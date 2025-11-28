# 🐄 Vacas - Endpoints

**Autenticação:** Requer token JWT

## GET /vacas/
**Descrição:** Listar todas as vacas do usuário

**Query Params:**
- `skip`: Paginação (default: 0)
- `limit`: Limite de resultados (default: 100)

**Response 200:**
```json
[
  {
    "id": 1,
    "nome": "Mimosa",
    "raca": "Holandesa",
    "data_nascimento": "2020-01-15",
    "numero_identificacao": "BR123456",
    "ativa": true,
    "user_id": 1
  }
]
```

---

## POST /vacas/
**Descrição:** Cadastrar nova vaca

**Body:**
```json
{
  "nome": "Mimosa",
  "raca": "Holandesa",
  "data_nascimento": "2020-01-15",
  "numero_identificacao": "BR123456"
}
```

**Response 200:**
```json
{
  "id": 1,
  "nome": "Mimosa",
  "raca": "Holandesa",
  "data_nascimento": "2020-01-15",
  "numero_identificacao": "BR123456",
  "ativa": true,
  "user_id": 1
}
```

---

## GET /vacas/{id}
**Descrição:** Obter detalhes de uma vaca específica

**Response 200:**
```json
{
  "id": 1,
  "nome": "Mimosa",
  "raca": "Holandesa",
  "data_nascimento": "2020-01-15",
  "numero_identificacao": "BR123456",
  "ativa": true,
  "user_id": 1
}
```

**Erros:**
- 404: Vaca não encontrada

---

## PUT /vacas/{id}
**Descrição:** Atualizar dados da vaca

**Body:**
```json
{
  "nome": "Mimosa Atualizada",
  "ativa": false
}
```

**Response 200:**
```json
{
  "id": 1,
  "nome": "Mimosa Atualizada",
  "ativa": false
}
```

---

## DELETE /vacas/{id}
**Descrição:** Remover vaca

**Response 200:**
```json
{
  "message": "Vaca removida com sucesso"
}
```
