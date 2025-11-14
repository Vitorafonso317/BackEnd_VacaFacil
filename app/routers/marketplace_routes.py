from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.marketplace_model import Anuncio
from app.schemas.marketplace_schemas import AnuncioCreate, AnuncioUpdate, AnuncioResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/marketplace", tags=["marketplace"])

@router.post("/", response_model=AnuncioResponse)
def create_anuncio(
    anuncio: AnuncioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_anuncio = Anuncio(**anuncio.dict(), user_id=current_user.id)
        db.add(db_anuncio)
        db.commit()
        db.refresh(db_anuncio)
        return db_anuncio
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar anúncio: {str(e)}")

@router.get("/", response_model=List[AnuncioResponse])
def get_anuncios(
    categoria: str = Query(None),
    search: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Anuncio).filter(Anuncio.ativo.is_(True))
    
    if categoria:
        query = query.filter(Anuncio.categoria == categoria)
    if search:
        search_param = f"%{search}%"
        query = query.filter(Anuncio.titulo.ilike(search_param))
    
    return query.offset(skip).limit(limit).all()

@router.get("/meus", response_model=List[AnuncioResponse])
def get_meus_anuncios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Anuncio).filter(Anuncio.user_id == current_user.id).all()

@router.put("/{anuncio_id}", response_model=AnuncioResponse)
def update_anuncio(
    anuncio_id: int,
    anuncio_update: AnuncioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        anuncio = db.query(Anuncio).filter(
            Anuncio.id == anuncio_id,
            Anuncio.user_id == current_user.id
        ).first()
        
        if not anuncio:
            raise HTTPException(status_code=404, detail="Anúncio não encontrado")
        
        for field, value in anuncio_update.dict(exclude_unset=True).items():
            setattr(anuncio, field, value)
        
        db.commit()
        db.refresh(anuncio)
        return anuncio
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar anúncio: {str(e)}")