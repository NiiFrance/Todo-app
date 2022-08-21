from fastapi import FastAPI, HTTPException, status
from sqlmodel import create_engine

app = FastAPI()

todos = {
    "Work out",
    "Learn FastAPI",
    "Visit Egypt"
}


@app.get("/todos", status_code=status.HTTP_200_OK)
def get_todos():
    return todos


@app.get("/todos/{id}")
def get_todo(id: int):
    try:
        return todos[id]

    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def add_todo(todo: str):
    todos.append(todo)


@app.put("/todos/{id}")
def update_todo(id: int, todo: str):
    try:
        todos[id] = todo
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.delete("/todos/{id}")
def delete_todo(id: int):
    try:
        todos.pop(id)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
