from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """Схема создания пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationUser(DonationCreate):
    """Схема отображения пожертвования."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    """Схема базового пожертвования."""

    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    clode_date: Optional[datetime]
