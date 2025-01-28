from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractModel


class Donation(AbstractModel):
    """Модель пожертвований."""

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f", user_id={self.user_id}, comment={self.comment[:50]}...)>"
        )
