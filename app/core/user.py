import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings, MIN_PASSWORD_LENGTH
from app.core.db import get_async_session
from app.models import User
from app.schemas import UserCreate


logging.basicConfig(level=logging.INFO)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Предоставляет доступ к базе данных через SQLAlchemy.
    Используется как зависимость для объекта класса UserManager.
    """ 
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Определяет стратегию хранения токена JWT."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Проверяет введённый пароль на соответствие правилам безопасности."""
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason='Пароль должен быть не менее 3 символов.'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать адрес электронной почты.'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """После успешной регистрации пользователя."""
        logging.info(f'Пользователь {user.email} успешно зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """Возвращает экземпляр UserManager для управления пользователями."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
