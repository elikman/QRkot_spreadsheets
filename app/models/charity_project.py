from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class CharityProject(Base):
    """Модель благотворительного проекта, которая может быть связана с
    инвестициями."""

    __tablename__ = 'charity_project'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    investment_id = Column(Integer, ForeignKey('investment.id'))

    investment = relationship("Investment", backref="charity_projects")

    def __repr__(self) -> str:
        """Строковое представление объекта CharityProject."""
        return f"<CharityProject(id={self.id}, name={self.name})>"
