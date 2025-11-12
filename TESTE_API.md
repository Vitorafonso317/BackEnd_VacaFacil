# 🧪 Guia de Testes - VacaFácil API

## 🚀 Iniciar o Servidor

```bash
.\run.bat
```

Ou:

```bash
venv\Scripts\uvicorn app.main:app --reload
```

Servidor rodando em: **http://localhost:8000**

---

## 📦 Importar Collection no Insomnia

1. Abra o Insomnia
2. Clique em **Import/Export** > **Import Data** > **From File**
3. Selecione o arquivo `insomnia_collection.json`
4. Pronto! Todas as rotas estarão disponíveis

---

## 🔥 Testes Manuais (Sem Banco de Dados)

### 1️⃣ Health Check

**GET** `http://localhost:8000/health`

**Resposta esperada:**
```json
{
  "status": "healthy"
}
```

---

### 2️⃣ Listar Planos de Assinatura

**GET** `http://localhost:8000/subscriptions/plans`

**Resposta esperada:**
```json
{
  "free": {
    "name": "Gratuito",
    "price": 0,
    "max_vacas": 5,
    "features": {...}
  },
  "basic": {...},
  "pro": {...}
}
```

---

### 3️⃣ Documentação Interativa

Acesse: **http://localhost:8000/docs**

Aqui você pode testar todas as rotas diretamente pelo navegador!

---

## 🗄️ Testes com Banco de Dados

### Pré-requisitos:
1. PostgreSQL instalado
2. Banco `vacafacil` criado
3. Arquivo `.env` configurado
4. Executar: `venv\Scripts\python create_tables.py`

---

### 1️⃣ Registrar Usuário

**POST** `http://localhost:8000/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "fazendeiro@example.com",
  "nome": "João Silva",
  "telefone": "11999999999",
  "fazenda": "Fazenda Boa Vista",
  "password": "senha123"
}
```

**Resposta esperada (200):**
```json
{
  "id": 1,
  "email": "fazendeiro@example.com",
  "nome": "João Silva",
  "telefone": "11999999999",
  "fazenda": "Fazenda Boa Vista",
  "is_active": true,
  "foto_perfil": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 2️⃣ Login

**POST** `http://localhost:8000/auth/login`

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```

**Body (form-data):**
```
username: fazendeiro@example.com
password: senha123
```

**Resposta esperada (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

⚠️ **IMPORTANTE:** Copie o `access_token` para usar nas próximas requisições!

---

### 3️⃣ Criar Vaca

**POST** `http://localhost:8000/vacas/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer SEU_TOKEN_AQUI
```

**Body:**
```json
{
  "nome": "Mimosa",
  "raca": "Holandesa",
  "idade": 3,
  "peso": 550.5,
  "producao_media": 25.5,
  "status": "ativa",
  "observacoes": "Vaca saudável e produtiva"
}
```

**Resposta esperada (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "nome": "Mimosa",
  "raca": "Holandesa",
  "idade": 3,
  "peso": 550.5,
  "producao_media": 25.5,
  "status": "ativa",
  "observacoes": "Vaca saudável e produtiva",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": null
}
```

---

### 4️⃣ Listar Vacas

**GET** `http://localhost:8000/vacas/`

**Headers:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

**Query Params (opcionais):**
- `skip=0` - Paginação
- `limit=100` - Limite de resultados
- `search=Mimosa` - Buscar por nome
- `raca=Holandesa` - Filtrar por raça
- `status=ativa` - Filtrar por status

**Resposta esperada (200):**
```json
[
  {
    "id": 1,
    "nome": "Mimosa",
    "raca": "Holandesa",
    ...
  }
]
```

---

### 5️⃣ Buscar Vaca por ID

**GET** `http://localhost:8000/vacas/1`

**Headers:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

---

### 6️⃣ Atualizar Vaca

**PUT** `http://localhost:8000/vacas/1`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer SEU_TOKEN_AQUI
```

**Body:**
```json
{
  "peso": 560.0,
  "producao_media": 26.0
}
```

---

### 7️⃣ Deletar Vaca

**DELETE** `http://localhost:8000/vacas/1`

**Headers:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

**Resposta esperada (200):**
```json
{
  "message": "Vaca deleted successfully"
}
```

---

### 8️⃣ Criar Assinatura

**POST** `http://localhost:8000/subscriptions/subscribe`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer SEU_TOKEN_AQUI
```

**Body:**
```json
{
  "plan_type": "basic",
  "payment_method": "credit_card"
}
```

---

### 9️⃣ Status da Assinatura

**GET** `http://localhost:8000/subscriptions/status`

**Headers:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

---

## 🎯 Fluxo Completo de Teste

1. ✅ Health Check
2. ✅ Listar Planos
3. ✅ Registrar Usuário
4. ✅ Login (copiar token)
5. ✅ Criar Assinatura
6. ✅ Criar Vaca
7. ✅ Listar Vacas
8. ✅ Atualizar Vaca
9. ✅ Buscar Vaca por ID
10. ✅ Deletar Vaca

---

## 🐛 Erros Comuns

### 401 Unauthorized
- Token expirado ou inválido
- Faça login novamente

### 404 Not Found
- Recurso não existe
- Verifique o ID

### 422 Unprocessable Entity
- Dados inválidos no body
- Verifique o formato JSON

### 500 Internal Server Error
- Banco de dados não configurado
- Verifique conexão PostgreSQL

---

## 📚 Documentação Completa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
