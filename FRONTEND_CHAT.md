# 💬 Frontend - Sistema de Chat do Marketplace

## Endpoints Disponíveis

### 1. Criar Conversa
```javascript
POST /chat/conversations
Body: { anuncio_id: number }
```

### 2. Listar Conversas
```javascript
GET /chat/conversations
Response: [{ id, anuncio_id, comprador_id, vendedor_id, ultima_mensagem, mensagens_nao_lidas }]
```

### 3. Ver Conversa Completa
```javascript
GET /chat/conversations/{id}
Response: { id, anuncio_id, mensagens: [...] }
```

### 4. Enviar Mensagem
```javascript
POST /chat/messages
Body: { conversation_id: number, mensagem: string }
```

### 5. Contar Não Lidas
```javascript
GET /chat/unread-count
Response: { unread_count: number }
```

---

## Frontend Implementation

### 1. Criar `src/services/chatService.js`

```javascript
import api from './api';

export const chatService = {
  // Criar conversa com vendedor
  createConversation: (anuncioId) => 
    api.post('/chat/conversations', { anuncio_id: anuncioId }),
  
  // Listar todas as conversas
  getConversations: () => 
    api.get('/chat/conversations'),
  
  // Ver conversa específica
  getConversation: (id) => 
    api.get(`/chat/conversations/${id}`),
  
  // Enviar mensagem
  sendMessage: (conversationId, mensagem) => 
    api.post('/chat/messages', { conversation_id: conversationId, mensagem }),
  
  // Contar não lidas
  getUnreadCount: () => 
    api.get('/chat/unread-count')
};
```

### 2. Criar `src/pages/ChatList.jsx`

```jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { chatService } from '../services/chatService';

export default function ChatList() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await chatService.getConversations();
      setConversations(response.data);
    } catch (error) {
      console.error('Erro ao carregar conversas:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Minhas Conversas</h1>
      
      {conversations.length === 0 ? (
        <p className="text-gray-500">Nenhuma conversa ainda</p>
      ) : (
        <div className="space-y-4">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => navigate(`/chat/${conv.id}`)}
              className="bg-white p-4 rounded-lg shadow cursor-pointer hover:shadow-md transition"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-semibold">Anúncio #{conv.anuncio_id}</h3>
                  <p className="text-gray-600 text-sm mt-1">
                    {conv.ultima_mensagem || 'Sem mensagens'}
                  </p>
                </div>
                {conv.mensagens_nao_lidas > 0 && (
                  <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                    {conv.mensagens_nao_lidas}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 3. Criar `src/pages/ChatRoom.jsx`

```jsx
import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { chatService } from '../services/chatService';

export default function ChatRoom() {
  const { id } = useParams();
  const [conversation, setConversation] = useState(null);
  const [mensagem, setMensagem] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadConversation();
    const interval = setInterval(loadConversation, 3000); // Atualizar a cada 3s
    return () => clearInterval(interval);
  }, [id]);

  useEffect(() => {
    scrollToBottom();
  }, [conversation?.mensagens]);

  const loadConversation = async () => {
    try {
      const response = await chatService.getConversation(id);
      setConversation(response.data);
    } catch (error) {
      console.error('Erro ao carregar conversa:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!mensagem.trim()) return;

    try {
      await chatService.sendMessage(id, mensagem);
      setMensagem('');
      loadConversation();
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-green-500 text-white p-4">
        <h2 className="font-bold">Chat - Anúncio #{conversation?.anuncio_id}</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {conversation?.mensagens.map((msg) => (
          <div
            key={msg.id}
            className={`mb-4 flex ${
              msg.sender_id === conversation.comprador_id ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.sender_id === conversation.comprador_id
                  ? 'bg-green-500 text-white'
                  : 'bg-white text-gray-800'
              }`}
            >
              <p>{msg.mensagem}</p>
              <span className="text-xs opacity-75">
                {new Date(msg.created_at).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="bg-white p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={mensagem}
            onChange={(e) => setMensagem(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button
            type="submit"
            className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600"
          >
            Enviar
          </button>
        </div>
      </form>
    </div>
  );
}
```

### 4. Adicionar botão no Anúncio

```jsx
// Em MarketplaceDetail.jsx ou similar
import { chatService } from '../services/chatService';

const handleContactSeller = async () => {
  try {
    const response = await chatService.createConversation(anuncio.id);
    navigate(`/chat/${response.data.id}`);
  } catch (error) {
    console.error('Erro ao criar conversa:', error);
  }
};

// No JSX:
<button
  onClick={handleContactSeller}
  className="bg-green-500 text-white px-6 py-2 rounded-lg"
>
  💬 Conversar com Vendedor
</button>
```

### 5. Badge de mensagens não lidas

```jsx
// Em Navbar.jsx ou Header.jsx
import { useState, useEffect } from 'react';
import { chatService } from '../services/chatService';

const [unreadCount, setUnreadCount] = useState(0);

useEffect(() => {
  const loadUnread = async () => {
    try {
      const response = await chatService.getUnreadCount();
      setUnreadCount(response.data.unread_count);
    } catch (error) {
      console.error('Erro ao carregar não lidas:', error);
    }
  };

  loadUnread();
  const interval = setInterval(loadUnread, 10000); // Atualizar a cada 10s
  return () => clearInterval(interval);
}, []);

// No JSX:
<Link to="/chat" className="relative">
  💬 Chat
  {unreadCount > 0 && (
    <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
      {unreadCount}
    </span>
  )}
</Link>
```

### 6. Adicionar rotas

```jsx
// Em App.jsx
import ChatList from './pages/ChatList';
import ChatRoom from './pages/ChatRoom';

<Route path="/chat" element={<ChatList />} />
<Route path="/chat/:id" element={<ChatRoom />} />
```

---

## ✅ Funcionalidades

- ✅ Criar conversa ao clicar em anúncio
- ✅ Listar todas as conversas
- ✅ Ver mensagens em tempo real (polling)
- ✅ Enviar mensagens
- ✅ Marcar como lidas automaticamente
- ✅ Contador de não lidas
- ✅ Badge de notificação

## 🚀 Melhorias Futuras

- WebSocket para mensagens em tempo real
- Notificações push
- Upload de imagens no chat
- Histórico de mensagens paginado

---

**Sistema de chat completo e funcional!** 💬🎉
