from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_nam = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)  ###a password that cannot decrypted
    is_active = Column(Boolean, default=False)
    role = Column(String)
    
### models schema of tables that we are submitted into database
class Todos(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default= False)
    owner_id = Column(Integer, ForeignKey("users.id"))