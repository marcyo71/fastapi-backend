import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

# 🔧 Fix per permettere ad Alembic di vedere la root del progetto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 📦 Carica il file .env dalla root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# 🧪 Debug
print("DEBUG: .env path =", env_path)
print("DEBUG: os.environ['DATABASE_URL'] =", os.environ.get("DATABASE_URL"))

# 🔗 Recupera DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL non trovato. Verifica il file .env nella root.")

# 🔧 Configurazione Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)
fileConfig(config.config_file_name)

# 📦 Import modelli
from backend.db.engine import Base
import backend.models

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
