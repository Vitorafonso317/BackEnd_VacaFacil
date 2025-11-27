# 👤 Usuários - Endpoints

**Autenticação:** Todos os endpoints requerem token JWT no header `Authorization: Bearer {token}`

## GET /users/me
**Descrição:** Obter dados do usuário logado

**Response 200:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nome": "Nome do Usuário",
  "telefone": "11999999999",
  "fazenda": "Fazenda Exemplo",
  "foto_perfil": null,
  "created_at": "2024-01-01T00:00:00"
}
```

---

## PUT /users/me
**Descrição:** Atualizar dados do usuário logado

**Body:**
```json
{
  "nome": "Novo Nome",
  "telefone": "11988888888",
  "fazenda": "Nova Fazenda"
}
```

**Response 200:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nome": "Novo Nome",
  "telefone": "11988888888",
  "fazenda": "Nova Fazenda"
}
```

---

## DELETE /users/me
**Descrição:** Deletar conta do usuário

**Response 200:**
```json
{
  "message": "Usuário deletado com sucesso"
}
```
