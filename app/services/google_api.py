from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.google_client import FORMAT, PERMISSIONS_BODY, SPREADSHEET_BODY


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Gives your personal account access to the documents
    you create on the service account disk.
    """
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    closed_projects: list[dict],
    wrapper_services: Aiogoogle
) -> None:
    """Updates data in a report table."""
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
