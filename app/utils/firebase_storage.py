import os
import time
import mimetypes
from io import BytesIO
from PIL import Image
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

load_dotenv()

# Inicializar Firebase (apenas uma vez)
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
    
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': bucket_name
        })
    else:
        print("⚠️ Firebase credentials não encontrado. Upload de imagens desabilitado.")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIMES = ("image/jpeg", "image/png", "image/webp", "image/jpg")

def optimize_image(image_bytes: bytes, max_size=(800, 800)) -> bytes:
    """Redimensiona e otimiza imagem"""
    try:
        image = Image.open(BytesIO(image_bytes))
        
        # Converter para RGB se necessário
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        # Redimensionar mantendo proporção
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Salvar otimizado
        output = BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        return output.getvalue()
    except Exception as e:
        print(f"Erro ao otimizar imagem: {e}")
        return image_bytes

def upload_image(file_content: bytes, content_type: str, user_id: int, entity_type: str, entity_id: int) -> str:
    """
    Upload de imagem para Firebase Storage
    
    Args:
        file_content: Conteúdo do arquivo em bytes
        content_type: MIME type (image/jpeg, image/png, etc)
        user_id: ID do usuário
        entity_type: Tipo da entidade (vaca, anuncio, etc)
        entity_id: ID da entidade
    
    Returns:
        URL pública da imagem
    """
    # Validações
    if content_type not in ALLOWED_MIMES:
        raise ValueError("Tipo de arquivo não suportado. Use JPEG, PNG ou WebP")
    
    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError("Arquivo muito grande. Máximo 5MB")
    
    # Otimizar imagem
    optimized_content = optimize_image(file_content)
    
    # Gerar nome único
    ext = mimetypes.guess_extension(content_type) or ".jpg"
    timestamp = int(time.time())
    filename = f"{entity_type}-{entity_id}-{timestamp}{ext}"
    path = f"{entity_type}s/{user_id}/{filename}"
    
    try:
        bucket = storage.bucket()
        blob = bucket.blob(path)
        
        # Upload
        blob.upload_from_string(optimized_content, content_type="image/jpeg")
        
        # Tornar público
        blob.make_public()
        
        return blob.public_url
    except Exception as e:
        raise Exception(f"Erro ao fazer upload: {str(e)}")

def delete_image(image_url: str):
    """Deletar imagem do Firebase Storage"""
    try:
        # Extrair path da URL
        bucket = storage.bucket()
        # Parse URL para pegar o path
        path = image_url.split(f"{bucket.name}/")[-1].split("?")[0]
        
        blob = bucket.blob(path)
        blob.delete()
        return True
    except Exception as e:
        print(f"Erro ao deletar imagem: {e}")
        return False
