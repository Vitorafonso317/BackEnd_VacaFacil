# 🔧 Configuração Manual na Render

## ⚠️ IMPORTANTE: Configure Manualmente no Painel da Render

A Render está ignorando o Procfile. Siga estes passos:

### 1️⃣ Acesse o Dashboard da Render
- Vá para: https://dashboard.render.com
- Selecione seu serviço VacaFácil

### 2️⃣ Configure o Start Command

**Vá em: Settings > Build & Deploy**

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3️⃣ Configure as Variáveis de Ambiente

**Vá em: Environment**

Adicione estas variáveis:

```
SECRET_KEY = [Gerar valor aleatório de 32+ caracteres]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALLOWED_ORIGINS = ["*"]
```

**DATABASE_URL** já deve estar configurada automaticamente.

### 4️⃣ Configurações Adicionais

**Build Command:**
```bash
pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
```

**Python Version:**
```
3.11.7
```

### 5️⃣ Salvar e Fazer Deploy Manual

1. Clique em **"Save Changes"**
2. Clique em **"Manual Deploy"** > **"Deploy latest commit"**

### 6️⃣ Verificar Deploy

Após o deploy:
- ✅ Health: `https://seu-app.onrender.com/health`
- ✅ Docs: `https://seu-app.onrender.com/docs`

## 🔑 Gerar SECRET_KEY

Use este comando para gerar uma chave segura:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Ou use este valor de exemplo (MUDE EM PRODUÇÃO):
```
xK9mP2vN8qR5tY7wE4aS6dF3gH1jL0zX9cV8bN5mQ2
```

## 📋 Checklist

- [ ] Start Command configurado: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] SECRET_KEY configurada (32+ caracteres)
- [ ] ALGORITHM = HS256
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES = 30
- [ ] ALLOWED_ORIGINS configurado
- [ ] Build Command configurado
- [ ] Python Version = 3.11.7
- [ ] Deploy manual executado
- [ ] Health check funcionando

## 🐛 Se ainda der erro

1. Verifique os logs em **Logs** no painel
2. Confirme que todas as variáveis estão configuradas
3. Tente fazer um novo deploy manual
4. Verifique se o DATABASE_URL está correto