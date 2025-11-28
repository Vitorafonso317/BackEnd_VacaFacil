from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contact_model import Contact
from app.schemas.contact_schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    """Criar nova mensagem de contato"""
    
    new_contact = Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    return new_contact
