from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    pass
