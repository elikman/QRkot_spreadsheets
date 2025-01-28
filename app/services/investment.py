from datetime import datetime
from typing import Tuple, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.utils.utils import ZERO


async def sort_obj(
    session: AsyncSession, model: Union[CharityProject, Donation]
) -> list[Union[CharityProject, Donation]]:
    """Сортировка объектов по дате создания."""
    obj = await session.execute(
        select(model)
        .where(model.fully_invested == ZERO)
        .order_by(model.create_date)
    )
    return obj.scalars().all()


async def investment_close(
    obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Закрытие инвестирования."""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


async def investment(
    source_obj: Union[CharityProject, Donation],
    target_obj: Union[CharityProject, Donation],
) -> Tuple[Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    """Распределение инвестиций между проектами."""
    source_balance = source_obj.full_amount - source_obj.invested_amount
    target_balance = target_obj.full_amount - target_obj.invested_amount

    if source_balance > target_balance:
        source_obj.invested_amount += target_balance
        await investment_close(target_obj)
    elif source_balance == target_balance:
        await investment_close(source_obj)
        await investment_close(target_obj)
    else:
        target_obj.invested_amount += source_balance
        await investment_close(source_obj)
    return source_obj, target_obj


async def invest_donation(
    source_obj: Union[CharityProject, Donation],
    target_obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """Логика инвестирования пожертвований в проект."""
    sorted_source = await sort_obj(session, target_obj)
    for source in sorted_source:
        source_obj, source = await investment(source_obj, source)
        session.add(source_obj)
        session.add(source)
    await session.commit()
    await session.refresh(source_obj)
    return source_obj
