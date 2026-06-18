from pydantic import BaseModel , EmailStr
from typing import Optional 

class Book(BaseModel): 
    title: str
    author: str 
    category: str 
    total_copies: int
    available_copies: int




class BorrowCreate(BaseModel):
    book_id: int
    member_id: int


class Borrow(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrow_date: str
    return_date: Optional[str] = None
    status: str
    
    class Config:
        from_attributes = True 

class UserCreate(BaseModel): 
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str 

class Token(BaseModel): 
    access_token:str
    token_type:str

class MemberCreate(BaseModel):
    name: str
    email: str
    phone: str
    membership_type: str


class Member(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    membership_type: str
    
    class Config:
        from_attributes = True


