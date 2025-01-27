from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_by_user(
        self, user: User, session: AsyncSession
    ) -> list[Donation]:
        donations_by_user = await session.execute(
            select(Donation).where(user.id == Donation.user_id)
        )
        return donations_by_user.scalars().all()


donation_crud = CRUDDonation(Donation)
