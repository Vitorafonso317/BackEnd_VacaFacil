from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MessageCreate(BaseModel):
    conversation_id: int
    mensagem: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    mensagem: str
    lida: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    anuncio_id: int

class ConversationResponse(BaseModel):
    id: int
    anuncio_id: int
    comprador_id: int
    vendedor_id: int
    created_at: datetime
    ultima_mensagem: Optional[str] = None
    mensagens_nao_lidas: int = 0
    
    class Config:
        from_attributes = True

class ConversationDetail(ConversationResponse):
    mensagens: List[MessageResponse] = []
