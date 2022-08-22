from typing import List
from fastapi import FastAPI, HTTPException, status, Depends
from models import *
from database import create_db_and_tables, get_session
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@app.get('/')
async def index(token: str = Depends(oauth2_scheme)):
    return {'token': token}


@app.on_event("startup")
async def startup():
    create_db_and_tables()


@app.post('/token')
@app.get("/todos", status_code=status.HTTP_200_OK, response_model=List[TodoOut])
async def get_todos(session: Session = Depends(get_session)):
    statement = select(Todo)
    result = session.exec(statement)
    return result.all()


@app.get("/todos/{id}", status_code=status.HTTP_200_OK, response_model=TodoOut)
async def get_todo(id: int, session: Session = Depends(get_session)):
    try:
        result = session.get(Todo, id)
        return result

    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoOut)
async def add_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    todo = Todo(**todo.dict())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    session.close()
    return todo


@app.put("/todos/{id}", response_model=TodoOut)
async def update_todo(id: int, todo: TodoUpdate, session: Session = Depends(get_session)):

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
async def delete_todo(id: int, session: Session = Depends(get_session)):

    result = session.get(Todo, id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    session.delete(result)
    session.commit()
    return result
