from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal


router = APIRouter()



##fetch info from a database, return it to the client then close the connection

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
## Annotated to create Dependency Injection       
db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):  ### Done before post request for sure to validate request insertion
    ## id is auto incremented by sqlalchemy so no needed here 
    title: str = Field(min_length=3)
    description: str = Field(min_length=4, max_length=100)
    priority: int = Field(gt=0, lt=7)
    complete: bool
    

@router.get("/")
async def read_all(db: db_dependency):  ## Depends create session, return info back to us then close connection
    
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Task is not found")

    
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    
    db.add(todo_model) 
    db.commit()
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description  = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tod(db: db_dependency, todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Could not found Todo")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    