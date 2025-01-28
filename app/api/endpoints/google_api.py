from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.charity_project import get_all_projects
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.schemas.google_api import ProjectReport
from app.services.google_api import (
    get_delete_service, get_projects_by_completion_rate,
    set_user_permissions, spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[ProjectReport],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Создание отчёта.
    Только для суперпользователя."""
    projects = await get_all_projects(session)
    projects = await get_projects_by_completion_rate(projects)
    spreadsheet_id = await spreadsheets_create(wrapper_services)

    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services)

    return projects


@router.get(
    "/",
    response_model=list[str],
    dependencies=[Depends(current_superuser)],
)
async def get_spreadsheets(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Получение списка всех отчётов на Google Диске.
    Только для суперпользователя."""
    spreadsheets = await get_delete_service(wrapper_services)
    for spreadsheet in spreadsheets:
        await set_user_permissions(spreadsheet["id"], wrapper_services)
    return [spreadsheet["name"] for spreadsheet in spreadsheets]


@router.delete(
    "/",
    response_model=list[str],
    dependencies=[Depends(current_superuser)],
)
async def delete_old_reports(
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Удаление старых отчётов, кроме последнего.
    Только для суперпользователя."""
    spreadsheets = await get_delete_service(wrapper_services)
    service = await wrapper_services.discover("drive", "v3")
    for spreadsheet in spreadsheets[1:]:
        await set_user_permissions(spreadsheet["id"], wrapper_services)
        await wrapper_services.as_service_account(
            service.files.delete(fileId=spreadsheet["id"])
        )
    return [spreadsheet["name"] for spreadsheet in spreadsheets[1:]]
