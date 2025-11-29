# init_db.py
from database import Base, engine
import models  # importa i tuoi modelli, così Base li conosce

Base.metadata.create_all(bind=engine)
print("Tabelle create!")
