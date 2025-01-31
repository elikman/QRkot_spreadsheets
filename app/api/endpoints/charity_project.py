from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.charity_project import (create_charity_project_service,
                                          delete_charity_project_service,
                                          get_all_charity_projects_service,
                                          update_charity_project_service)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить список всех благотворительных проектов",
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await get_all_charity_projects_service(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
    summary="Создать новый благотворительный проект",
)
async def create_new_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Создаёт благотворительный проект."""
    return await create_charity_project_service(obj_in, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
    summary="Обновить данные благотворительного проекта",
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму
    меньше уже вложенной."""
    return await update_charity_project_service(project_id, obj_in, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
    summary="Удалить благотворительный проект",
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть."""
    return await delete_charity_project_service(project_id, session)
