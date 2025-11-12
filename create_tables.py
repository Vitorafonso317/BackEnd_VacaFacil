"""
Script para criar as tabelas do banco de dados
"""
from app.database import engine, Base
from app.models import user, vaca, producao, subscription, financeiro, reproducao, marketplace

def create_tables():
    """Criar todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_tables()