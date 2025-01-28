from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Базовая модель для всех сущностей проекта."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Имя таблицы совпадает с названием класса, написанным в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url, future=True, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии для работы с базой данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
