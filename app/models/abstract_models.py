from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    FetchedValue,
    CheckConstraint
)

from app.core.db import Base


DEFAULT_INVESTED_AMOUNT = 0


class BaseFields(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('0 <= invested_amount <= full_amount'),
    )
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, server_default=FetchedValue())

    def __repr__(self):
        return (
            f'{self.full_amount=} '
            f'{self.invested_amount=} '
            f'{self.create_date=} '
            f'{self.close_date=}'
        )
