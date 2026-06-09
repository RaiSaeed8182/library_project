from typing import Optional
from unicodedata import category
from fastapi import APIRouter , HTTPException, Depends 
from sqlalchemy.orm import Session, query 
from typing import Optional
from database import get_db
from models import Book, User
from schemas import Book as BookSchema 
from auth import get_current_user


route = APIRouter(
    prefix="/books",
    tags=["Books"]
)

book_list =[]


@route.post("/", status_code=201)
async def create_book(new_book:BookSchema,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
     book_db=Book(
        title=new_book.title,
        author=new_book.author,
        category=new_book.category,
        total_copies =new_book.total_copies,
        available_copies= new_book.available_copies
     )
     db.add(book_db)
     db.commit()
     db.refresh(book_db)
     return {"message":"Book added success fully", "book":book_db}

@route.get("/")
async def get_book(category: Optional[str]=None,available_only:bool= False, db:Session=Depends(get_db)):
    query=db.query(Book)

    if category is not None: 
        query=query.filter(Book.category==category)
    if available_only: 
        query= query.filter(Book.available_copies > 0)

    return query.all()


@route.get("/{book_id}")
async def get_any_book(book_id: int, db:Session=Depends(get_db)):
       book=db.query(Book).filter(Book.id==book_id).first()
       if book is None: 
            raise HTTPException( status_code = 404, detail="Book not found")
       return book

@route.put("/{book_id}") 
async def update_book(book_id: int, update_book:BookSchema, db:Session=Depends(get_db),current_user:User=Depends(get_current_user)): 
   book= db.query(Book).filter(Book.id==book_id).first()

   if book is None : 
        raise HTTPException(status_code=404, detail="The Book does not found")
    
   book.title= update_book.title
   book.author= update_book.author
   book.category= update_book.category
   book.total_copies= update_book.total_copies
   book.available_copies= update_book.available_copies
   db.commit()
   db.refresh(book)
   return {"message":"The Book is update","book":book}

@route.delete("/{book_id}")
async def delete_book(book_id : int, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)): 
    book=db.query(Book).filter(Book.id==book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="The book is not found")
    db.delete(book)
    db.commit()
    return {"message":"The Book is deleted successfully"}