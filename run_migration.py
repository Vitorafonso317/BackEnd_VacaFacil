"""Script para executar migração do banco de dados"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def run_migration():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("Executando migracao...")
        
        # Adicionar coluna foto_url
        cursor.execute("ALTER TABLE vacas ADD COLUMN IF NOT EXISTS foto_url TEXT;")
        print("Coluna foto_url adicionada")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Migracao concluida com sucesso!")
        
    except Exception as e:
        print(f"Erro na migracao: {e}")

if __name__ == "__main__":
    run_migration()
