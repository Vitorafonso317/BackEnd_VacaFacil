# 🚀 Deploy na Render - VacaFácil API

## ✅ Deploy Realizado

O backend foi deployado com sucesso na Render!

## 🔧 Configurações Necessárias

### Variáveis de Ambiente na Render

Configure as seguintes variáveis no painel da Render:

```env
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=sua_chave_secreta_de_32_caracteres_ou_mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["https://seu-frontend.com","http://localhost:5173"]
```

### Comando de Start

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 📋 Checklist Pós-Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] DATABASE_URL apontando para PostgreSQL da Render
- [ ] SECRET_KEY configurada (mínimo 32 caracteres)
- [ ] ALLOWED_ORIGINS incluindo domínio do frontend
- [ ] Health check funcionando: `https://seu-app.onrender.com/health`
- [ ] Documentação acessível: `https://seu-app.onrender.com/docs`

## 🧪 Testar API em Produção

```bash
# Health Check
curl https://seu-app.onrender.com/health

# Documentação
https://seu-app.onrender.com/docs
```

## 🔒 Segurança

✅ Credenciais hardcoded removidas
✅ SQL Injection corrigido
✅ Headers de segurança aplicados
✅ Rate limiting implementado
✅ Validação de SECRET_KEY obrigatória

## 📊 Endpoints Disponíveis

- **Auth**: `/auth/register`, `/auth/login`
- **Users**: `/users/me`
- **Cattle**: `/vacas/`
- **Production**: `/producao/`
- **Financial**: `/financeiro/receitas`, `/financeiro/despesas`
- **Subscriptions**: `/subscriptions/`
- **ML**: `/ml/predict-production`, `/ml/insights`
- **Marketplace**: `/marketplace/`

## 🐛 Troubleshooting

### Erro 500 no startup
- Verifique se SECRET_KEY está configurada
- Verifique se DATABASE_URL está correta
- Veja os logs na Render

### Erro de CORS
- Adicione o domínio do frontend em ALLOWED_ORIGINS

### Erro de conexão com banco
- Verifique se o PostgreSQL está ativo na Render
- Confirme a DATABASE_URL

## 📞 Suporte

- Logs: Painel da Render > Logs
- Documentação: `/docs` endpoint
- Health: `/health` endpoint