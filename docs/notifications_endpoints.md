# 🔔 Notificações - Endpoints

**Autenticação:** Requer token JWT

## POST /notifications/send
**Descrição:** Enviar notificação para um usuário

**Body:**
```json
{
  "user_id": 1,
  "title": "Nova Produção",
  "message": "Produção registrada com sucesso",
  "type": "success"
}
```

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Nova Produção",
  "message": "Produção registrada com sucesso",
  "type": "success",
  "read": false,
  "created_at": "2024-01-15T10:00:00"
}
```

---

## GET /notifications/
**Descrição:** Listar notificações do usuário

**Query Params:**
- `skip`: Paginação (default: 0)
- `limit`: Limite (default: 50)
- `unread_only`: Apenas não lidas (default: false)

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Nova Produção",
    "message": "Produção registrada com sucesso",
    "type": "success",
    "read": false,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

## PUT /notifications/{id}
**Descrição:** Marcar notificação como lida

**Body:**
```json
{
  "read": true
}
```

**Response 200:**
```json
{
  "id": 1,
  "read": true
}
```

---

## PUT /notifications/mark-all-read
**Descrição:** Marcar todas as notificações como lidas

**Response 200:**
```json
{
  "message": "Todas as notificações marcadas como lidas"
}
```

---

## DELETE /notifications/{id}
**Descrição:** Deletar notificação

**Response 200:**
```json
{
  "message": "Notificação deletada"
}
```

---

## GET /notifications/unread/count
**Descrição:** Contar notificações não lidas

**Response 200:**
```json
{
  "unread_count": 5
}
```
