from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from .base import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_multi(
            self,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        select_ = select(self.model)
        if user and not user.is_superuser:
            select_ = select_.where(self.model.user_id == user.id)
        db_objs = await session.execute(select_)
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
