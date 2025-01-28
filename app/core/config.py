from typing import Optional
from pydantic import BaseSettings, EmailStr


MIN_PASSWORD_LENGTH = 3

TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

USER_ROLE = 'user'

WRITER_ROLE = 'writer'

FUNDRAISING_DURATION = 'duration'


class Settings(BaseSettings):
    """
    Класс настроек приложения. Данные берутся из переменных окружения
    или подставляются значения по умолчанию.
    """

    app_title: str = 'Cat Charitable Foundation'

    description: str = 'Service to support cats!'

    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    secret: str = 'SECRET'

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    gapi_type: Optional[str] = None
    gapi_project_id: Optional[str] = None
    gapi_private_key_id: Optional[str] = None
    gapi_private_key: Optional[str] = None
    gapi_client_email: Optional[str] = None
    gapi_client_id: Optional[str] = None
    gapi_auth_uri: Optional[str] = None
    gapi_token_uri: Optional[str] = None
    gapi_auth_provider_x509_cert_url: Optional[str] = None
    gapi_client_x509_cert_url: Optional[str] = None

    class Config:
        """
        Класс конфигурации Pydantic для настройки переменных окружения.
        """

        env_file = '.env'
        env_prefix = 'FUND_APP_'


settings = Settings()
