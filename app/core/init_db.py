"""
Этот модуль управляет созданием первого суперпользователя в приложении.

При первом подключении к базе данных, если пользователи отсутствуют,
создается суперпользователь с учетными данными, указанными в переменных
окружения или в файле `config.py`.
"""

import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas import UserCreate

# Преобразование асинхронных генераторов в асинхронные контекстные менеджеры
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)


async def create_first_superuser():
    """
    Создаёт первого суперпользователя в базе данных, если такие отсутствуют.

    Используются данные суперпользователя из настроек приложения
    (`settings.SUPERUSER_EMAIL` и `settings.SUPERUSER_PASSWORD`).
    """
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            user_manager = get_user_manager(user_db)

            try:
                superuser_data = UserCreate(
                    email=EmailStr(settings.SUPERUSER_EMAIL),
                    password=settings.SUPERUSER_PASSWORD,
                    is_superuser=True,
                )
                await user_manager.create(superuser_data)
                print("Суперпользователь успешно создан.")
            except UserAlreadyExists:
                print("Суперпользователь уже существует.")
