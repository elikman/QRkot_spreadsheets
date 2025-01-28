from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='не должно быть пустым'
    )
    description: str = Field(
        ...,
        min_length=1,
        description='не должно быть пустым'
    )
    full_amount: PositiveInt = Field(
        ...,
        description='сумма должна быть больше ноля'
    )
    invested_amount: Optional[int] = 0

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'string',
                'description': 'string',
                'full_amount': 0
            }
        }


class CharityProjectPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = 'forbid'


class CharityProjectGet(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
