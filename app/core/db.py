from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from app.core.config import settings
from typing import AsyncGenerator


class PreBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор для создания асинхронной сессии для работы с БД.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
