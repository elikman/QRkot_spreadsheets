from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import crud_charity_project
from app.models import CharityProject


async def check_name_exists(
    project_name: str,
    session: AsyncSession,
):
    """Проверка, существует ли проект с таким именем."""
    project_id = await crud_charity_project.get_project_id_by_name(
        project_name,
        session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_charity_project_investment_sum(
    project: CharityProject,
    new_amount: int,
):
    """Проверка, что новая сумма не меньше уже вложенной."""
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить сумму, меньше уже вложенной!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
):
    """Проверка существования благотворительного проекта по ID."""
    project = await crud_charity_project.get_charity_project_by_id(
        project_id,
        session,
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return project


def check_charity_project_no_investment(
    charity_project: CharityProject,
):
    """Проверка, что в проект не были внесены средства перед удалением."""
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


def check_charity_project_closed(
    charity_project: CharityProject,
):
    """Проверка, что проект не закрыт (не завершён)."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
