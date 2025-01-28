from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Text, Numeric, Date
from base import Base

from app.core.db import Base


class Investment(Base):
    """Модель для работы с информацией об инвестициях."""

    __tablename__ = 'investment'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        doc="Уникальный идентификатор инвестиции."
    )
    name = Column(
        String(255),
        nullable=False,
        doc="Название инвестиции."
    )
    description = Column(
        Text,
        nullable=True,
        doc="Описание инвестиции."
    )
    amount = Column(
        Numeric(15, 2),
        nullable=False,
        doc="Сумма инвестиции."
    )
    start_date = Column(
        Date,
        nullable=False,
        doc="Дата начала инвестиционного периода."
    )
    end_date = Column(
        Date,
        nullable=True,
        doc="Дата окончания инвестиционного периода (если известна)."
    )


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
