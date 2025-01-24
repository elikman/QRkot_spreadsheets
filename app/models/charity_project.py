from sqlalchemy import (
    Column,
    String,
    Text
)

from .abstract_models import BaseFields


NAME_LENGTH = 100


class CharityProject(BaseFields):
    name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text)

    def __repr__(self):
        return (
            f'{self.name=} {super().__repr__()}'
        )
