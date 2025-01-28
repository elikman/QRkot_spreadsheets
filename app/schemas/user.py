from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема просмотра пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема изменения пользователя."""

    pass
