from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_closed,
    check_new_full_amount,
    check_project_name_duplicate,
)
from app.crud import charity_crud
from app.services.money_flow import money_flow
from app.schemas import CharityProjectCreate, CharityProjectUpdate


async def create_project_service(project: CharityProjectCreate, session: AsyncSession):
    """Создает новый благотворительный проект."""
    await check_project_name_duplicate(project.name, session)
    new_project = await charity_crud.create(project, session)
    await money_flow(session)
    await session.refresh(new_project)
    return new_project


async def get_all_projects_service(session: AsyncSession):
    """Получает все благотворительные проекты из базы."""
    return await charity_crud.get_multi(session)


async def delete_project_service(project_id: int, session: AsyncSession):
    """Проверяет возможность удаления и удаляет проект."""
    charity_project = await check_charity_project_exists(project_id, session)

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, и его нельзя удалить!",
        )

    deleted_project = await charity_crud.remove(charity_project, session)
    return deleted_project


async def update_project_service(project_id: int, new_data: CharityProjectUpdate, session: AsyncSession):
    """Обновляет данные благотворительного проекта с проверками."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_closed(project_id, session)

    if new_data.name:
        await check_project_name_duplicate(name=new_data.name, session=session)
    if new_data.full_amount:
        await check_new_full_amount(new_data.full_amount, charity_project)

    updated_project = await charity_crud.update(charity_project, new_data, session)
    return updated_project
