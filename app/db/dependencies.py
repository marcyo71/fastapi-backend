from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# ---- LIFECYCLE ----

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    print("🔌 DB connesso correttamente.")

async def close_db() -> None:
    await engine.dispose()
    print("🧹 Engine SQLAlchemy chiuso correttamente.")
