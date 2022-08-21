from unittest import result
from fastapi import FastAPI, HTTPException, status
from models import *
from database import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()


todos = {
    "Work out",
    "Learn FastAPI",
    "Visit Egypt"
}


@app.get("/todos", status_code=status.HTTP_200_OK)
def get_todos():
    with Session(engine) as session:
        statement = select(Todo)
        result = session.exec(statement)
        return result.all()


@app.get("/todos/{id}")
def get_todo(id: int):
    try:
        with Session(engine) as session:
            statement = select(Todo).where(Todo.id == id)
            result = session.exec(statement).first()
            return result

    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def add_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.close()


@app.put("/todos/{id}")
def update_todo(id: int, todo: str):
    try:
        with Session(engine) as session:
            pass
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.delete("/todos/{id}")
def delete_todo(id: int):
    try:
        todos.pop(id)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
