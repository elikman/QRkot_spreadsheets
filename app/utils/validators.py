from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models import CharityProject
from app.utils.utils import (
    LOW_SUM, NO_DELETE_CLOSED_PROJECT, NO_DELETE_PROJECT,
    PROJECT_ALREADY_EXISTS, PROJECT_NOT_FOUND, ZERO
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка наличия проекта с таким же именем."""
    project_id = await project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_ALREADY_EXISTS,
        )


def check_project_amount(project: CharityProject, amount: int) -> None:
    """Проверка достаточности суммы инвестирования."""
    if project.invested_amount > amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=LOW_SUM,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта."""
    project = await project_crud.get_project_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PROJECT_NOT_FOUND
        )
    return project


def check_project_invested_amount(project: CharityProject) -> None:
    """Проверка закрытия проекта.
    Вызывается, если проект уже был инвестирован."""
    if project.invested_amount > ZERO:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_DELETE_PROJECT,
        )


def check_project_fully_invested(project: CharityProject) -> None:
    """Проверка закрытия проекта.
    Вызывается, если проект уже был полностью инвестирован."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NO_DELETE_CLOSED_PROJECT,
        )
