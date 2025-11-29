import sqlite3
import os

def check_payments_table():
    db_path = os.path.join(os.path.dirname(__file__), "app.db")
    print(f"🔍 Controllo il DB in: {db_path}")

    if not os.path.exists(db_path):
        print("❌ Il file app.db non esiste nel percorso indicato.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Mostra tutte le tabelle presenti
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📋 Tabelle trovate nel DB:", [t[0] for t in tables])

    # Controlla se la tabella payments esiste
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payments';")
    table_exists = cursor.fetchone()

    if table_exists:
        print("✅ La tabella 'payments' esiste.")
        cursor.execute("PRAGMA table_info(payments);")
        schema = cursor.fetchall()
        print("Schema della tabella payments:")
        for col in schema:
            print(col)
        cursor.execute("SELECT * FROM payments;")
        rows = cursor.fetchall()
        print("Dati nella tabella payments:")
        for row in rows:
            print(row)
    else:
        print("❌ La tabella 'payments' NON esiste.")

    conn.close()

if __name__ == "__main__":
    check_payments_table()
