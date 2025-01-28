from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_before_delete,
                                check_charity_project_exist,
                                check_name_duplicate,
                                check_project_close)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectBase,
                                         CharityProjectGet,
                                         CharityProjectPatch)
from app.services import find_charity


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectGet],
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectGet,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_projects(
        charity_project: CharityProjectBase,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создаёт благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    session.add_all(
        find_charity(
            new_project,
            await donation_crud.get_all_not_fully_invested(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectGet,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exist(project_id, session)
    check_before_delete(charity_project)
    check_project_close(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectGet,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        project_id: int,
        obj_in: CharityProjectPatch,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exist(
        project_id, session
    )

    await check_name_duplicate(obj_in.name, session, project_id)
    check_project_close(charity_project)

    if obj_in.full_amount is not None:
        if charity_project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='нельзя установить требуемую сумму меньше уже вложенной'
            )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
