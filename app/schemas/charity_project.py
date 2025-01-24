from typing import Optional

from pydantic import BaseModel, Field, Extra
from pydantic.types import PositiveInt

from .base_schemas import BaseSchema, BaseDBSchema


MIN_LENGTH = 1
MAX_LENGTH = 100


class CharityProjectCreateSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH
    )
    description: str = Field(
        ...,
        min_length=MIN_LENGTH
    )

    class Config:
        extra = Extra.forbid


class CharityProjectUpdateSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDBSchema(CharityProjectCreateSchema, BaseDBSchema):
    pass
