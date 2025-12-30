# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from app.core.config import settings
from app.db.base import Base

# ---- CONFIG ----
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata per autogenerate
target_metadata = Base.metadata

# Sovrascrive sqlalchemy.url con quello preso dalle settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# ---- RUN MIGRATIONS ----
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# ---- ENTRYPOINT ----
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()