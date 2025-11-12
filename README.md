# 🐄 VacaFácil Backend

Backend da aplicação VacaFácil - Sistema de gestão para fazendas leiteiras.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação segura
- **Pydantic** - Validação de dados
- **Alembic** - Migrações de banco

## 📦 Instalação

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd BackEnd_VacaFacil
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar banco de dados
```bash
# Instalar PostgreSQL
# Criar banco: vacafacil
# Configurar .env com suas credenciais
```

### 5. Executar aplicação
```bash
uvicorn app.main:app --reload
```

## 🐳 Docker

```bash
# Executar com Docker Compose
docker-compose up --build
```

## 📚 Documentação da API

Após executar a aplicação, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Autenticação

A API usa JWT para autenticação. Endpoints protegidos requerem o header:
```
Authorization: Bearer <token>
```

## 📊 Funcionalidades

- ✅ Autenticação JWT
- ✅ Gestão de usuários
- ✅ Cadastro de vacas
- ✅ Sistema de assinaturas
- 🚧 Controle de produção
- 🚧 Relatórios financeiros
- 🚧 Marketplace

## 🧪 Testes

```bash
pytest
```

## 📝 Estrutura do Projeto

```
app/
├── models/          # Modelos SQLAlchemy
├── schemas/         # Schemas Pydantic
├── routers/         # Rotas da API
├── services/        # Lógica de negócio
├── utils/           # Utilitários
└── tests/           # Testes
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request