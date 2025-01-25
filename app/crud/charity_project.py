from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD для благотворительных проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получение ID проекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name,
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_charity_project_by_id(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получение проекта по ID."""
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id,
            )
        )
        db_project = db_project.scalars().first()
        return db_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, str]]:
        """
        Возвращает список завершённых проектов,
        отсортированный по времени выполнения.
        """
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        projects = projects.scalars().all()
        closed_projects = []
        for project in projects:
            closed_projects.append(
                {
                    'name': project.name,
                    'time': project.close_date - project.create_date,
                    'description': project.description,
                }
            )
        return sorted(closed_projects, key=lambda i: (i['time']))


crud_charity_project = CRUDCharityProject(CharityProject)
