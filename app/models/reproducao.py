from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Reproducao(Base):
    __tablename__ = "reproducoes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vaca_id = Column(Integer, ForeignKey("vacas.id"), nullable=False)
    tipo = Column(String, nullable=False)  # inseminacao, cobertura, parto
    data = Column(Date, nullable=False)
    data_prevista_parto = Column(Date)
    sucesso = Column(Boolean, default=None)
    observacoes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User")
    vaca = relationship("Vaca")