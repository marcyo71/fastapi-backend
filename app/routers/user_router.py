from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService
from app.services.user_status_service import UserStatusService   # <— MANCAVA QUESTO

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await UserService.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await UserService.create(db, data)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await UserService.update(db, user, data)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await UserService.delete(db, user)
    return {"detail": "User deleted"}


@router.patch("/{user_id}/status")
async def update_user_status(user_id: int, new_status: str, db: AsyncSession = Depends(get_db)):
    status = await UserStatusService.get_by_user(db, user_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    return await UserStatusService.update_status(db, status, new_status)

