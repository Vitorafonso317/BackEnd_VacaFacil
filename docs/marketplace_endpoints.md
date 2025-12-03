# 🛒 Marketplace - Endpoints

**Autenticação:** Requer token JWT

## GET /marketplace/
**Descrição:** Listar anúncios do marketplace

**Query Params:**
- `categoria`: Filtrar por categoria (vaca, equipamento, insumo)
- `skip`: Paginação (default: 0)
- `limit`: Limite (default: 100)

**Response 200:**
```json
[
  {
    "id": 1,
    "titulo": "Vaca Holandesa de Alta Produção",
    "descricao": "Excelente produtora, 25L/dia",
    "categoria": "vaca",
    "preco": 8000.00,
    "localizacao": "São Paulo",
    "telefone": "11999999999",
    "ativo": true,
    "user_id": 1,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

## POST /marketplace/
**Descrição:** Criar anúncio no marketplace

**Body:**
```json
{
  "titulo": "Vaca Holandesa de Alta Produção",
  "descricao": "Excelente produtora, 25L/dia",
  "categoria": "vaca",
  "preco": 8000.00,
  "localizacao": "São Paulo",
  "telefone": "11999999999"
}
```

**Response 200:**
```json
{
  "id": 1,
  "titulo": "Vaca Holandesa de Alta Produção",
  "descricao": "Excelente produtora, 25L/dia",
  "categoria": "vaca",
  "preco": 8000.00,
  "localizacao": "São Paulo",
  "telefone": "11999999999",
  "ativo": true,
  "user_id": 1,
  "created_at": "2024-01-15T10:00:00"
}
```

---

## GET /marketplace/{id}
**Descrição:** Obter detalhes de um anúncio

**Response 200:**
```json
{
  "id": 1,
  "titulo": "Vaca Holandesa de Alta Produção",
  "descricao": "Excelente produtora, 25L/dia",
  "categoria": "vaca",
  "preco": 8000.00,
  "localizacao": "São Paulo",
  "telefone": "11999999999",
  "ativo": true,
  "user_id": 1
}
```

**Erros:**
- 404: Anúncio não encontrado

---

## PUT /marketplace/{id}
**Descrição:** Atualizar anúncio

**Body:**
```json
{
  "titulo": "Vaca Holandesa - Preço Atualizado",
  "preco": 7500.00,
  "ativo": true
}
```

**Response 200:**
```json
{
  "id": 1,
  "titulo": "Vaca Holandesa - Preço Atualizado",
  "preco": 7500.00,
  "ativo": true
}
```

---

## DELETE /marketplace/{id}
**Descrição:** Remover anúncio

**Response 200:**
```json
{
  "message": "Anúncio removido com sucesso"
}
```

**Categorias disponíveis:**
- `vaca` - Animais
- `equipamento` - Equipamentos
- `insumo` - Insumos e ração
