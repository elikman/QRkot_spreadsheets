from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, Investment


class Donation(Base, Investment):

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
