from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class InvestmentBaseModel(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0 <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return (f'{type(self)}'
                f'{self.full_amount=}, '
                f'{self.invested_amount=}, '
                f'{self.fully_invested=}, '
                f'{self.create_date=}, '
                f'{self.close_date=}')
