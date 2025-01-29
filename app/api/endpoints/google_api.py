from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google import (
    grant_user_permissions,
    create_spreadsheet,
    update_spreadsheet_values,
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
    summary=(
        "Создание отчёта в Google таблице с закрытыми проектами,"
        "отсортированными по времени сбора средств",
        )
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> str:
    """
    Создание отчёта в Google таблицу
    с закрытыми проектами отсортированными
    по времени затраченному на сбор средств.
    Только для суперюзеров.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    spreadsheet_id, spreadsheet_url = await create_spreadsheet(
        wrapper_services)
    await grant_user_permissions(
        spreadsheet_id, wrapper_services)
    try:
        await update_spreadsheet_values(
            spreadsheet_id,
            projects,
            wrapper_services,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f"Произошла ошибка: {error}",
        )

    return spreadsheet_url
