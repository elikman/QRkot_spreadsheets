from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Класс для работы с проектами."""

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получение ID проекта по его имени."""
        return await self.get_by_field(
            CharityProject.name, project_name, session
        )

    async def get_project_by_id(
        self, project_id: int, session: AsyncSession
    ) -> Optional[CharityProject]:
        """Получение проекта по его ID."""
        return await self.get_by_field(CharityProject.id, project_id, session)


project_crud = CRUDCharityProject(CharityProject)
