# ✅ Configuração de Conexão - VacaFácil

## 🎯 URLs Configuradas

**Frontend (Vercel):** https://front-vacafacil.vercel.app
**Backend (Render):** https://backend-vacafacil.onrender.com

---

## 1️⃣ CONFIGURAR NA RENDER (Backend)

Acesse: https://dashboard.render.com → Seu serviço → **Environment**

**Adicione/Atualize esta variável:**

```
ALLOWED_ORIGINS=["https://front-vacafacil.vercel.app","http://localhost:5173","http://localhost:3000"]
```

**Depois clique em "Save Changes" e faça "Manual Deploy"**

---

## 2️⃣ CONFIGURAR NA VERCEL (Frontend)

Acesse: https://vercel.com/dashboard → Seu projeto → **Settings** → **Environment Variables**

**Adicione esta variável:**

**Name:** `VITE_API_URL`
**Value:** `https://backend-vacafacil.onrender.com`

**Depois faça um novo deploy (ou vai automaticamente)**

---

## 3️⃣ TESTAR A CONEXÃO

### Teste 1: Health Check
Abra no navegador:
```
https://backend-vacafacil.onrender.com/health
```

Deve retornar: `{"status":"healthy"}`

### Teste 2: Documentação
```
https://backend-vacafacil.onrender.com/docs
```

### Teste 3: No Frontend
Abra o console do navegador (F12) e teste:

```javascript
fetch('https://backend-vacafacil.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 4️⃣ CÓDIGO PARA O FRONTEND

### Configurar API URL (src/config.js ou similar)

```javascript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
```

### Exemplo de Login

```javascript
import { API_URL } from './config';

export const login = async (email, password) => {
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

  if (!response.ok) throw new Error('Login falhou');
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};
```

### Exemplo de Request Autenticado

```javascript
import { API_URL } from './config';

export const getVacas = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_URL}/vacas/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) throw new Error('Erro ao buscar vacas');
  return response.json();
};
```

---

## 📋 Checklist Final

- [ ] ALLOWED_ORIGINS configurado na Render
- [ ] Deploy manual feito na Render
- [ ] VITE_API_URL configurado na Vercel
- [ ] Deploy feito na Vercel
- [ ] Teste /health funcionando
- [ ] CORS funcionando (sem erro no console)
- [ ] Login funcionando
- [ ] Requests autenticados funcionando

---

## 🐛 Problemas Comuns

### ❌ Erro: "CORS policy: No 'Access-Control-Allow-Origin'"
**Solução:** Verifique se a URL da Vercel está correta em ALLOWED_ORIGINS na Render

### ❌ Erro: "Failed to fetch"
**Solução:** Verifique se a URL do backend está correta na Vercel

### ❌ Erro: 401 Unauthorized
**Solução:** Verifique se o token está sendo enviado: `Authorization: Bearer {token}`

### ❌ Backend não responde
**Solução:** Render pode estar em "sleep". Acesse a URL do backend primeiro para acordar.

---

## 🚀 Pronto!

Agora seu frontend na Vercel está conectado com o backend na Render!
