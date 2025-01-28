from pydantic import BaseModel


class CompletionDuration(BaseModel):
    """Модель времени для создания отчета."""
    days: int
    hours: int
    minutes: int
    seconds: int


class ProjectReport(BaseModel):
    """Модель отчета о проекте."""
    name: str
    completion_duration: CompletionDuration
    description: str
