from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.models.investment import Investment
from app.core.db import Base


class Donation(Investment, Base):
    """Модель пожертвования."""

    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    user = relationship("User", backref="donations")

    def __repr__(self) -> str:
        """Строковое представление объекта Donation."""
        return (
            f"< Donation(id={self.id}, user_id={self.user_id}, "
            f"amount={self.full_amount}) >"
        )

    __mapper_args__ = {
        'inherit_condition': text("Investment.id == Donation.id")
    }
