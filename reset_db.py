import os
from app.database import Base, engine
from app.models import User

# Cancella il file SQLite se esiste
if os.path.exists("test.db"):
    os.remove("test.db")
    print("Vecchio DB eliminato.")

# Ricrea le tabelle
Base.metadata.create_all(bind=engine)
print("Nuovo DB creato con tabella users.")
