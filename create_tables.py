"""Script para criar tabelas no banco de dados"""
from app.database import engine, Base
from app.models import user, vaca, producao, subscription

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
