from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas

# Inizializza le tabelle se non esistono
Base.metadata.create_all(bind=engine)

# Istanza FastAPI
app = FastAPI(title="Backend CRUD Demo", version="1.0.0")

# Dependency per gestire la sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Endpoint CRUD per Users
# -------------------------------

@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name, status=user.status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# -------------------------------
# Endpoint CRUD per Transactions
# -------------------------------

@app.post("/transactions/", response_model=schemas.TransactionRead)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Verifica che l'utente esista
    user = db.query(models.User).filter(models.User.id == tx.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    db_tx = models.Transaction(**tx.dict())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

@app.get("/transactions/{tx_id}", response_model=schemas.TransactionRead)
def read_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

@app.get("/transactions/", response_model=list[schemas.TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

# -------------------------------
# Healthcheck
# -------------------------------

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend FastAPI attivo"}

@app.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.name = user.name
    db_user.status = user.status
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": f"User {user_id} deleted"}

@app.put("/transactions/{tx_id}", response_model=schemas.TransactionRead)
def update_transaction(tx_id: int, tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for field, value in tx.dict().items():
        setattr(db_tx, field, value)
    db.commit()
    db.refresh(db_tx)
    return db_tx

@app.delete("/transactions/{tx_id}")
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    db_tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_tx)
    db.commit()
    return {"detail": f"Transaction {tx_id} deleted"}

