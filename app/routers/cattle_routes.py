from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.cattle_model import Vaca
from app.schemas.cattle_schemas import VacaCreate, VacaUpdate, VacaResponse
from app.utils.dependencies import get_current_user
from app.utils.image_upload import upload_image, delete_image

router = APIRouter(prefix="/vacas", tags=["vacas"])

@router.post("/", response_model=VacaResponse)
def create_vaca(
    vaca: VacaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Verificar limites de assinatura
        from app.services.subscription_service import SubscriptionService
        subscription_service = SubscriptionService(db)
        
        current_count = db.query(Vaca).filter(Vaca.user_id == current_user.id).count()
        if not subscription_service.check_limits(current_user.id, "vacas", current_count + 1):
            raise HTTPException(
                status_code=403,
                detail="Limite de vacas atingido. Faça upgrade do seu plano."
            )
        
        db_vaca = Vaca(**vaca.dict(), user_id=current_user.id)
        db.add(db_vaca)
        db.commit()
        db.refresh(db_vaca)
        return db_vaca
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao criar vaca: {str(e)}"
        )

@router.post("/{vaca_id}/upload-foto")
async def upload_foto_vaca(
    vaca_id: int,
    foto: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload de foto da vaca"""
    # Verificar se vaca existe e pertence ao usuário
    vaca = db.query(Vaca).filter(
        Vaca.id == vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    try:
        # Ler conteúdo do arquivo
        content = await foto.read()
        
        # Deletar foto antiga se existir
        if vaca.foto_url:
            delete_image(vaca.foto_url)
        
        # Upload nova foto
        foto_url = upload_image(
            file_content=content,
            content_type=foto.content_type,
            user_id=current_user.id,
            entity_type="vaca",
            entity_id=vaca_id
        )
        
        # Atualizar banco
        vaca.foto_url = foto_url
        db.commit()
        db.refresh(vaca)
        
        return {"message": "Foto enviada com sucesso", "foto_url": foto_url}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@router.delete("/{vaca_id}/foto")
def delete_foto_vaca(
    vaca_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar foto da vaca"""
    vaca = db.query(Vaca).filter(
        Vaca.id == vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    if not vaca.foto_url:
        raise HTTPException(status_code=404, detail="Vaca não possui foto")
    
    try:
        delete_image(vaca.foto_url)
        vaca.foto_url = None
        db.commit()
        return {"message": "Foto removida com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao remover foto: {str(e)}")

@router.get("/", response_model=List[VacaResponse])
def get_vacas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = Query(None),
    raca: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Vaca).filter(Vaca.user_id == current_user.id)
    
    if search:
        query = query.filter(Vaca.nome.ilike(f"%{search}%"))
    if raca:
        query = query.filter(Vaca.raca == raca)
    if status:
        query = query.filter(Vaca.status == status)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{vaca_id}", response_model=VacaResponse)
def get_vaca(
    vaca_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vaca = db.query(Vaca).filter(
        Vaca.id == vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    return vaca

@router.put("/{vaca_id}", response_model=VacaResponse)
def update_vaca(
    vaca_id: int,
    vaca_update: VacaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vaca = db.query(Vaca).filter(
        Vaca.id == vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    try:
        for field, value in vaca_update.dict(exclude_unset=True).items():
            setattr(vaca, field, value)
        
        db.commit()
        db.refresh(vaca)
        return vaca
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar vaca: {str(e)}"
        )

@router.delete("/{vaca_id}")
def delete_vaca(
    vaca_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vaca = db.query(Vaca).filter(
        Vaca.id == vaca_id,
        Vaca.user_id == current_user.id
    ).first()
    
    if not vaca:
        raise HTTPException(status_code=404, detail="Vaca não encontrada")
    
    try:
        # Deletar foto se existir
        if vaca.foto_url:
            delete_image(vaca.foto_url)
        
        db.delete(vaca)
        db.commit()
        return {"message": "Vaca removida com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao remover vaca: {str(e)}"
        )
