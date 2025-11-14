from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Producao(Base):
    __tablename__ = "producoes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vaca_id = Column(Integer, ForeignKey("vacas.id", ondelete="CASCADE"), nullable=False)
    data = Column(Date, nullable=False)
    quantidade_manha = Column(Float, default=0)
    quantidade_tarde = Column(Float, default=0)
    quantidade_total = Column(Float)
    observacoes = Column(String)

    # Relacionamentos
    user = relationship("User")
    vaca = relationship("Vaca", back_populates="producoes")