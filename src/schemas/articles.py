from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Article(BaseModel):
    id: int
    published_at: date
    title: str
    content: str
    tags: list[str] | None

class ArticleCreate(BaseModel):
    title: str = Field(min_length = 12, max_length = 64)
    content: str = Field(max_length = 320)
    tags: Optional[list[str]] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default = None, min_length = 12, max_length = 64)
    content: Optional[str] = Field(default = None, max_length = 320)
    tags: Optional[list[str]] = None