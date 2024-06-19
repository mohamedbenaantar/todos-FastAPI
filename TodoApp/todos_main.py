from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field

from database import engine, session_local
from sqlalchemy.orm import Session
import models
from models import Todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# this is will create database with the table speicified if todos.db not exist

# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated [Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title : str = Field(min_length=5)
    description: str = Field(min_length=10, max_length=100)
    priority : int = Field(gt=0, lt=30)
    complete : bool


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    new_todo = Todos(**todo_request.model_dump())
    db.add(new_todo)
    db.commit()

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()



@app.get("/todos/{todo_id}",  status_code=status.HTTP_200_OK)
async def read_todo_of_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not exist to be updated")
    else:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()
        
