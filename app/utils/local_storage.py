import os
import time
import mimetypes
from io import BytesIO
from PIL import Image
from pathlib import Path

# Diretório para salvar uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIMES = ("image/jpeg", "image/png", "image/webp", "image/jpg")

def optimize_image(image_bytes: bytes, max_size=(800, 800)) -> bytes:
    """Redimensiona e otimiza imagem"""
    try:
        image = Image.open(BytesIO(image_bytes))
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        output = BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        return output.getvalue()
    except Exception as e:
        print(f"Erro ao otimizar imagem: {e}")
        return image_bytes

def upload_image_local(file_content: bytes, content_type: str, user_id: int, entity_type: str, entity_id: int) -> str:
    """Upload local de imagem"""
    # Validações
    if content_type not in ALLOWED_MIMES:
        raise ValueError("Tipo de arquivo não suportado")
    
    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError("Arquivo muito grande. Máximo 5MB")
    
    # Otimizar
    optimized_content = optimize_image(file_content)
    
    # Criar diretórios
    user_dir = UPLOAD_DIR / f"{entity_type}s" / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # Gerar nome
    ext = mimetypes.guess_extension(content_type) or ".jpg"
    timestamp = int(time.time())
    filename = f"{entity_type}-{entity_id}-{timestamp}{ext}"
    filepath = user_dir / filename
    
    # Salvar
    with open(filepath, "wb") as f:
        f.write(optimized_content)
    
    # Retornar URL relativa
    return f"/uploads/{entity_type}s/{user_id}/{filename}"

def delete_image_local(image_url: str):
    """Deletar imagem local"""
    try:
        # Remover /uploads/ do início
        path = image_url.replace("/uploads/", "")
        filepath = UPLOAD_DIR / path
        
        if filepath.exists():
            filepath.unlink()
            return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
    return False
