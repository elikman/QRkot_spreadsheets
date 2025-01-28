from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
            project_id: Optional[int] = None,
    ) -> Optional[int]:

        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            ).where(
                CharityProject.id != project_id
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(True)
            ).order_by(self.model.close_date - self.model.create_date)

        )
        return db_objs.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
