from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.cattle_model import Vaca
from app.schemas.cattle_schemas import VacaCreate, VacaUpdate, VacaResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/vacas", tags=["vacas"])

@router.post("/", response_model=VacaResponse)
def create_vaca(
    vaca: VacaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_vaca = Vaca(**vaca.dict(), user_id=current_user.id)
    db.add(db_vaca)
    db.commit()
    db.refresh(db_vaca)
    return db_vaca

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
        raise HTTPException(status_code=404, detail="Vaca not found")
    
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
        raise HTTPException(status_code=404, detail="Vaca not found")
    
    for field, value in vaca_update.dict(exclude_unset=True).items():
        setattr(vaca, field, value)
    
    db.commit()
    db.refresh(vaca)
    return vaca

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
        raise HTTPException(status_code=404, detail="Vaca not found")
    
    db.delete(vaca)
    db.commit()
    return {"message": "Vaca deleted successfully"}