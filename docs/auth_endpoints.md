# 🔐 Autenticação - Endpoints

## POST /auth/register
**Descrição:** Registrar novo usuário no sistema

**Body:**
```json
{
  "email": "usuario@example.com",
  "nome": "Nome do Usuário",
  "password": "senha123",
  "telefone": "11999999999",
  "fazenda": "Fazenda Exemplo"
}
```

**Response 200:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "nome": "Nome do Usuário",
  "telefone": "11999999999",
  "fazenda": "Fazenda Exemplo"
}
```

**Erros:**
- 409: Email já cadastrado

---

## POST /auth/login
**Descrição:** Fazer login e obter token JWT

**Body (form-data):**
```
username: usuario@example.com
password: senha123
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Erros:**
- 401: Email ou senha incorretos
