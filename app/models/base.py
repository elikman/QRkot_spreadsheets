from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.utils.utils import ZERO


class AbstractModel(Base):
    """Абстрактная модель."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=ZERO)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, "
            f"full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount}, "
            f"fully_invested={self.fully_invested})>"
        )
