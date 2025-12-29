import sys
from pathlib import Path

# Aggiunge la root del progetto al PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

from app.config.settings import settings
from app.db.base import Base

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dei modelli
target_metadata = Base.metadata

# URL del DB
DATABASE_URL = settings.database_url


# 🔥 AGGIUNTA: include_object per evitare migrazioni sporche
def include_object(object, name, type_, reflected, compare_to):
    # Ignora tabelle di sistema PostgreSQL
    if type_ == "table" and name.startswith("pg_"):
        return False

    # Ignora differenze spurie sui default generati dal DB
    if type_ == "column":
        if object.server_default and compare_to is not None:
            return False

    return True


def run_migrations_offline() -> None:
    """Esecuzione offline (senza connessione)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,   # 🔥 AGGIUNTA
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Esecuzione online (async)."""
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_object=include_object,   # 🔥 AGGIUNTA
    )

    with context.begin_transaction():
        context.run_migrations()


def main() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


main()
