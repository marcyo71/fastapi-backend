from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app import models

router = APIRouter(prefix="/user_status", tags=["user_status"])

class UserStatusCreate(BaseModel):
    user_id: int
    status: str

class UserStatusUpdate(BaseModel):
    status: str | None = None

class UserStatusResponse(BaseModel):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True

@router.post("/", response_model=UserStatusResponse)
def create_status(status: UserStatusCreate, db: Session = Depends(get_db)):
    db_status = models.UserStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.get("/", response_model=list[UserStatusResponse])
def list_status(db: Session = Depends(get_db)):
    return db.query(models.UserStatus).all()

@router.get("/{status_id}", response_model=UserStatusResponse)
def read_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(models.UserStatus).filter(models.UserStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

@router.put("/{status_id}", response_model=UserStatusResponse)
def update_status(status_id: int, status_update: UserStatusUpdate, db: Session = Depends(get_db)):
    status = db.query(models.UserStatus).filter(models.UserStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    for field, value in status_update.dict(exclude_unset=True).items():
        setattr(status, field, value)
    db.commit()
    db.refresh(status)
    return status

@router.delete("/{status_id}")
def delete_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(models.UserStatus).filter(models.UserStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(status)
    db.commit()
    return {"detail": "Status deleted"}
