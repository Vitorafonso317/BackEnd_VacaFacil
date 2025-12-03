# 🐮 Reprodução - Endpoints

**Autenticação:** Requer token JWT

## GET /reproducao/
**Descrição:** Listar eventos de reprodução

**Query Params:**
- `vaca_id`: Filtrar por vaca
- `skip`: Paginação (default: 0)
- `limit`: Limite (default: 100)

**Response 200:**
```json
[
  {
    "id": 1,
    "vaca_id": 1,
    "tipo": "inseminacao",
    "data": "2024-01-15",
    "data_prevista_parto": "2024-10-15",
    "sucesso": true,
    "observacoes": "Inseminação artificial",
    "user_id": 1,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

## POST /reproducao/
**Descrição:** Registrar evento de reprodução

**Body:**
```json
{
  "vaca_id": 1,
  "tipo": "inseminacao",
  "data": "2024-01-15",
  "data_prevista_parto": "2024-10-15",
  "sucesso": true,
  "observacoes": "Inseminação artificial"
}
```

**Response 200:**
```json
{
  "id": 1,
  "vaca_id": 1,
  "tipo": "inseminacao",
  "data": "2024-01-15",
  "data_prevista_parto": "2024-10-15",
  "sucesso": true,
  "observacoes": "Inseminação artificial",
  "user_id": 1,
  "created_at": "2024-01-15T10:00:00"
}
```

**Tipos de eventos:**
- `inseminacao` - Inseminação artificial
- `cobertura` - Cobertura natural
- `parto` - Nascimento

**Erros:**
- 404: Vaca não encontrada
