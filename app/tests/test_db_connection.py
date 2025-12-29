import pytest
from app.db.dependencies import engine

@pytest.mark.asyncio
async def test_engine_connects():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
