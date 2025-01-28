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
    """
    Проверяет, существует ли проект с указанным именем.

    Параметры:
    - name: имя проекта, которое необходимо проверить.
    - session: асинхронная сессия базы данных.

    Исключение:
    - HTTPException: если проект с таким именем уже существует.
    """
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
    """
    Проверяет, существует ли благотворительный проект с данным ID.

    Параметры:
    - project_id: ID проекта, который нужно проверить.
    - session: асинхронная сессия базы данных.

    Возвращает:
    - объект CharityProject: если проект существует.

    Исключение:
    - HTTPException: если проект не найден.
    """
    charity_project = await charity_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_closed(
    project_id: int,
    session: AsyncSession
) -> None:
    """
    Проверяет, закрыт ли благотворительный проект с данным ID.

    Параметры:
    - project_id: ID проекта, который нужно проверить.
    - session: асинхронная сессия базы данных.

    Исключение:
    - HTTPException: если проект закрыт.
    """
    charity_project = await charity_crud.get(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_new_full_amount(full_amount: int, model: Base) -> None:
    """
    Проверяет новый полный объём (full_amount) в сравнении с имеющимся объёмом.

    Параметры:
    - full_amount: новый полный объём, который нужно проверить.
    - model: модель, в которой хранится информация о уже инвестированных средствах.

    Исключение:
    - HTTPException: если новый полный объём меньше или равен инвестированному объёму.
    """
    if full_amount < model.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Новый полный объём меньше, чем инвестированный!'
        )
    if full_amount == model.invested_amount:
        to_close(model)
