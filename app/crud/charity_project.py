from datetime import timedelta
from typing import Optional, Union

from sqlalchemy import func, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import FUNDRAISING_DURATION
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                project_name == CharityProject.name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession
    ) -> list[dict[str, Union[str, timedelta]]]:
        """
        Provides closed projects sorted by fundraising duration.

        Columns:

        Project name - fundraising duration - project description
        """
        datetime_difference_in_days = (
            func.julianday(
                CharityProject.close_date
            ) - func.julianday(
                CharityProject.create_date
            )).label(FUNDRAISING_DURATION)
        closed_projects = await session.execute(
            select(
                CharityProject.name,
                datetime_difference_in_days,
                CharityProject.description
            ).where(
                CharityProject.fully_invested == true()
            ).order_by(FUNDRAISING_DURATION)
        )
        closed_projects = closed_projects.all()
        return closed_projects


charity_crud = CRUDCharityProject(CharityProject)
