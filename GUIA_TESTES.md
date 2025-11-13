# 🧪 Guia de Testes - VacaFácil API

## 🚀 Iniciar Servidor

```bash
# Opção 1: Script automático
start_server.bat

# Opção 2: Python direto
python test_server.py

# Opção 3: Uvicorn
uvicorn app.main:app --reload --port 8000
```

**Acesse**: http://localhost:8000/docs

## 📋 Sequência de Testes

### 1. 🔐 **Autenticação**

#### Registrar Usuário
```http
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "teste@vacafacil.com",
  "nome": "João Fazendeiro",
  "telefone": "(11) 99999-9999",
  "fazenda": "Fazenda Teste",
  "password": "senha123"
}
```

#### Login
```http
POST http://localhost:8000/auth/login
Content-Type: application/x-www-form-urlencoded

username=teste@vacafacil.com&password=senha123
```

**Copie o `access_token` retornado!**

### 2. 👤 **Perfil do Usuário**

#### Ver Perfil
```http
GET http://localhost:8000/users/me
Authorization: Bearer SEU_TOKEN_AQUI
```

#### Atualizar Perfil
```http
PUT http://localhost:8000/users/me
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "nome": "João Silva Fazendeiro",
  "telefone": "(11) 88888-8888"
}
```

### 3. 🐄 **Gestão de Vacas**

#### Criar Vaca
```http
POST http://localhost:8000/vacas/
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "nome": "Mimosa",
  "raca": "Holandesa",
  "idade": 3,
  "peso": 550.5,
  "producao_media": 25.0,
  "status": "ativa",
  "observacoes": "Vaca muito produtiva"
}
```

#### Listar Vacas
```http
GET http://localhost:8000/vacas/
Authorization: Bearer SEU_TOKEN_AQUI
```

#### Buscar Vaca por Nome
```http
GET http://localhost:8000/vacas/?search=Mimosa
Authorization: Bearer SEU_TOKEN_AQUI
```

#### Atualizar Vaca
```http
PUT http://localhost:8000/vacas/1
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "peso": 560.0,
  "producao_media": 26.5
}
```

### 4. 📊 **Produção de Leite**

#### Registrar Produção
```http
POST http://localhost:8000/producao/
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "vaca_id": 1,
  "data": "2024-01-15",
  "quantidade_manha": 12.5,
  "quantidade_tarde": 13.0,
  "observacoes": "Produção normal"
}
```

#### Listar Produção
```http
GET http://localhost:8000/producao/
Authorization: Bearer SEU_TOKEN_AQUI
```

#### Filtrar por Vaca
```http
GET http://localhost:8000/producao/?vaca_id=1
Authorization: Bearer SEU_TOKEN_AQUI
```

### 5. 💰 **Controle Financeiro**

#### Registrar Receita
```http
POST http://localhost:8000/financeiro/receitas
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "descricao": "Venda de leite",
  "valor": 150.50,
  "data": "2024-01-15",
  "categoria": "venda_leite"
}
```

#### Registrar Despesa
```http
POST http://localhost:8000/financeiro/despesas
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "descricao": "Ração para gado",
  "valor": 85.00,
  "data": "2024-01-15",
  "categoria": "alimentacao"
}
```

### 6. 🐮 **Controle Reprodutivo**

#### Registrar Inseminação
```http
POST http://localhost:8000/reproducao/
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "vaca_id": 1,
  "tipo": "inseminacao",
  "data": "2024-01-15",
  "data_prevista_parto": "2024-10-15",
  "observacoes": "Primeira inseminação"
}
```

### 7. 🛒 **Marketplace**

#### Criar Anúncio
```http
POST http://localhost:8000/marketplace/
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "titulo": "Vaca Holandesa - Alta Produção",
  "descricao": "Vaca de 3 anos, produção média 25L/dia",
  "categoria": "vaca",
  "preco": 3500.00,
  "localizacao": "São Paulo - SP",
  "telefone": "(11) 99999-9999"
}
```

#### Listar Anúncios
```http
GET http://localhost:8000/marketplace/
```

### 8. 💳 **Sistema de Assinaturas**

#### Ver Planos
```http
GET http://localhost:8000/subscriptions/plans
```

#### Status da Assinatura
```http
GET http://localhost:8000/subscriptions/status
Authorization: Bearer SEU_TOKEN_AQUI
```

#### Fazer Upgrade
```http
PUT http://localhost:8000/subscriptions/upgrade?new_plan=basic
Authorization: Bearer SEU_TOKEN_AQUI
```

## 🧪 **Testes de Validação**

### Teste 1: Senha Fraca
```http
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "teste2@vacafacil.com",
  "nome": "Teste",
  "password": "123"
}
```
**Esperado**: Erro 422 - "Senha deve ter pelo menos 6 caracteres"

### Teste 2: Dados Inválidos de Vaca
```http
POST http://localhost:8000/vacas/
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "nome": "",
  "raca": "Holandesa",
  "idade": -1,
  "peso": -100
}
```
**Esperado**: Erro 422 - Validações de campos

### Teste 3: Limite de Vacas (Plano Gratuito)
Tente criar mais de 5 vacas no plano gratuito.
**Esperado**: Erro 403 - "Limite de vacas atingido"

## 📊 **Endpoints de Monitoramento**

### Health Check
```http
GET http://localhost:8000/health
```

### Documentação
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 **Comandos Úteis**

```bash
# Ver logs do servidor
tail -f app.log

# Resetar banco de dados
del vacafacil.db
python create_tables.py

# Executar testes automatizados
pytest app/tests/ -v
```

## 📱 **Testando com cURL**

```bash
# Registrar usuário
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@vacafacil.com","nome":"João","password":"senha123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@vacafacil.com&password=senha123"

# Criar vaca (substitua TOKEN)
curl -X POST "http://localhost:8000/vacas/" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Mimosa","raca":"Holandesa","idade":3}'
```

## ✅ **Checklist de Testes**

- [ ] Registro de usuário funciona
- [ ] Login retorna token válido
- [ ] Token é aceito em endpoints protegidos
- [ ] Validações de dados funcionam
- [ ] CRUD de vacas completo
- [ ] Sistema de produção funciona
- [ ] Controle financeiro operacional
- [ ] Marketplace acessível
- [ ] Limites de assinatura respeitados
- [ ] Exception handlers funcionando
- [ ] Documentação Swagger acessível