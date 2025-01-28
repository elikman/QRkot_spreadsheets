from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investment import invest_donation

router = APIRouter()


@router.post(
    "/",
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationUser:
    """Создание нового пожертвования.
    Только для зарегистрированных пользователей."""
    new_donation = await donation_crud.create(donation, session, user)
    await invest_donation(new_donation, CharityProject, session)
    return new_donation


@router.get(
    "/",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationDB]:
    """Получение всех пожертвований.
    Только для суперпользователя."""
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=List[DonationUser],
    response_model_exclude={"user_id"},
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> List[DonationUser]:
    """Отображение всех пожертвований текущего пользователя."""
    return await donation_crud.get_all_donations_user(
        session=session, user=user
    )
