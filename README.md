# 🐄 VacaFácil Backend

Backend da aplicação VacaFácil - Sistema completo de gestão para fazendas leiteiras.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação segura
- **Pydantic** - Validação de dados
- **Alembic** - Migrações de banco
- **Docker** - Containerização
- **Pytest** - Testes automatizados

## 📦 Instalação Rápida

### Método 1: Script Automático (Windows)
```bash
# Execute o script que configura tudo automaticamente
run.bat
```

### Método 2: Manual
```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
# Edite o arquivo .env com suas configurações

# 4. Executar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Método 3: Docker
```bash
# Executar com Docker Compose (inclui PostgreSQL)
docker-compose up --build
```

## 🗄️ Configuração do Banco

### PostgreSQL (Recomendado para Produção)
```sql
-- Criar banco e usuário
CREATE DATABASE vacafacil;
CREATE USER vacafacil_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE vacafacil TO vacafacil_user;
```

### SQLite (Desenvolvimento)
```bash
# A aplicação criará automaticamente o arquivo SQLite
# Apenas execute: python create_tables.py
```

## 📚 Documentação da API

Após executar a aplicação:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Sistema de Autenticação

### Registro de Usuário
```http
POST /auth/register
{
  "email": "fazendeiro@exemplo.com",
  "nome": "José Silva",
  "fazenda": "Fazenda Boa Vista",
  "password": "senha123"
}
```

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=fazendeiro@exemplo.com&password=senha123
```

### Usar Token
```http
Authorization: Bearer {token_retornado}
```

## 💳 Sistema de Assinaturas

### Planos Disponíveis
- **Gratuito**: 5 vacas, histórico 30 dias
- **Básico (R$ 29,90)**: 50 vacas, histórico 1 ano, marketplace
- **Pro (R$ 59,90)**: Vacas ilimitadas, recursos avançados

### Endpoints
```http
GET /subscriptions/plans          # Listar planos
POST /subscriptions/subscribe     # Criar assinatura
GET /subscriptions/status         # Status atual
PUT /subscriptions/upgrade        # Upgrade de plano
DELETE /subscriptions/cancel      # Cancelar
```

## 📊 Funcionalidades Implementadas

- ✅ **Autenticação JWT** - Login/registro seguro
- ✅ **Gestão de Usuários** - Perfis e configurações
- ✅ **Cadastro de Vacas** - CRUD completo do rebanho
- ✅ **Sistema de Assinaturas** - Planos e limites
- ✅ **Controle de Produção** - Registro diário de leite
- ✅ **Validações Robustas** - Schemas Pydantic
- ✅ **Documentação Automática** - Swagger/OpenAPI
- ✅ **Testes Automatizados** - Pytest
- ✅ **Docker Support** - Containerização completa

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app

# Testes específicos
pytest app/tests/test_auth.py -v
```

## 📁 Estrutura do Projeto

```
BackEnd_VacaFacil/
├── app/
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── user.py         # Modelo de usuário
│   │   ├── vaca.py         # Modelo de vaca
│   │   ├── producao.py     # Modelo de produção
│   │   └── subscription.py # Modelo de assinatura
│   ├── schemas/            # Schemas Pydantic
│   │   ├── user.py         # Validações de usuário
│   │   ├── vaca.py         # Validações de vaca
│   │   └── subscription.py # Validações de assinatura
│   ├── routers/            # Rotas da API
│   │   ├── auth.py         # Autenticação
│   │   ├── vacas.py        # Gestão de vacas
│   │   └── subscriptions.py# Sistema de assinaturas
│   ├── services/           # Lógica de negócio
│   │   └── subscription_service.py
│   ├── utils/              # Utilitários
│   │   ├── security.py     # JWT e criptografia
│   │   └── dependencies.py # Dependências FastAPI
│   ├── tests/              # Testes automatizados
│   ├── config.py           # Configurações
│   ├── database.py         # Conexão com banco
│   └── main.py             # Aplicação principal
├── .env                    # Variáveis de ambiente
├── requirements.txt        # Dependências Python
├── docker-compose.yml      # Orquestração Docker
├── Dockerfile             # Imagem Docker
├── alembic.ini            # Configuração de migrações
├── run.bat                # Script de execução Windows
└── TESTE_API.md           # Guia de testes
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env)
```env
# IMPORTANTE: Copie .env.example para .env e configure suas variáveis
DATABASE_URL=postgresql://username:password@localhost:5432/vacafacil_db
SECRET_KEY=sua_chave_secreta_de_32_caracteres_ou_mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### Verificação de Segurança
```bash
# Verificar configurações de segurança
python security_check.py
```

### Migrações com Alembic
```bash
# Inicializar Alembic
alembic init alembic

# Criar migração
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head
```

## 🚀 Deploy em Produção

### Usando Docker
```bash
# Build da imagem
docker build -t vacafacil-api .

# Executar em produção
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  -e SECRET_KEY="sua_chave_producao" \
  vacafacil-api
```

### Usando Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar com múltiplos workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📈 Monitoramento

### Health Checks
```bash
# Verificar status da API
curl http://localhost:8000/health

# Verificar métricas
curl http://localhost:8000/docs
```

## 🛠️ Ferramentas de Desenvolvimento

- **Insomnia/Postman**: Use `insomnia_collection.json` para importar requests
- **pgAdmin**: Interface gráfica para PostgreSQL
- **Docker Desktop**: Gerenciamento de containers
- **VS Code**: Editor recomendado com extensões Python

## 🔒 Segurança

### Problemas Corrigidos
- ✅ Credenciais hardcoded removidas
- ✅ SQL Injection corrigido
- ✅ Tratamento de erros melhorado
- ✅ Rate limiting implementado
- ✅ Logging de segurança
- ✅ Validação de SECRET_KEY

Veja `SECURITY.md` para detalhes completos de segurança.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação em `/docs`
- Verifique o guia de testes em `TESTE_API.md`
- Para problemas de segurança, veja `SECURITY.md`

## ⚙️ Arquivos Importantes

- `.env.example` - Template de variáveis de ambiente
- `SECURITY.md` - Guia de segurança
- `security_check.py` - Script de verificação
- `requirements.txt` - Dependências Python