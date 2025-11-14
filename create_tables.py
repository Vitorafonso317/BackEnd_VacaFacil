"""
Script para criar as tabelas do banco de dados
"""
import logging
from app.database import engine, Base
from app.models import user_model, cattle_model, production_model, subscription_model, financial_model, reproduction_model, marketplace_model

logging.basicConfig(level=logging.INFO)

def create_tables():
    """Criar todas as tabelas no banco de dados"""
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables()