from typing import Optional
from fastapi import APIRouter , HTTPException
from models import Book


route = APIRouter(
    prefix="/books",
    tags=["Books"]
)

book_list =[]


@route.post("/", status_code=201)
async def create_book(new_book:Book):
     book_list.append(new_book)
     return {"message":" The Book is added successfully", "book":new_book}


@route.get("/")
async def get_book(category : Optional[str]=None, available_only:bool= False):
       filter_book=[]
       for book in book_list:
           if category is not None and book.category != category: 
            continue

           if available_only and book.available_copies <=0 : 
            continue

           filter_book.append(book)
        
       return filter_book



@route.get("/{book_id}")
async def get_any_book(book_id: int): 
    for book in book_list: 
        if book.id ==  book_id : 
            return {"message":"The Book is here", "book":book}
    raise HTTPException (status_code=404,detail="Data is not found")

@route.put("/{book_id}")
async def update_book(book_id: int, update_book:Book): 
    for index,book in enumerate(book_list): 
      if book.id == book_id : 
        book_list[index]=update_book 
        return {"message":" The Book id is update successfully"}
    raise HTTPException(status_code=404, detail="The data is not found")


@route.delete("/{book_id}")
async def delete_book(book_id : int): 
    for index , book in enumerate (book_list): 
        if book.id == book_id: 
            book_list.pop(index)
            return {"message": "Data is deleted successfully"}
    raise HTTPException(status_code=404, detail="The data is not found ")