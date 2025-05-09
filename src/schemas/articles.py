from pydantic import BaseModel
from datetime import date

class Article(BaseModel):
    id: int
    published_at: date
    title: str
    content: str
    tags: list[str]