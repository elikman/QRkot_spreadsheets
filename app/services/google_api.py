from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.google_client import FORMAT, PERMISSIONS_BODY, SPREADSHEET_BODY


async def create_spreadsheet(wrapper_services: Aiogoogle) -> str:
    """Создает новую электронную таблицу Google."""
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    return response['spreadsheetId']


async def grant_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Предоставляет указанному пользователю разрешения на доступ к
    электронной таблице Google."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields='id'
        )
    )


async def update_spreadsheet_values(
    spreadsheet_id: str,
    closed_projects: list[dict],
    wrapper_services: Aiogoogle
) -> None:
    """Обновляет содержимое электронной таблицы Google с помощью данных
    проекта."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_body = [
        [f'Report dated {datetime.now().strftime(FORMAT)}'],
        ['Top projects by closing speed'],
        ['Project name', 'Fundraising duration', 'Description']
    ]
    for project in closed_projects:
        table_body.append((
            project['name'],
            str(timedelta(project['duration'])),
            project['description']
        ))
    updated_body = {
        'majorDimension': 'ROWS',
        'values': table_body
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E300',
            valueInputOption='USER_ENTERED',
            json=updated_body
        )
    )
