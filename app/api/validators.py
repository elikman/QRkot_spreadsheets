from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_crud
from app.models import CharityProject


async def check_project_name_duplicate(
    name: str, session: AsyncSession
) -> None:
    """
    Проверяет, существует ли проект с таким же именем в базе данных.

    Если проект с указанным именем уже есть, функция выбрасывает исключение
    HTTPException
    с кодом 400 (Bad Request).

    Args:
        name (str): Имя благотворительного проекта для проверки на
        уникальность.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для
        взаимодействия с базой данных.

    Raises:
        HTTPException: Если проект с указанным именем уже существует.
    """
    project_id: Optional[int] = await charity_crud.get_project_id_by_name(
        name,
        session
        )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Проверяет, существует ли благотворительный проект с указанным ID в базе
    данных.

    Возвращает объект проекта, если он найден. Если проект отсутствует,
    выбрасывает исключение HTTPException с кодом 404 (Not Found).

    Args:
        project_id (int): ID благотворительного проекта для проверки
        существования.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для
        взаимодействия с базой данных.

    Returns:
        CharityProject: Объект найденного благотворительного проекта.

    Raises:
        HTTPException: Если проект с указанным ID не найден.
    """
    charity_project = await charity_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Благотворительный проект не найден!"
        )
    return charity_project


async def check_project_before_delete(project: CharityProject) -> None:
    """
    Проверяет, закрыт ли проект перед удалением.

    Если проект не закрыт, выбрасывает исключение HTTPException с кодом 400
    (Bad Request).

    Args:
        project (CharityProject): Объект благотворительного проекта, который
        проверяется.

    Raises:
        HTTPException: Если проект имеет некорректный статус и не может быть
        удалён.
    """
    if project.fully_invested is False:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя удалять проект, у которого есть незавершённые
                "инвестиции!"
                )
        )


async def check_invested_amount_is_zero(project: CharityProject) -> None:
    """
    Проверяет, была ли сумма инвестиций в проекте равна нулю.

    Если сумма инвестиций проекта больше нуля, то проект не может быть
    отредактирован,
    и выбрасывается HTTPException с кодом 400 (Bad Request).

    Args:
        project (CharityProject): Объект благотворительного проекта, который
        проверяется.

    Raises:
        HTTPException: Если сумма инвестиций проекта больше нуля.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Редактирование запрещено: уже вложены средства "
                f"в размере {project.invested_amount}."
            )
        )


async def check_investment_amount(
    project: CharityProject, full_amount: int
) -> None:
    """
    Проверяет корректность суммы полной стоимости проекта.

    Если указано значение `full_amount`, меньшее текущей уже вложенной суммы
    в проект, выбрасывается исключение HTTPException с кодом 422
    (Unprocessable Entity).

    Args:
        project (CharityProject): Объект благотворительного проекта для
        проверки.
        full_amount (int): Заданное значение полной стоимости проекта.

    Raises:
        HTTPException: Если `full_amount` меньше текущей вложенной суммы.
    """
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                "Сумма вложений не может быть уменьшена! Текущая вложенная "
                f"сумма: {project.invested_amount}. Укажите сумму не меньше "
                "текущих вложений."
            )
        )
