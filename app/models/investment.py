from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from app.core.db import Base

class Investment(Base):
    """Родительский класс для денежных объектов."""

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime)
