from typing import Optional

from sqlalchemy import select, func, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_faster_closed_projects(
            self,
            session: AsyncSession
    ):
        projects = await session.execute(
            select(
                self.model.name,
                self.model.close_date,
                self.model.create_date,
                self.model.description,
            ).where(
                self.model.fully_invested.is_(True)
            ).order_by(asc(
                func.extract('day', self.model.close_date) -
                func.extract('day', self.model.create_date)
            ))
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
