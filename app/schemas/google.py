from pydantic import BaseModel

from app.schemas.charity_project import CharityProjectGet


class GoogleResponse(BaseModel):
    charity_projects: list[CharityProjectGet]
    link: str
