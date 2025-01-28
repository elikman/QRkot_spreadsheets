from app.models import Donation

from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    ...


donation_crud = CRUDCharityProject(Donation)
