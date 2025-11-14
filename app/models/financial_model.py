from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False, index=True)
    categoria = Column(String(100), default="venda_leite", index=True)
    observacoes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User")

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False, index=True)
    categoria = Column(String(100), nullable=False, index=True)
    observacoes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User")