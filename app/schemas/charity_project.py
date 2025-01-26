from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator
from pydantic.types import PositiveInt

MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100
MIN_DESCRIPTION_LENGTH = 1


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=MIN_NAME_LENGTH,
                                max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=MIN_NAME_LENGTH,
                      max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть пустым')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
