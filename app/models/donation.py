from sqlalchemy import (
    Column,
    Text,
    Integer,
    ForeignKey
)

from .abstract_models import BaseFields


class Donation(BaseFields):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{self.user_id=} {super().__repr__()}'
        )
