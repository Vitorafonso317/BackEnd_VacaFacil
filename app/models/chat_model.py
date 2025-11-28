from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Conversation(Base):
    """Conversa entre comprador e vendedor"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    anuncio_id = Column(Integer, ForeignKey("anuncios.id", ondelete="CASCADE"), nullable=False)
    comprador_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    anuncio = relationship("Anuncio")
    comprador = relationship("User", foreign_keys=[comprador_id])
    vendedor = relationship("User", foreign_keys=[vendedor_id])
    mensagens = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """Mensagem individual no chat"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mensagem = Column(Text, nullable=False)
    lida = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    conversation = relationship("Conversation", back_populates="mensagens")
    sender = relationship("User")
