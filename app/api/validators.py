from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud


async def check_name_dublicate(project_name: str, session: AsyncSession):
    """
    Проверяет, существует ли проект с указанным названием.
    Если проект с таким именем уже существует, вызывается исключение
    HTTPException с ошибкой 400.

    :param project_name: Название проекта.
    :param session: Асинхронная сессия для работы с БД.
    """
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(project_id: int, session: AsyncSession):
    """
    Проверяет, существует ли благотворительный проект с заданным ID.
    Если проект не найден, вызывается исключение HTTPException с ошибкой 404.

    :param project_id: ID проекта для проверки.
    :param session: Асинхронная сессия для работы с БД.
    :return: Объект благотворительного проекта, если он существует.
    """
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Такого проекта не существует!",
        )
    return charity_project


def check_invested_sum(invested_amount: int, new_full_amount: int):
    """
    Проверяет, что новая сумма не меньше уже вложенной.
    Если новая сумма меньше уже вложенной, вызывает исключение HTTPException
    с ошибкой 400.

    :param invested_amount: Уже вложенная сумма.
    :param new_full_amount: Новая полная сумма для проекта.
    """
    if invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            ),
        )


def check_project_closed(fully_invested: bool):
    """
    Проверяет, не закрыт ли проект.
    Если проект закрыт, вызывает исключение HTTPException с ошибкой 400.

    :param fully_invested: Флаг, указывающий, закрыт ли проект.
    """
    if fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )


def check_alredy_invested(invested: bool):
    """
    Проверяет, были ли внесены средства в проект.
    Если средства уже внесены, вызывает исключение HTTPException с ошибкой 400.

    :param invested: Сумма вложенных средств.
    """
    if invested > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
