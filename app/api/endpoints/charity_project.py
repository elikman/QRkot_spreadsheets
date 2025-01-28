from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.services.charity_project_service import (
    create_project_service,
    delete_project_service,
    update_project_service,
    get_all_projects_service,
)
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=(
        "Создать благотворительный проект "
        "(доступно только суперпользователям)."
    )
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание благотворительного проекта.  
    Доступно только для суперпользователей.
    """
    new_project = await create_project_service(project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить список всех благотворительных проектов."
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех благотворительных проектов.
    """
    return await get_all_projects_service(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Удалить благотворительный проект (только для суперпользователей)."
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление благотворительного проекта.
    Нельзя удалить проект, в который уже внесены средства — его можно только 
    закрыть.
    Доступно только для суперпользователей.
    """
    charity_project = await delete_project_service(project_id, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Обновить благотворительный проект (
    "только для суперпользователей)."
)
async def update_charity_project(
    project_id: int,
    new_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление благотворительного проекта.  
    Нельзя изменять закрытые проекты или устанавливать сумму меньше уже 
    вложенных средств.
    Доступно только для суперпользователей.
    """
    charity_project = await update_project_service(project_id, new_data,
                                                   session)
    return charity_project
