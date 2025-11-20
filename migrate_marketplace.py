#!/usr/bin/env python3
"""
Script para adicionar colunas ao marketplace
"""
from sqlalchemy import create_engine, text
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

def migrate():
    print("Adicionando colunas ao marketplace...")
    
    with engine.connect() as conn:
        try:
            # Adicionar coluna tipo
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS tipo VARCHAR(20)"))
            print("[OK] Coluna 'tipo' adicionada")
            
            # Adicionar coluna raca
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS raca VARCHAR(100)"))
            print("[OK] Coluna 'raca' adicionada")
            
            # Adicionar coluna idade
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS idade INTEGER"))
            print("[OK] Coluna 'idade' adicionada")
            
            # Adicionar coluna producao_diaria
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS producao_diaria FLOAT"))
            print("[OK] Coluna 'producao_diaria' adicionada")
            
            # Adicionar coluna imagem_url
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS imagem_url VARCHAR(500)"))
            print("[OK] Coluna 'imagem_url' adicionada")
            
            # Adicionar coluna contato
            conn.execute(text("ALTER TABLE anuncios ADD COLUMN IF NOT EXISTS contato VARCHAR(100)"))
            print("[OK] Coluna 'contato' adicionada")
            
            # Atualizar registros existentes
            conn.execute(text("UPDATE anuncios SET tipo = 'venda' WHERE tipo IS NULL"))
            print("[OK] Registros existentes atualizados")
            
            # Tornar tipo obrigatório
            conn.execute(text("ALTER TABLE anuncios ALTER COLUMN tipo SET NOT NULL"))
            print("[OK] Coluna 'tipo' configurada como NOT NULL")
            
            # Criar índice
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_anuncios_tipo ON anuncios(tipo)"))
            print("[OK] Indice criado")
            
            conn.commit()
            print("\n[SUCESSO] Migracao concluida!")
            
        except Exception as e:
            print(f"\n[ERRO] Migracao falhou: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
