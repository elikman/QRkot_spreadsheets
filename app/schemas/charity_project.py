from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""

    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        """Конфигурация для CharityProjectBase."""

        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(BaseModel):
    """Схема для создания проекта."""

    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        """Конфигурация для CharityProjectCreate."""

        min_anystr_length = 1


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта в базе данных."""

    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """Конфигурация для CharityProjectDB."""

        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта."""
