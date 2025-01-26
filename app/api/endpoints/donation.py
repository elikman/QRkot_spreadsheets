from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import crud_donation
from app.models import CharityProject, User
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
from app.utils.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создание пожертвования и начало процесса инвестирования."""
    start_donation = await crud_donation.create(
        donation,
        session,
        user,
    )
    await investment_process(
        start_donation,
        CharityProject,
        session,
    )
    return start_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех пожертвований."""
    all_donations = await crud_donation.get_all(
        session,
    )
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationCreate],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получение пожертвований текущего пользователя."""
    donations = await crud_donation.get_by_user(
        session=session,
        user=user,
    )
    return donations
