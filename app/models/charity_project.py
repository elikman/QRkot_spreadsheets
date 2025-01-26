from sqlalchemy import Column, String, Text

from app.models.base import BaseModel

MAX_STRING_LENGTH = 100


class CharityProject(BaseModel):
    name = Column(String(MAX_STRING_LENGTH), unique=True, nullable=False)
    description = Column(Text)
