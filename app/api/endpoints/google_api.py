from datetime import timedelta
from typing import Union

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_api import spreadsheets_create, set_user_permissions, spreadsheets_update_value

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service)
) -> Union[str, None]:
    """
    Генерация отчета о закрытых проектах в Google Sheets.
    
    Только для суперпользователей.
    """
    closed_projects = await charity_project_crud.get_projects_by_completion_rate(session)
    
    if not closed_projects:
        return None
    
    spreadsheet_id = await spreadsheets_create(wrapper_service)

    await set_user_permissions(spreadsheet_id, wrapper_service)

    table_data = [
        ['Название проекта', 'Время сбора (в днях)', 'Описание', 'Собранная сумма']
    ]

    for project in closed_projects:
        duration = (project.close_date - project.create_date).days
        table_data.append([
            project.name,
            duration,
            project.description,
            float(project.fully_invested)
        ])
    
    now_date = (await wrapper_service.as_user).get_now() + timedelta(hours=3)
    formatted_date = now_date.strftime('%Y/%m/%d %H:%M:%S')

    spreadsheets_update_value(
        spreadsheet_id, table_data, wrapper_service, f'Отчет на {formatted_date}'
    )

    return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
