from fastapi import FastAPI
from database import engine
from routers import auth, todos
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  ### this is will create database with the table speicified if todos.db not exist
app.include_router(auth.router)
app.include_router(todos.router)

