from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
        project_id: Optional[int] = None
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session,
        project_id
    )
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exist(
        charity_project: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_before_delete(
        charity_project: CharityProject,
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект, '
                   'в который уже были инвестированы средства'
        )


def check_project_close(
        charity_project: CharityProject,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать или удалять'
        )
