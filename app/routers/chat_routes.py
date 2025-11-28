from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user_model import User
from app.models.chat_model import Conversation, Message
from app.models.marketplace_model import Anuncio
from app.schemas.chat_schemas import (
    ConversationCreate, ConversationResponse, ConversationDetail,
    MessageCreate, MessageResponse
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar nova conversa com vendedor"""
    # Buscar anúncio
    anuncio = db.query(Anuncio).filter(Anuncio.id == data.anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    
    # Não pode conversar consigo mesmo
    if anuncio.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode conversar com você mesmo")
    
    # Verificar se já existe conversa
    existing = db.query(Conversation).filter(
        Conversation.anuncio_id == data.anuncio_id,
        Conversation.comprador_id == current_user.id
    ).first()
    
    if existing:
        return existing
    
    # Criar nova conversa
    conversation = Conversation(
        anuncio_id=data.anuncio_id,
        comprador_id=current_user.id,
        vendedor_id=anuncio.user_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todas as conversas do usuário"""
    conversations = db.query(Conversation).filter(
        (Conversation.comprador_id == current_user.id) |
        (Conversation.vendedor_id == current_user.id)
    ).all()
    
    result = []
    for conv in conversations:
        # Última mensagem
        ultima_msg = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.created_at.desc()).first()
        
        # Mensagens não lidas
        nao_lidas = db.query(Message).filter(
            Message.conversation_id == conv.id,
            Message.sender_id != current_user.id,
            Message.lida == False
        ).count()
        
        conv_dict = {
            "id": conv.id,
            "anuncio_id": conv.anuncio_id,
            "comprador_id": conv.comprador_id,
            "vendedor_id": conv.vendedor_id,
            "created_at": conv.created_at,
            "ultima_mensagem": ultima_msg.mensagem if ultima_msg else None,
            "mensagens_nao_lidas": nao_lidas
        }
        result.append(conv_dict)
    
    return result

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de uma conversa com todas as mensagens"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Verificar se usuário faz parte da conversa
    if conversation.comprador_id != current_user.id and conversation.vendedor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    # Marcar mensagens como lidas
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != current_user.id,
        Message.lida == False
    ).update({"lida": True})
    db.commit()
    
    return conversation

@router.post("/messages", response_model=MessageResponse)
def send_message(
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar mensagem"""
    # Verificar se conversa existe
    conversation = db.query(Conversation).filter(
        Conversation.id == data.conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Verificar se usuário faz parte da conversa
    if conversation.comprador_id != current_user.id and conversation.vendedor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    # Criar mensagem
    message = Message(
        conversation_id=data.conversation_id,
        sender_id=current_user.id,
        mensagem=data.mensagem
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Contar mensagens não lidas"""
    count = db.query(Message).join(Conversation).filter(
        ((Conversation.comprador_id == current_user.id) |
         (Conversation.vendedor_id == current_user.id)),
        Message.sender_id != current_user.id,
        Message.lida == False
    ).count()
    
    return {"unread_count": count}
