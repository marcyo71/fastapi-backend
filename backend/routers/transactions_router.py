from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.engine import SessionLocal
from backend.models import Transaction

# Istanza del router
transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])

# Dependency per ottenere la sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: lista transazioni
@transactions_router.get("/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

# Endpoint: crea transazione
@transactions_router.post("/")
def create_transaction(amount: float, description: str, db: Session = Depends(get_db)):
    new_transaction = Transaction(amount=amount, description=description)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# Endpoint: dettaglio transazione
@transactions_router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

# Endpoint: elimina transazione
@transactions_router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
        return {"status": "deleted"}
    return {"error": "transaction not found"}
