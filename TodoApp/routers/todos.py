from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from .auth import get_current_user

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
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):  ### Done before post request for sure to validate request insertion
    ## id is auto incremented by sqlalchemy so no needed here 
    title: str = Field(min_length=3)
    description: str = Field(min_length=4, max_length=100)
    priority: int = Field(gt=0, lt=7)
    complete: bool
    
### get all todos based on a specific user
@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):  ## Depends create session, return info back to us then close connection
    
    return db.query(Todos).filter(user.get('id')== Todos.id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, default='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Task is not found")

    
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    ### can' accept insert new todo if you are not authenticated required user id
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id')) 
    
    db.add(todo_model)
    db.commit()
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description  = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tod(user: user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Could not found Todo")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
    