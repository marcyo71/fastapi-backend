from sqlalchemy.orm import declarative_base
from app.backend.db.engine import Base, SessionLocal, engine

Base = declarative_base()

# Importa tutti i modelli per registrarli nel metadata
# Aggiungi qui altri modelli se ne hai (es. Survey, Payout, ecc.)
