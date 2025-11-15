# 🔗 Integração Backend (Render) + Frontend (Vercel)

## 1️⃣ Configure CORS no Backend (Render)

**Vá em: Environment Variables na Render**

Atualize a variável `ALLOWED_ORIGINS`:

```
ALLOWED_ORIGINS=["https://seu-app.vercel.app","http://localhost:5173","http://localhost:3000"]
```

**Substitua `seu-app.vercel.app` pela URL real do seu frontend na Vercel!**

## 2️⃣ Configure a API URL no Frontend (Vercel)

**No seu projeto frontend, adicione a variável de ambiente:**

```
VITE_API_URL=https://seu-backend.onrender.com
```

ou

```
NEXT_PUBLIC_API_URL=https://seu-backend.onrender.com
```

**Substitua `seu-backend.onrender.com` pela URL real do seu backend na Render!**

## 3️⃣ Teste a Conexão

### No Frontend, use:

```javascript
// Para Vite/React
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Para Next.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Teste
fetch(`${API_URL}/health`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 4️⃣ Endpoints Principais

```
GET  /health                    - Health check
POST /auth/register             - Registrar usuário
POST /auth/login                - Login
GET  /users/me                  - Dados do usuário
GET  /vacas/                    - Listar vacas
POST /vacas/                    - Criar vaca
GET  /producao/                 - Listar produção
POST /producao/                 - Registrar produção
```

## 5️⃣ Exemplo de Login

```javascript
const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData
  });

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};
```

## 6️⃣ Exemplo de Request Autenticado

```javascript
const getVacas = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/vacas/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.json();
};
```

## ✅ Checklist

- [ ] ALLOWED_ORIGINS configurado na Render com URL da Vercel
- [ ] API_URL configurado na Vercel com URL da Render
- [ ] Deploy manual feito na Render
- [ ] Deploy feito na Vercel
- [ ] Teste de /health funcionando
- [ ] Login funcionando
- [ ] Requests autenticados funcionando

## 🐛 Troubleshooting

### Erro de CORS
- Verifique se a URL da Vercel está em ALLOWED_ORIGINS
- Certifique-se de incluir `https://` na URL
- Faça redeploy na Render após mudar variáveis

### Erro 401 Unauthorized
- Verifique se o token está sendo enviado no header
- Formato: `Authorization: Bearer {token}`

### Erro de conexão
- Verifique se a URL da API está correta
- Teste a URL diretamente no navegador: `https://seu-backend.onrender.com/health`
