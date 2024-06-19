from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path, status
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

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()



@app.get("/todos/{todo_id}")
async def read_todo_of_id(db: db_dependency, todo_id: int = Path(gt=0), status_code=status.HTTP_200_OK):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")
