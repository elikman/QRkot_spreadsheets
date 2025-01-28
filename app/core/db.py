from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from typing import AsyncGenerator


class PreBase:
    @declared_attr
    def __tablename__(cls):
        """Возвращает имя таблицы в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает асинхронную сессию для работы с базой данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
