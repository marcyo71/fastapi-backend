from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas, models
from app.models.transaction import Transaction

# -------------------------------
# CREATE Transaction
# -------------------------------
def create_transaction(db: Session, tx: schemas.TransactionOut) -> Transaction:
    new_tx = Transaction(
        user_id=tx.user_id,
        amount=tx.amount,
        timestamp=tx.timestamp
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx

# -------------------------------
# GET Transactions
# -------------------------------
def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).order_by(Transaction.timestamp.desc()).offset(skip).limit(limit).all()

def get_transaction_by_id(db: Session, tx_id: int):
    return db.query(Transaction).filter(Transaction.id == tx_id).first()

# ---------------------------
# PLAN CRUD
# ---------------------------
def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = models.Plan(
        name=plan.name,
        price=plan.price
        # aggiungi features/interval se li hai nel modello e schema
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

def get_plans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Plan).offset(skip).limit(limit).all()

# ---------------------------
# USER CRUD
# ---------------------------
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# ---------------------------
# SUBSCRIPTION CRUD
# ---------------------------
def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    db_sub = models.Subscription(
        user_id=subscription.user_id,
        plan_id=subscription.plan_id,
        start_date=datetime.utcnow(),
        status="attivo"  # default se non lo hai nello schema
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def get_subscriptions_by_user(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).all()

def cancel_subscription(db: Session, subscription_id: int):
    db_sub = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_sub:
        db_sub.status = "canceled"
        db_sub.end_date = datetime.utcnow()
        db.commit()
        db.refresh(db_sub)
    return db_sub