from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import User
from app.schemas.donation import (
    DonationDBSchema,
    DonationCreateSchema,
    UserDonationDBSchema
)
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.services.investing_processes import investing_process


USER_DONATION_FIELDS = {
    'id',
    'full_amount',
    'comment',
    'create_date'
}


router = APIRouter()


@router.post(
    '/',
    response_model=UserDonationDBSchema,
    response_model_include=USER_DONATION_FIELDS,
    response_model_exclude_none=True,
)
async def create_donation(
        donation_data: DonationCreateSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(
        obj_in=donation_data,
        session=session,
        user=user
    )
    projects = await charity_project_crud.get_not_fully_invested_objects(
        session=session
    )
    projects = investing_process(
        target=donation,
        sources=projects
    )
    session.add_all(projects)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/',
    response_model=list[DonationDBSchema],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    donations = await donation_crud.get_multi(session=session)
    return donations


@router.get(
    '/my',
    response_model=list[UserDonationDBSchema],
    response_model_include=USER_DONATION_FIELDS,
    response_model_exclude_none=True,
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session=session, user=user)
    return donations
