from datetime import datetime

from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import Donation, CharityProject


def to_close(model: Base) -> None:
    """Закрывает проект или пожертвование."""
    model.close_date = datetime.now()
    model.fully_invested = True


async def __get_open_cases(model: Base, session: AsyncSession) -> list[Base]:
    case = await session.execute(
        select(model).where(model.fully_invested == false()))
    return case.scalars().all()


async def money_flow(session: AsyncSession) -> None:
    """Основная функция для взаиморасчетов."""
    projects = await __get_open_cases(CharityProject, session)
    donations = await __get_open_cases(Donation, session)
    for project in projects:
        for donation in donations:
            project_diff = project.full_amount - project.invested_amount
            donation_diff = donation.full_amount - donation.invested_amount
            if donation_diff > project_diff:
                project.invested_amount += project_diff
                donation.invested_amount += project_diff
                to_close(project)
            if donation_diff <= project_diff:
                project.invested_amount += donation_diff
                donation.invested_amount += donation_diff
                if donation_diff < project_diff:
                    to_close(donation)
                if donation_diff == project_diff:
                    to_close(project)
    await session.commit()
