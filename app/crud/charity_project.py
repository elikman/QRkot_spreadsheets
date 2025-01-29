from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
        self, charity_project_name: str, session: AsyncSession
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == charity_project_name)
        )
        return db_charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        completion_rate = extract("epoch", CharityProject.close_date) - extract(
            "epoch", CharityProject.create_date
        )
        projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested)
            .order_by(completion_rate)
        )

        return projects.scalars().all()

    async def get_not_full_invested(self, session: AsyncSession):
        """Возвращает все проекты, которые не полностью инвестированы."""
        not_full_invested_projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == 0)
            .order_by(CharityProject.create_date)
        )
        return not_full_invested_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
