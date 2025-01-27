from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_closed, check_charity_project_exists,
    check_new_full_amount, check_project_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_crud
from app.services.money_flow import money_flow
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    Creates a charity project.
    """
    await check_project_name_duplicate(project.name, session)
    new_project = await charity_crud.create(project, session)
    await money_flow(session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Returns the list of all projects."""
    return await charity_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    Deletes a project.

    You cannot delete a project in which funds have already been invested,
    it can only be closed
    """
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    charity_project = await charity_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    new_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    A closed project cannot be updated;
    you cannot set the required amount less than the amount already invested.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_closed(project_id, session)
    if new_data.name:
        await check_project_name_duplicate(name=new_data.name, session=session)
    if new_data.full_amount:
        await check_new_full_amount(new_data.full_amount, charity_project)
    charity_project = await charity_crud.update(
        charity_project, new_data, session
    )
    return charity_project
