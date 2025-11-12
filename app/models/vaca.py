from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Vaca(Base):
    __tablename__ = "vacas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome = Column(String, nullable=False)
    raca = Column(String, nullable=False)
    idade = Column(Integer)
    peso = Column(Float)
    producao_media = Column(Float)
    status = Column(String, default="ativa")
    observacoes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    owner = relationship("User", back_populates="vacas")
    producoes = relationship("Producao", back_populates="vaca")