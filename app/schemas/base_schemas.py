from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import PositiveInt


class BaseSchema(BaseModel):
    full_amount: PositiveInt
    invested_amount: Optional[int] = 0


class BaseDBSchema(BaseModel):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
