from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud import charity_crud
from app.models import CharityProject
from app.services.money_flow import to_close


async def check_project_name_duplicate(
    name: str, session: AsyncSession
) -> None:
    project_id = await charity_crud.get_project_id_by_name(name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='The project not found!'
        )
    return charity_project


async def check_charity_project_closed(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_crud.get(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_new_full_amount(full_amount: int, model: Base) -> None:
    """Will close the product if new full_amount equals invested_amount."""
    if full_amount < model.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='New full_amount is less then the invested_amount!'
        )
    if full_amount == model.invested_amount:
        to_close(model)
