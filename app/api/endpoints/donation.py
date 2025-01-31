from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import AllDotationsDB, DonationCreate, DonationDB
from app.services.donation import DonationService

router = APIRouter()


@router.get(
    "/",
    response_model=list[AllDotationsDB],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
    summary="Возвращает список всех пожертвований для суперюзеров",
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров. Возвращает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post("/", response_model=DonationDB, summary="Сделать пожертвование")
async def create_new_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    return await DonationService.create_donation(obj_in, session, user)


@router.get(
    "/my",
    response_model=list[DonationDB],
    summary="Вернуть список пожертвований текущего пользователя",
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_user(session, user)
