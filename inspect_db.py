from sqlalchemy import create_engine, inspect

# crea l'engine verso il tuo DB SQLite
engine = create_engine("sqlite:///app.db")

# crea l'inspector
insp = inspect(engine)

# ora puoi stampare le colonne
print(insp.get_columns("users"))
print(insp.get_columns("transactions"))
