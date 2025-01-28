from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import Depends

from app.core.config import settings
from app.core.google_client import get_service
from app.utils.utils import (
    FORMAT, HOUR, LINK_GOOGLE_DOCS, MINUTES
)


def format_duration(duration) -> dict[str, int]:
    """Форматирование длительности проекта."""
    days = duration.days
    hours, remainder = divmod(duration.seconds, HOUR)
    minutes, seconds = divmod(remainder, MINUTES)
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
    }


def format_project_duration_for_table(duration) -> str:
    """Форматирование длительности проекта для таблицы."""
    return (
        f"{duration['days']} д., {duration['hours']} ч., "
        f"{duration['minutes']} мин., {duration['seconds']} сек."
    )


async def get_projects_by_completion_rate(projects) -> list:
    """Получение выполненных проектов с сортировкой по времени исполнения."""
    filtered_projects = [
        project
        for project in projects
        if project.close_date and project.fully_invested
    ]
    sorted_projects = sorted(
        filtered_projects,
        key=lambda project: project.close_date - project.create_date,
    )

    return [
        {
            "name": project.name,
            "completion_duration": format_duration(
                project.close_date - project.create_date
            ),
            "description": project.description,
        }
        for project in sorted_projects
    ]


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    """Назначение прав доступа на таблицу для пользователя."""
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание новой таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {
            "title": f"Отчёт на {now_date_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 11,
                    },
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    print(LINK_GOOGLE_DOCS + {response['spreadsheetId']})
    return response["spreadsheetId"]


async def spreadsheets_update_value(
    spreadsheet_id: str, sorted_projects: list, wrapper_services: Aiogoogle
) -> None:
    """Обновление значений в таблице."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for project in sorted_projects:
        collect_time = format_project_duration_for_table(
            project["completion_duration"]
        )
        new_row = [project["name"], collect_time, project["description"]]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1:C30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )


async def get_delete_service(
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, str]]:
    """Метод получения списка всех отчётов на Google Диске."""
    service = await wrapper_services.discover("drive", "v3")
    response = await wrapper_services.as_service_account(
        service.files.list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            fields="files(id, name, createdTime)",
        )
    )
    spreadsheets = response["files"]
    return spreadsheets
