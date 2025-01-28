from sqlalchemy import Column, String, Text

from app.models.investment import Investment, Base


class CharityProject(Investment, Base):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
