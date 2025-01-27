from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.shema_mixing import InvestmentDB


class CharityProjectCreate(BaseModel):

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: PositiveInt

    @validator('name', 'description')
    def cannot_be_only_spaces(cls, value: str):
        if value.isspace():
            raise ValueError('The fields cannot be empty!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectCreate):

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(InvestmentDB, CharityProjectCreate):
    pass
