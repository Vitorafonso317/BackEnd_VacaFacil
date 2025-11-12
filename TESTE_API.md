# 🧪 Guia de Testes da API VacaFácil

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados
```bash
# Criar banco PostgreSQL
createdb vacafacil

# Ou usar SQLite para desenvolvimento
# A aplicação criará automaticamente as tabelas
```

### 3. Executar Aplicação
```bash
# Método 1: Script automático (Windows)
run.bat

# Método 2: Comando direto
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Método 3: Docker
docker-compose up --build
```

### 4. Acessar Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 Endpoints Disponíveis

### 🔐 Autenticação

#### Registrar Usuário
```http
POST /auth/register
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "fazenda": "Fazenda São João",
  "password": "senha123"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=usuario@exemplo.com&password=senha123
```

### 🐄 Gestão de Vacas

#### Listar Vacas
```http
GET /vacas?skip=0&limit=10&search=Mimosa&raca=Holandesa&status=ativa
Authorization: Bearer {token}
```

#### Criar Vaca
```http
POST /vacas
Authorization: Bearer {token}
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

#### Atualizar Vaca
```http
PUT /vacas/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "nome": "Mimosa Atualizada",
  "peso": 560.0
}
```

#### Deletar Vaca
```http
DELETE /vacas/{id}
Authorization: Bearer {token}
```

### 💳 Sistema de Assinaturas

#### Listar Planos
```http
GET /subscriptions/plans
```

#### Criar Assinatura
```http
POST /subscriptions/subscribe
Authorization: Bearer {token}
Content-Type: application/json

{
  "plan_type": "basic",
  "payment_method": "credit_card"
}
```

#### Status da Assinatura
```http
GET /subscriptions/status
Authorization: Bearer {token}
```

#### Upgrade de Plano
```http
PUT /subscriptions/upgrade?new_plan=pro
Authorization: Bearer {token}
```

#### Cancelar Assinatura
```http
DELETE /subscriptions/cancel
Authorization: Bearer {token}
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app

# Executar testes específicos
pytest app/tests/test_auth.py
```

## 📊 Exemplos de Uso

### 1. Fluxo Completo de Registro e Login
```bash
# 1. Registrar usuário
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "fazendeiro@exemplo.com",
    "nome": "José da Silva",
    "fazenda": "Fazenda Boa Vista",
    "password": "senha123"
  }'

# 2. Fazer login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=fazendeiro@exemplo.com&password=senha123"

# 3. Usar token retornado nas próximas requisições
```

### 2. Gestão de Rebanho
```bash
# Criar vaca
curl -X POST "http://localhost:8000/vacas" \
  -H "Authorization: Bearer {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Estrela",
    "raca": "Gir",
    "idade": 4,
    "peso": 480.0,
    "producao_media": 18.5
  }'

# Listar vacas
curl -X GET "http://localhost:8000/vacas" \
  -H "Authorization: Bearer {seu_token}"
```

## 🔧 Troubleshooting

### Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
pg_ctl status

# Verificar conexão
psql -h localhost -U vacafacil_user -d vacafacil
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Limpar cache
pip cache purge
```

### Erro de CORS
- Verificar se o frontend está na lista de origens permitidas em `app/config.py`
- Adicionar nova origem se necessário

## 📈 Monitoramento

### Health Check
```http
GET /health
```

### Métricas da API
- Acesse http://localhost:8000/docs para ver todas as rotas disponíveis
- Use ferramentas como Postman ou Insomnia para testes mais complexos

## 🚀 Deploy em Produção

### Usando Docker
```bash
# Build da imagem
docker build -t vacafacil-api .

# Executar container
docker run -p 8000:8000 -e DATABASE_URL="postgresql://..." vacafacil-api
```

### Usando Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar em produção
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```