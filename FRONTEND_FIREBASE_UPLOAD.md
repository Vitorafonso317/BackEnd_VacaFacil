# 📸 Frontend - Upload de Fotos com Firebase Storage

## 🎯 Endpoints Disponíveis

### 1. Upload de Foto da Vaca
```
POST /vacas/{vaca_id}/upload-foto
Content-Type: multipart/form-data
Body: foto (file)
```

### 2. Deletar Foto da Vaca
```
DELETE /vacas/{vaca_id}/foto
```

---

## 🚀 Implementação no Frontend

### 1. Criar componente de upload

```jsx
// components/ImageUpload.jsx
import { useState } from 'react';
import api from '../services/api';

export default function ImageUpload({ vacaId, currentImage, onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(currentImage);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validações
    if (!file.type.startsWith('image/')) {
      alert('Por favor, selecione uma imagem');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert('Imagem muito grande. Máximo 5MB');
      return;
    }

    // Preview
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);

    // Upload
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('foto', file);

      const response = await api.post(
        `/vacas/${vacaId}/upload-foto`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      onUploadSuccess(response.data.foto_url);
      alert('Foto enviada com sucesso!');
    } catch (error) {
      console.error('Erro ao enviar foto:', error);
      alert(error.response?.data?.detail || 'Erro ao enviar foto');
      setPreview(currentImage);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Deseja remover a foto?')) return;

    try {
      await api.delete(`/vacas/${vacaId}/foto`);
      setPreview(null);
      onUploadSuccess(null);
      alert('Foto removida com sucesso!');
    } catch (error) {
      console.error('Erro ao remover foto:', error);
      alert('Erro ao remover foto');
    }
  };

  return (
    <div className="space-y-4">
      {/* Preview */}
      {preview && (
        <div className="relative w-full h-64 bg-gray-100 rounded-lg overflow-hidden">
          <img
            src={preview}
            alt="Preview"
            className="w-full h-full object-cover"
          />
          <button
            onClick={handleDelete}
            className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600"
          >
            🗑️
          </button>
        </div>
      )}

      {/* Upload Button */}
      <label className="block">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
        />
        <div className="cursor-pointer bg-green-500 text-white px-4 py-2 rounded-lg text-center hover:bg-green-600 disabled:bg-gray-400">
          {uploading ? 'Enviando...' : preview ? 'Trocar Foto' : '📷 Adicionar Foto'}
        </div>
      </label>

      {/* Info */}
      <p className="text-sm text-gray-500">
        Formatos: JPG, PNG, WebP • Máximo: 5MB
      </p>
    </div>
  );
}
```

### 2. Usar no formulário de vaca

```jsx
// pages/CattleForm.jsx
import { useState } from 'react';
import ImageUpload from '../components/ImageUpload';

export default function CattleForm({ vaca }) {
  const [fotoUrl, setFotoUrl] = useState(vaca?.foto_url);

  return (
    <form>
      {/* Outros campos... */}
      
      <div className="mb-4">
        <label className="block text-gray-700 mb-2">Foto da Vaca</label>
        <ImageUpload
          vacaId={vaca?.id}
          currentImage={fotoUrl}
          onUploadSuccess={(url) => setFotoUrl(url)}
        />
      </div>

      {/* Botão salvar... */}
    </form>
  );
}
```

### 3. Exibir na listagem

```jsx
// components/CattleCard.jsx
export default function CattleCard({ vaca }) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      {/* Foto */}
      <div className="w-full h-48 bg-gray-200 rounded-lg overflow-hidden mb-4">
        {vaca.foto_url ? (
          <img
            src={vaca.foto_url}
            alt={vaca.nome}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <span className="text-6xl">🐄</span>
          </div>
        )}
      </div>

      {/* Info */}
      <h3 className="font-bold text-lg">{vaca.nome}</h3>
      <p className="text-gray-600">{vaca.raca}</p>
      <p className="text-sm text-gray-500">
        {vaca.idade} anos • {vaca.peso}kg
      </p>
    </div>
  );
}
```

### 4. Upload com drag & drop (opcional)

```jsx
// components/ImageUploadDragDrop.jsx
import { useState, useRef } from 'react';

export default function ImageUploadDragDrop({ vacaId, onUploadSuccess }) {
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  const handleUpload = async (file) => {
    // Mesma lógica de upload...
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-8 text-center ${
        dragging ? 'border-green-500 bg-green-50' : 'border-gray-300'
      }`}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={(e) => handleUpload(e.target.files[0])}
        className="hidden"
      />
      
      <div className="text-gray-600">
        <p className="text-4xl mb-2">📷</p>
        <p>Arraste uma foto aqui ou</p>
        <button
          onClick={() => fileInputRef.current?.click()}
          className="text-green-500 underline"
        >
          clique para selecionar
        </button>
      </div>
    </div>
  );
}
```

### 5. Compressão de imagem no frontend (opcional)

```bash
npm install browser-image-compression
```

```jsx
import imageCompression from 'browser-image-compression';

const handleFileChange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  try {
    // Comprimir antes de enviar
    const options = {
      maxSizeMB: 1,
      maxWidthOrHeight: 1920,
      useWebWorker: true
    };
    
    const compressedFile = await imageCompression(file, options);
    
    // Enviar arquivo comprimido
    const formData = new FormData();
    formData.append('foto', compressedFile);
    
    await api.post(`/vacas/${vacaId}/upload-foto`, formData);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

---

## 📋 Configuração do Firebase

### 1. Criar projeto Firebase
1. Acesse https://console.firebase.google.com
2. Crie um novo projeto
3. Ative o Storage

### 2. Criar Service Account
1. Project Settings → Service Accounts
2. Generate New Private Key
3. Salve como `firebase-credentials.json` na raiz do backend

### 3. Configurar .env
```env
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
```

### 4. Instalar dependências no backend
```bash
pip install firebase-admin google-cloud-storage Pillow
```

### 5. Reiniciar servidor
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

---

## ✅ Funcionalidades Implementadas

- ✅ Upload de imagens (JPEG, PNG, WebP)
- ✅ Validação de tipo e tamanho (máx 5MB)
- ✅ Otimização automática (redimensiona para 800x800)
- ✅ Preview antes do upload
- ✅ Deletar foto
- ✅ URLs públicas do Firebase Storage
- ✅ Integração com modelo de Vaca

## 🚀 Melhorias Futuras

- Múltiplas fotos por vaca
- Galeria de fotos
- Crop de imagem
- Filtros e edição
- Upload em lote

---

**Sistema de upload completo e funcional!** 📸🎉
