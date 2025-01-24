from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectDBSchema,
    CharityProjectCreateSchema,
    CharityProjectUpdateSchema
)
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.api.validators import (
    check_name_duplicate,
    check_fully_invested,
    check_full_amount_less_than_invested_amount,
    check_empty_invested_amount
)
from app.services.investing_processes import investing_process


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        project_data: CharityProjectCreateSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    await check_name_duplicate(
        project_name=project_data.name,
        session=session
    )
    new_project = await charity_project_crud.create(
        obj_in=project_data,
        session=session
    )
    donations = await donation_crud.get_not_fully_invested_objects(
        session=session
    )
    donations = investing_process(
        target=new_project, sources=donations
    )
    session.add_all(donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDBSchema],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    projects = await charity_project_crud.get_multi(session=session)
    return projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        project_data: CharityProjectUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    db_project: CharityProject = await charity_project_crud.get(
        project_id, session
    )
    if project_data.name:
        await check_name_duplicate(
            project_name=project_data.name,
            session=session
        )
    check_fully_invested(db_project)
    if project_data.full_amount:
        check_full_amount_less_than_invested_amount(
            new_full_amount=project_data.full_amount,
            invested_amount=db_project.invested_amount
        )
    db_project: CharityProject = await charity_project_crud.update(
        db_obj=db_project,
        obj_in=project_data,
        session=session
    )
    return db_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    db_project: CharityProject = await charity_project_crud.get(
        project_id, session
    )
    check_fully_invested(db_project)
    check_empty_invested_amount(
        invested_amount=db_project.invested_amount
    )
    db_project: CharityProject = await charity_project_crud.remove(
        db_obj=db_project,
        session=session
    )
    return db_project
