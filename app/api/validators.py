from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


NAME_DUPLICATE = 'Проект с таким именем уже существует!'
DELETION_OR_MODIFICATION_ERROR = (
    'Удалять или модифицировать закрытые проекты запрещено!'
)
FULL_AMOUNT_LESS_THAN_INVESTED_AMOUNT = (
    'Требуемая сумма не может быть меньше внесенной!'
)
INVESTED_AMOUNT_ISNT_EMPTY = (
    'В проекте имеются инвестиции!'
)


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_DUPLICATE,
        )


def check_fully_invested(
        obj: CharityProject
) -> None:
    if obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DELETION_OR_MODIFICATION_ERROR,
        )


def check_full_amount_less_than_invested_amount(
        new_full_amount: int,
        invested_amount: int
) -> None:
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_AMOUNT_LESS_THAN_INVESTED_AMOUNT,
        )


def check_empty_invested_amount(
        invested_amount: int
) -> None:
    if invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_AMOUNT_ISNT_EMPTY,
        )
