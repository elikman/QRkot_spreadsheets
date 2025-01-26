from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    """Базовая модель для пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    """Модель для создания пожертвования."""

    id: int
    create_date: datetime

    class Config:
        """Конфигурация для DonationCreate."""

        orm_mode = True


class DonationDB(DonationCreate):
    """Модель для пожертвования, возвращаемая из базы данных."""

    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = Field(0)
    fully_invested: bool
    close_date: Optional[datetime]
