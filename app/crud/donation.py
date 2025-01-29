from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_by_user(
            self, session: AsyncSession, user: User) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()

    async def get_not_full_invested(
            self, session: AsyncSession) -> list[Donation]:
        """Возвращает все донаты, которые не были полностью инвестированы."""
        not_full_invested_donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested == 0)
            .order_by(Donation.create_date)
        )

        return not_full_invested_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
