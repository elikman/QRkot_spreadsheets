from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):

    id: int
    full_amount: PositiveInt = Field(
        ...,
        description='сумма должна быть больше ноля'
    )
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGet(DonationBase):

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None


class DonationPost(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        description='сумма должна быть больше ноля'
    )
    comment: Optional[str] = None
    invested_amount: Optional[int] = 0

    class Config:

        schema_extra = {
            'example': {
                'full_amount': 0,
                'comment': 'string'
            }
        }
