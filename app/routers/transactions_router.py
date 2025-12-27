from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.transaction_schema import TransactionCreate, TransactionRead
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionRead)
async def create_transaction(data: TransactionCreate, db: AsyncSession = Depends(get_db)):
    return await TransactionService.create(db, data)


@router.get("/{tx_id}", response_model=TransactionRead)
async def get_transaction(tx_id: int, db: AsyncSession = Depends(get_db)):
    tx = await TransactionService.get(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.get("/", response_model=list[TransactionRead])
async def get_all_transactions(db: AsyncSession = Depends(get_db)):
    return await TransactionService.get_all(db)

