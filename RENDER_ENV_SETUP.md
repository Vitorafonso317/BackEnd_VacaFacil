# 🔧 Configurar Variáveis de Ambiente no Render

## Passo a Passo

### 1. Acesse o Dashboard do Render
- Vá para: https://dashboard.render.com
- Clique no seu serviço **VacaFacil**

### 2. Vá em Environment
- No menu lateral, clique em **Environment**

### 3. Adicione as Variáveis

Clique em **Add Environment Variable** e adicione cada uma:

#### Variáveis Obrigatórias (Já devem estar configuradas)
```
DATABASE_URL = [Já configurado automaticamente pelo Render]
```

#### Variáveis de Segurança
```
SECRET_KEY = xK9mP2vN8qR5tY7wE4aS6dF3gH1jL0zX9cV8bN5mQ2wP4tR7uY9vB3nM6qS8dG
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

#### CORS
```
ALLOWED_ORIGINS = ["https://front-vacafacil.vercel.app","http://localhost:5173"]
```

#### Email (Gmail)
```
MAIL_USERNAME = vacafacil344@gmail.com
MAIL_PASSWORD = 224107
MAIL_FROM = vacafacil344@gmail.com
MAIL_PORT = 587
MAIL_SERVER = smtp.gmail.com
MAIL_FROM_NAME = VacaFácil
```

#### Frontend
```
FRONTEND_URL = https://front-vacafacil.vercel.app
```

#### Firebase (Opcional - se usar upload de imagens)
```
FIREBASE_CREDENTIALS_PATH = vacafacil-9b0f3.json
FIREBASE_STORAGE_BUCKET = vacafacil-9b0f3.appspot.com
```

### 4. Salvar
- Clique em **Save Changes**
- O Render vai fazer redeploy automaticamente

### 5. Verificar
Após o deploy, acesse:
- https://seu-app.onrender.com/health
- https://seu-app.onrender.com/docs

## ⚠️ Importante

### Gerar SECRET_KEY Segura
Para produção, gere uma chave única:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### Gmail - Senha de App
Se usar Gmail, você precisa:
1. Ativar verificação em 2 etapas
2. Gerar uma "Senha de App" em: https://myaccount.google.com/apppasswords
3. Usar essa senha no `MAIL_PASSWORD`

## 📋 Checklist Final

- [ ] DATABASE_URL configurada
- [ ] SECRET_KEY configurada (32+ caracteres)
- [ ] ALGORITHM = HS256
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES = 30
- [ ] ALLOWED_ORIGINS com URL do frontend
- [ ] MAIL_USERNAME configurado
- [ ] MAIL_PASSWORD configurado (senha de app)
- [ ] MAIL_FROM configurado
- [ ] MAIL_PORT = 587
- [ ] MAIL_SERVER = smtp.gmail.com
- [ ] FRONTEND_URL com URL do Vercel
- [ ] Deploy concluído com sucesso
- [ ] /health retorna 200 OK
- [ ] /docs acessível

## 🐛 Troubleshooting

### Erro: "MAIL_USERNAME should be a valid string"
- Certifique-se de adicionar TODAS as variáveis de email
- Não deixe nenhuma vazia

### Erro: "Authentication failed"
- Use senha de app do Gmail, não a senha normal
- Verifique se 2FA está ativado no Gmail

### Deploy não inicia
- Verifique os logs em **Logs** no painel
- Confirme que todas as variáveis estão salvas
