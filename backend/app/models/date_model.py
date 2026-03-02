from pydantic import BaseModel


class DateModel(BaseModel):
    id: int
    name: str
    description: str
    challenge: str
    dress_code: str
    date: str
