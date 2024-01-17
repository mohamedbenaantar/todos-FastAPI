from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" ### create a database in the location where am I

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
### for multiple access, engine represents the database connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
### you need to explicitly call commit() to persist changes

### to interact with database
Base = declarative_base()
