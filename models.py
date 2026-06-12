import email
from unicodedata import category
from sqlalchemy import Column, Index, String , Integer , Float
from database import Base

class Book(Base): 
      __tablename__= "books" 

      id = Column(Integer, primary_key=True, index=True)
      title = Column(String, index=True)
      author= Column(String)
      category= Column (String, index=True)
      total_copies=Column(Integer)
      available_copies=Column(Integer)



class Member(Base): 
    __tablename__="members"
    
    id=Column(Integer, primary_key=True, index= True)
    name=Column(String, index=True)
    email = Column(String , unique=True, index=True)
    phone= Column (String)
    membership_type= Column (String)



class Borrow(Base): 
    __tablename__="borrows"
 
    id= Column(Integer, primary_key=True, index=True)
    book_id= Column(Integer, index=True)
    member_id= Column (Integer, index=True)
    borrow_date=Column(String)
    return_date=Column(String, nullable=True)
    status= Column(String)

class User(Base): 
    __tablename__="user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")