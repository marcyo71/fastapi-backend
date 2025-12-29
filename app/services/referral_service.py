from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.referral import Referral
from app.schemas.referral_schema import ReferralCreate


class ReferralService:

    @staticmethod
    async def create(db: AsyncSession, data: ReferralCreate) -> Referral:
        referral = Referral(**data.model_dump())
        db.add(referral)
        await db.commit()
        await db.refresh(referral)
        return referral

    @staticmethod
    async def get(db: AsyncSession, referral_id: int) -> Referral | None:
        result = await db.execute(
            select(Referral).where(Referral.id == referral_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Referral | None:
        result = await db.execute(
            select(Referral).where(Referral.code == code)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Referral]:
        result = await db.execute(select(Referral))
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, referral: Referral) -> None:
        await db.delete(referral)
        await db.commit()

