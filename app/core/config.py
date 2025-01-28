from typing import Optional

from pydantic import BaseSettings, EmailStr

"""Минимально допустимая длина пароля."""
MIN_PASSWORD_LENGTH = 3

FORMAT = '%Y/%m/%d %H:%M:%S'
USER = 'user'
WRITER = 'writer'
FUNDRAISING_DURATION = 'duration'


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'Благотворительный фонд кошек'
    description: str = 'Сервис для поддержки кошек!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    # Variables for Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'


settings = Settings()
