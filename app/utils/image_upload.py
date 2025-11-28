"""
Sistema de upload de imagens com fallback automático:
- Tenta usar Firebase Storage se configurado
- Usa armazenamento local se Firebase não disponível
"""
import os

# Verificar se Firebase está disponível
FIREBASE_AVAILABLE = False
try:
    from .firebase_storage import upload_image as firebase_upload, delete_image as firebase_delete
    if os.path.exists(os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")):
        FIREBASE_AVAILABLE = True
        print("✅ Firebase Storage ativado")
except Exception as e:
    print(f"⚠️ Firebase não disponível: {e}")

# Importar armazenamento local como fallback
from .local_storage import upload_image_local, delete_image_local

def upload_image(file_content: bytes, content_type: str, user_id: int, entity_type: str, entity_id: int) -> str:
    """Upload de imagem (Firebase ou local)"""
    if FIREBASE_AVAILABLE:
        return firebase_upload(file_content, content_type, user_id, entity_type, entity_id)
    else:
        print("📁 Usando armazenamento local")
        return upload_image_local(file_content, content_type, user_id, entity_type, entity_id)

def delete_image(image_url: str):
    """Deletar imagem (Firebase ou local)"""
    if FIREBASE_AVAILABLE and not image_url.startswith("/uploads/"):
        return firebase_delete(image_url)
    else:
        return delete_image_local(image_url)
