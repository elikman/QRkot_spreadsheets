from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint
from app.core.db import Base


class Investment(Base):
    """
    Модель инвестиции.

    Поля:
        full_amount (int): Полная сумма инвестиции.
        invested_amount (int): Уже инвестированная сумма.
        fully_invested (bool): Флаг, показывающий, закрыта ли инвестиция.
        create_date (datetime): Дата создания инвестиции.
        close_date (datetime): Дата закрытия инвестиции.
    """

    __tablename__ = 'investment'

    __table_args__ = (
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
        CheckConstraint(
            "invested_amount >= 0",
            name="check_invested_amount_non_negative"
        ),
    )

    full_amount = Column(
        Integer,
        nullable=False,
        doc="Полная сумма инвестиции, должна быть больше 0."
    )
    invested_amount = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Уже инвестированная сумма (не может быть отрицательной)."
    )
    fully_invested = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Статус: True, если инвестиция полностью распределена."
    )
    create_date = Column(
        DateTime,
        default=datetime.now,
        nullable=False,
        doc="Дата создания инвестиции."
    )
    close_date = Column(
        DateTime,
        nullable=True,
        doc="Дата закрытия инвестиции (если закрыта)."
    )
