from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_investment_sum,
                                check_charity_project_no_investment,
                                check_name_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import crud_charity_project
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.utils.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание благотворительного проекта."""
    await check_name_exists(charity_project.name, session)
    await crud_charity_project.get_project_id_by_name(
        charity_project.name,
        session,
    )
    start_project = await crud_charity_project.create(
        charity_project,
        session,
    )
    await investment_process(
        start_project,
        Donation,
        session,
    )
    return start_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение всех благотворительных проектов."""
    all_projects = await crud_charity_project.get_all(
        session,
    )
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление благотворительного проекта."""
    project = await check_charity_project_exists(
        project_id,
        session,
    )
    check_charity_project_closed(project)
    if obj_in.name:
        await check_name_exists(
            obj_in.name,
            session,
        )
    if obj_in.full_amount is not None:
        check_charity_project_investment_sum(
            project,
            obj_in.full_amount,
        )

    charity_project = await crud_charity_project.update(
        project,
        obj_in,
        session,
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление благотворительного проекта."""
    project = await check_charity_project_exists(
        project_id,
        session,
    )
    check_charity_project_no_investment(
        project,
    )
    charity_project = await crud_charity_project.delete(
        project,
        session,
    )
    return charity_project
