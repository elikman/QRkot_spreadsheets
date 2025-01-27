from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InvestmentDB(BaseModel):

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
