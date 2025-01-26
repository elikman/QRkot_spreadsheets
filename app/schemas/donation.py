from typing import Optional

from .base_schemas import BaseSchema, BaseDBSchema


class DonationCreateSchema(BaseSchema):
    comment: Optional[str] = None


class DonationDBSchema(DonationCreateSchema, BaseDBSchema):
    user_id: int


class UserDonationDBSchema(DonationCreateSchema, BaseDBSchema):
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'full_amount': 500,
                'comment': 'My donation',
                'create_date': '2024-09-25T13:27:29.873589'
            }
        }
