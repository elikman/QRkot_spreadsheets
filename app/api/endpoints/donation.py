from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, DonationGet, DonationPost
from app.services import find_charity


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationGet],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Возвращает список всех пожертвований."""
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.post(
    '/',
    response_model=DonationBase,
)
async def create_donation(
        donation: DonationPost,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    session.add_all(
        find_charity(
            new_donation,
            await charity_project_crud.get_all_not_fully_invested(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationBase],
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    all_donation = await donation_crud.get_multi(session, user)
    return all_donation
