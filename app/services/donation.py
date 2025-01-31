from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate
from app.services.investing import distribute_investments


class DonationService:
    @staticmethod
    async def create_donation(
        obj_in: DonationCreate, session: AsyncSession, user: User):
        """Создание пожертвования с распределением средств."""
        new_donation = await donation_crud.create(
            obj_in, session, user, commit=False)
        fill_models = await charity_project_crud.get_not_full_invested(session)
        sources = distribute_investments(new_donation, fill_models)
        session.add_all(sources)
        await session.commit()
        await session.refresh(new_donation)
        return new_donation
