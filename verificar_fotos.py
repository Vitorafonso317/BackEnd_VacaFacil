"""Script para verificar fotos armazenadas no Firebase Storage"""
import firebase_admin
from firebase_admin import credentials, storage
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializar Firebase
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {'storageBucket': bucket_name})

def listar_fotos():
    """Lista todas as fotos no Firebase Storage"""
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    
    print("\n📸 FOTOS ARMAZENADAS NO FIREBASE STORAGE\n")
    print("=" * 80)
    
    count = 0
    for blob in blobs:
        count += 1
        size_mb = blob.size / (1024 * 1024)
        print(f"\n{count}. {blob.name}")
        print(f"   Tamanho: {size_mb:.2f} MB")
        print(f"   Tipo: {blob.content_type}")
        print(f"   Criado: {blob.time_created}")
        print(f"   URL: {blob.public_url}")
    
    print("\n" + "=" * 80)
    print(f"\n✅ Total: {count} foto(s) encontrada(s)\n")

if __name__ == "__main__":
    try:
        listar_fotos()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Verifique:")
        print("   1. Se o arquivo de credenciais existe")
        print("   2. Se FIREBASE_STORAGE_BUCKET está configurado no .env")
