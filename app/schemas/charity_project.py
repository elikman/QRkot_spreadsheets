from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.utils.utils import HUNDRED, NOT_EMPTY_FIELD, ONE


class CharityProjectUpdate(BaseModel):
    """Схема изменения проекта."""

    name: str = Field(None, max_length=HUNDRED)
    description: str = Field(None)
    full_amount: PositiveInt = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = ONE


class CharityProjectCreate(CharityProjectUpdate):
    """Схема создания проекта."""

    name: str = Field(..., max_length=HUNDRED)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    @validator("name", "description")
    def validate_field(cls, value: str) -> str:
        """Проверка поля на пустоту."""
        if value is None or not value:
            raise ValueError(NOT_EMPTY_FIELD)
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема базового проекта."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
