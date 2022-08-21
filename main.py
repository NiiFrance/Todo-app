from typing import List
from unittest import result
from fastapi import FastAPI, HTTPException, status, Depends
from models import *
from database import create_db_and_tables, engine, get_session
from sqlmodel import Session, select

app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/todos", status_code=status.HTTP_200_OK, response_model=List[TodoOut])
def get_todos(session: Session = Depends(get_session)):
    statement = select(Todo)
    result = session.exec(statement)
    return result.all()


@app.get("/todos/{id}", status_code=status.HTTP_200_OK, response_model=TodoOut)
def get_todo(id: int, session: Session = Depends(get_session)):
    try:
        result = session.get(Todo, id)
        return result

    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoOut)
def add_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    todo = Todo(**todo.dict())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    session.close()
    return todo


@app.put("/todos/{id}", response_model=TodoOut)
def update_todo(id: int, todo: TodoUpdate, session: Session = Depends(get_session)):

    result = session.query(Todo).get(id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    todo = todo.dict(exclude_unset=True)
    for key in todo:
        setattr(result, key, todo[key])
    session.commit()
    session.refresh(result)
    return result


@app.delete("/todos/{id}")
def delete_todo(id: int, session: Session = Depends(get_session)):

    result = session.get(Todo, id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    session.delete(result)
    session.commit()
    return result
