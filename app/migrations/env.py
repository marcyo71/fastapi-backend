import sys
import os

# Aggiunge la root del progetto al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from app.models import Base

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context


# Alembic Config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dei modelli
target_metadata = Base.metadata

def run_migrations_offline():
    """Esegue le migrazioni in modalità offline."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Esegue le migrazioni in modalità online."""
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
