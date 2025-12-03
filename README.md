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

## ⚡ Início Rápido

### 1. Verificar se está tudo OK
```bash
python verificar_api.py
```

### 2. Iniciar o servidor
```bash
iniciar.bat
```

Ou manualmente:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### 3. Testar a API
```bash
python test_api.py
```

### 4. Acessar a documentação
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- PostgreSQL
- pip

### Configuração

1. **Clone o repositório**
```bash
git clone <repository-url>
cd BackEnd_VacaFacil
```

2. **Crie o ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Copie `.env.example` para `.env` e configure:
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=sua_chave_secreta_de_32_caracteres_ou_mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

5. **Execute a aplicação**
```bash
iniciar.bat
```

## 📚 Documentação da API

### Endpoints Disponíveis

#### 🔐 Autenticação
- `POST /auth/register` - Registrar novo usuário
- `POST /auth/login` - Login e obter token JWT

#### 👤 Usuários
- `GET /users/me` - Obter dados do usuário logado
- `PUT /users/me` - Atualizar dados do usuário
- `DELETE /users/me` - Deletar conta

#### 🐄 Vacas (Cattle)
- `GET /vacas/` - Listar todas as vacas
- `POST /vacas/` - Cadastrar nova vaca
- `GET /vacas/{id}` - Obter detalhes de uma vaca
- `PUT /vacas/{id}` - Atualizar dados da vaca
- `DELETE /vacas/{id}` - Remover vaca

#### 🥛 Produção
- `GET /producao/` - Listar registros de produção
- `POST /producao/` - Registrar produção de leite
- `GET /producao/?vaca_id={id}` - Produção de uma vaca específica
- `PUT /producao/{id}` - Atualizar registro de produção

#### 🐮 Reprodução
- `GET /reproducao/` - Listar eventos de reprodução
- `POST /reproducao/` - Registrar evento de reprodução
- `GET /reproducao/{id}` - Detalhes do evento

#### 💰 Financeiro
- `GET /financeiro/receitas` - Listar receitas
- `POST /financeiro/receitas` - Registrar receita
- `GET /financeiro/despesas` - Listar despesas
- `POST /financeiro/despesas` - Registrar despesa

#### 🛒 Marketplace
- `GET /marketplace/` - Listar anúncios
- `POST /marketplace/` - Criar anúncio
- `GET /marketplace/{id}` - Detalhes do anúncio
- `PUT /marketplace/{id}` - Atualizar anúncio
- `DELETE /marketplace/{id}` - Remover anúncio

#### 💳 Assinaturas
- `GET /subscriptions/plans` - Listar planos disponíveis
- `POST /subscriptions/subscribe` - Criar assinatura
- `GET /subscriptions/status` - Status da assinatura
- `PUT /subscriptions/upgrade` - Fazer upgrade de plano
- `DELETE /subscriptions/cancel` - Cancelar assinatura

#### 🔔 Notificações
- `POST /notifications/send` - Enviar notificação
- `GET /notifications/` - Listar notificações
- `PUT /notifications/{id}` - Marcar como lida
- `PUT /notifications/mark-all-read` - Marcar todas como lidas
- `DELETE /notifications/{id}` - Deletar notificação
- `GET /notifications/unread/count` - Contar não lidas

#### 📊 Relatórios
- `GET /relatorios/producao/json` - Relatório de produção
- `GET /relatorios/financeiro/json` - Relatório financeiro
- `GET /relatorios/completo/json` - Relatório completo da fazenda

#### 🤖 Machine Learning
- `POST /ml/predict-production` - Prever produção de leite
- `GET /ml/analyze-performance` - Análise de performance do rebanho
- `GET /ml/detect-anomalies` - Detectar anomalias na produção
- `GET /ml/recommendations` - Recomendações inteligentes
- `GET /ml/financial-forecast` - Previsão financeira
- `GET /ml/insights` - Dashboard com insights de ML

## 🔐 Autenticação

Todos os endpoints (exceto `/auth/register` e `/auth/login`) requerem autenticação JWT.

### Como usar:
1. Registre um usuário em `/auth/register`
2. Faça login em `/auth/login` para obter o token
3. Use o token no header: `Authorization: Bearer {seu_token}`

### Exemplo com cURL:
```bash
# Registro
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","nome":"User","password":"senha123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=senha123"

# Usar token
curl -X GET http://localhost:5000/users/me \
  -H "Authorization: Bearer {seu_token}"
```

## 🗄️ Banco de Dados

### PostgreSQL (Produção)
```sql
CREATE DATABASE vacafacil;
CREATE USER vacafacil_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE vacafacil TO vacafacil_user;
```

### SQLite (Desenvolvimento)
O arquivo `vacafacil.db` é criado automaticamente.

As tabelas são criadas automaticamente ao iniciar a aplicação.

## 🧪 Testes

### Executar todos os testes
```bash
pytest
```

### Com cobertura
```bash
pytest --cov=app
```

### Testes específicos
```bash
pytest app/tests/test_auth.py -v
```

### Teste completo da API
```bash
python test_api.py
```

## 📁 Estrutura do Projeto

```
BackEnd_VacaFacil/
├── app/
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── user_model.py
│   │   ├── cattle_model.py
│   │   ├── production_model.py
│   │   ├── reproduction_model.py
│   │   ├── financial_model.py
│   │   ├── marketplace_model.py
│   │   └── subscription_model.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── user_schemas.py
│   │   ├── cattle_schemas.py
│   │   ├── production_schemas.py
│   │   ├── reproduction_schemas.py
│   │   ├── financial_schemas.py
│   │   ├── marketplace_schemas.py
│   │   ├── subscription_schemas.py
│   │   └── ml_schemas.py
│   ├── routers/             # Rotas da API
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── cattle_routes.py
│   │   ├── production_routes.py
│   │   ├── reproduction_routes.py
│   │   ├── financial_routes.py
│   │   ├── marketplace_routes.py
│   │   ├── subscription_routes.py
│   │   └── ml_routes.py
│   ├── services/            # Lógica de negócio
│   │   ├── subscription_service.py
│   │   ├── ml_service.py
│   │   └── ml_service_simple.py
│   ├── utils/               # Utilitários
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── exception_handlers.py
│   ├── middleware/          # Middlewares
│   │   └── security_middleware.py
│   ├── tests/               # Testes automatizados
│   ├── config.py            # Configurações
│   ├── database.py          # Conexão com banco
│   └── main.py              # Aplicação principal
├── .env                     # Variáveis de ambiente
├── .env.example             # Template de variáveis
├── requirements.txt         # Dependências Python
├── docker-compose.yml       # Orquestração Docker
├── Dockerfile              # Imagem Docker
├── iniciar.bat             # Script de inicialização
├── test_api.py             # Teste completo da API
├── verificar_api.py        # Verificação do sistema
└── README.md               # Este arquivo
```

## 🐳 Docker

### Executar com Docker Compose
```bash
docker-compose up --build
```

### Build manual
```bash
docker build -t vacafacil-api .
docker run -p 5000:5000 vacafacil-api
```

## 🚀 Deploy

### Render / Railway / Heroku
1. Configure as variáveis de ambiente
2. Configure o PostgreSQL
3. Deploy automático via Git

### Comando de start
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 💳 Sistema de Assinaturas

### Planos Disponíveis
- **Gratuito**: 5 vacas, histórico 30 dias
- **Básico (R$ 29,90)**: 50 vacas, histórico 1 ano, marketplace
- **Pro (R$ 59,90)**: Vacas ilimitadas, recursos avançados, ML

## 🤖 Machine Learning

O sistema inclui funcionalidades de ML para:
- Predição de produção de leite
- Detecção de anomalias
- Análise de performance do rebanho
- Recomendações inteligentes
- Previsões financeiras

## 🔒 Segurança

- ✅ Autenticação JWT
- ✅ Senhas com hash bcrypt
- ✅ Validação de dados com Pydantic
- ✅ CORS configurado
- ✅ Rate limiting
- ✅ SQL Injection protegido (SQLAlchemy ORM)

## 📊 Status do Projeto

✅ **100% Funcional**
- 36+ endpoints testados e funcionando
- Autenticação completa
- CRUD completo de todas as entidades
- Sistema de notificações
- Relatórios completos
- Machine Learning integrado
- Testes automatizados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação em http://localhost:5000/docs
- Verifique os arquivos de documentação:
  - `docs/` - Documentação completa de todos os endpoints
  - `INICIO_RAPIDO.md` - Guia rápido
  - `README_EXECUCAO.md` - Documentação detalhada
  - `STATUS_FINAL.md` - Status completo do projeto
  - `RENDER_ENV_SETUP.md` - Configuração do Render

## 🎯 Roadmap

- [x] API REST completa
- [x] Autenticação JWT
- [x] Sistema de assinaturas
- [x] Machine Learning básico
- [x] Sistema de notificações
- [x] Relatórios JSON
- [ ] Notificações push (Firebase)
- [ ] Relatórios em PDF
- [ ] Integração com IoT
- [ ] App mobile

---

**Desenvolvido com ❤️ para facilitar a gestão de fazendas leiteiras**
