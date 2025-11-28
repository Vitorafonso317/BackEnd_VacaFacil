# 📧 Frontend - Sistema de Recuperação de Senha

## 1. Criar `src/pages/ForgotPassword.jsx`

```jsx
import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    
    try {
      await api.post('/auth/forgot-password', { email });
      setMessage('Email enviado! Verifique sua caixa de entrada.');
      setEmail('');
    } catch (err) {
      setError('Erro ao enviar email. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">Esqueceu sua senha?</h2>
        <p className="text-gray-600 text-center mb-6">
          Digite seu email e enviaremos instruções para redefinir sua senha.
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Email</label>
            <input
              type="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 disabled:bg-gray-400"
          >
            {loading ? 'Enviando...' : 'Enviar Email'}
          </button>
        </form>
        
        {message && (
          <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
            {message}
          </div>
        )}
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}
        
        <div className="mt-6 text-center">
          <Link to="/login" className="text-green-500 hover:underline">
            Voltar para o login
          </Link>
        </div>
      </div>
    </div>
  );
}
```

## 2. Criar `src/pages/ResetPassword.jsx`

```jsx
import { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (password !== confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }
    
    if (password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres');
      return;
    }
    
    setLoading(true);
    
    try {
      await api.post('/auth/reset-password', {
        token,
        new_password: password
      });
      
      alert('Senha alterada com sucesso!');
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao alterar senha. Token pode estar expirado.');
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600">Token inválido</h2>
          <p className="mt-2">O link de recuperação é inválido.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">Nova Senha</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Nova Senha</label>
            <input
              type="password"
              placeholder="Mínimo 6 caracteres"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
              minLength={6}
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Confirmar Senha</label>
            <input
              type="password"
              placeholder="Digite a senha novamente"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 disabled:bg-gray-400"
          >
            {loading ? 'Alterando...' : 'Alterar Senha'}
          </button>
        </form>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
```

## 3. Adicionar link no `Login.jsx`

Adicione este link abaixo do botão de login:

```jsx
<div className="text-center mt-4">
  <Link to="/forgot-password" className="text-green-500 hover:underline">
    Esqueceu sua senha?
  </Link>
</div>
```

## 4. Adicionar rotas no `App.jsx`

```jsx
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';

// Nas rotas:
<Route path="/forgot-password" element={<ForgotPassword />} />
<Route path="/reset-password" element={<ResetPassword />} />
```

## 5. Configurar Gmail

1. Acesse: https://myaccount.google.com/security
2. Ative a "Verificação em duas etapas"
3. Acesse: https://myaccount.google.com/apppasswords
4. Crie uma senha de app para "Email"
5. Use essa senha no `.env` do backend em `MAIL_PASSWORD`

## 6. Atualizar `.env` do backend

```env
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=senha_de_app_gerada_pelo_gmail
MAIL_FROM=seu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=VacaFácil
FRONTEND_URL=http://localhost:3000
```

## 7. Instalar dependência no backend

```bash
pip install fastapi-mail
```

## ✅ Pronto!

Agora você tem um sistema completo de recuperação de senha! 🎉
