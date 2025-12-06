from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Anuncio(Base):
    __tablename__ = "anuncios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    descricao = Column(Text)
    tipo = Column(String(20), nullable=False, index=True)  # venda, procura
    categoria = Column(String(50), nullable=False, index=True)  # vaca, equipamento, insumo
    raca = Column(String(100))
    idade = Column(Integer)  # em meses
    producao_diaria = Column(Float)  # litros/dia
    preco = Column(Float, nullable=False, index=True)
    imagem_url = Column(String(500))
    foto = Column(String(500))
    contato = Column(String(100))
    localizacao = Column(String(200))
    ativo = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    user = relationship("User")