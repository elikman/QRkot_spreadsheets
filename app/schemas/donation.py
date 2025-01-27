from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.schemas.shema_mixing import InvestmentDB


class DonationCreate(BaseModel):

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationsDB(InvestmentDB, DonationCreate):

    user_id: int
