from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest_donation
from app.utils.validators import (check_name_duplicate, check_project_amount,
                                  check_project_exists,
                                  check_project_fully_invested,
                                  check_project_invested_amount)

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создание нового проекта.
    Только для суперпользователя."""
    await check_name_duplicate(charity_project.name, session)
    await project_crud.get_project_id_by_name(
        charity_project.name, session
    )
    new_project = await project_crud.create(charity_project, session)
    await invest_donation(new_project, Donation, session)
    return new_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Получение всех проектов."""
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Обновление проекта.
    Только для суперпользователя."""
    project = await check_project_exists(project_id, session)
    check_project_fully_invested(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_project_amount(project, obj_in.full_amount)

    project = await project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Удаление проекта.
    Только для суперпользователя."""
    project = await check_project_exists(project_id, session)
    check_project_invested_amount(project)
    project = await project_crud.remove(project, session)
    return project
