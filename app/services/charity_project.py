from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.models.charity_project import CharityProject
from app.services.investing import distribute_investments
from app.api.validators import (
    check_name_dublicate,
    check_charity_project_exists,
    check_project_closed,
    check_invested_sum,
    check_alredy_invested,
)


async def get_all_charity_projects_service(
        session: AsyncSession
) -> List[CharityProject]:
    """Получает список всех благотворительных проектов."""
    return await charity_project_crud.get_multi(session)


async def create_charity_project_service(
    obj_in: CharityProjectCreate, session: AsyncSession
) -> CharityProject:
    """Создаёт новый благотворительный проект и распределяет инвестиции."""
    await check_name_dublicate(obj_in.name, session)
    new_charity_project = await charity_project_crud.create(
        obj_in, session, commit=False)
    await distribute_funds(new_charity_project, session)

    await session.commit()
    await session.refresh(new_charity_project)

    return new_charity_project


async def distribute_funds(
        project: CharityProject, session: AsyncSession
) -> None:
    """Распределяет инвестиции для благотворительного проекта."""
    fill_models = await donation_crud.get_not_full_invested(session)
    sources = distribute_investments(project, fill_models)
    session.add_all(sources)


async def update_charity_project_service(
    project_id: int, obj_in: CharityProjectUpdate, session: AsyncSession
) -> CharityProject:
    """Обновляет данные благотворительного проекта."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_closed(charity_project.fully_invested)

    if obj_in.name:
        await check_name_dublicate(obj_in.name, session)

    if obj_in.full_amount:
        check_invested_sum(charity_project.invested_amount, obj_in.full_amount)
        if obj_in.full_amount == charity_project.invested_amount:
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()

    return await charity_project_crud.update(charity_project, obj_in, session)


async def delete_charity_project_service(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Удаляет благотворительный проект (если не было инвестиций)."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_alredy_invested(charity_project.invested_amount)

    return await charity_project_crud.remove(charity_project, session)
