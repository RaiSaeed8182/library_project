from pydantic import BaseModel 
from typing import Optional 

class Book(BaseModel): 
    id: int 
    title: str
    author: str 
    category: str 
    total_copies: int
    available_copies: int


class Member(BaseModel): 
    id: int
    name: str
    email: str
    phone: str
    membership_type: str

class Borrow(BaseModel): 
    id: int
    book_id: int
    member_id: int 
    borrow_date: str 
    return_date: Optional[str]=None 
    status: str 


