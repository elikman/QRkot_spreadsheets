from sqlalchemy import Column, String, Text

from app.utils.utils import HUNDRED

from .base import AbstractModel


class CharityProject(AbstractModel):
    """Модель проекта."""

    name = Column(String(HUNDRED), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f", name={self.name}, description={self.description[:50]}...)>"
        )
