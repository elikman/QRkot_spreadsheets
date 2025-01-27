from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationsDB
from app.services.money_flow import money_flow


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    Returns the list of all donations.
    """
    return await donation_crud.get_multi(session)


@router.post('/', response_model=DonationDB, response_model_exclude_none=True)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Make a donation."""
    new_donation = await donation_crud.create(donation, session, user)
    await money_flow(session)
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationDB])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Return a list of donations from the user making the request."""
    return await donation_crud.get_donations_by_user(user, session)
