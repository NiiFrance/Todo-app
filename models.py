from typing import List, Optional
from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str]


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TodoOut(TodoBase):
    id: int
