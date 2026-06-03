from enum import member
from fastapi import APIRouter , HTTPException, Depends
from sqlalchemy.orm import Session 
from models import Member,Book,Borrow 
from schemas import Borrow as BorrowSchema 
from database import get_db
from datetime import date 
from typing import Optional


# app.include_router(borrows.route)              ← yeh comment
route= APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)

borrow_list=[]
 
@route.post("/", status_code=201)
async def create_borrow(new_borrow: BorrowSchema, db:Session=Depends(get_db)):
   book=db.query(Book).filter(Book.id == new_borrow.book_id).first()
   # Find book in database
   if book is None: 
     raise HTTPException(status_code =404, detail="The book is not found")
   # Find copies are available or not 
   if Book.total_copies <=0: 
    raise HTTPException(status_code =404, detail="The copy is not available")

   member=db.query(Member).filter(Member.id == new_borrow.member_id).first()
   if member is None: 
     raise HTTPException(status_code =404, detail="The member is not found")
   
   # decrement 
   Book.total_copies-=1
   new_borrow_db=Borrow (
     book_id = new_borrow.book_id,
     member_id= new_borrow.member_id,
     borrow_date= str(date.today()),
     return_date=None,
     status= "active"
   )
    
   db.add(new_borrow_db),
   db.commit(),
   db.refresh(new_borrow_db)
   return {"message": "Book borrowed successfully", "borrow": new_borrow_db}
@route.get("/")
async def get_borrows(member_id: Optional[int]=None, status: Optional[str]=None, db:Session=Depends(get_db)): 
    query=db.query(Borrow)
    if member_id is not None: 
        query=query.filter(Borrow.member_id==member_id)
    if status is not None: 
        query=query.filter(Borrow.status==status)
    
    return query.all()
      

@route.get("/{borrow_id}")
async def get_borrow_by_id(borrow_id:int, db:Session=Depends(get_db)):
     borrow=db.query(Borrow).filter(Borrow.id ==borrow_id).first()
     if borrow is None: 
         raise HTTPException (status_code=404, detail="The borrow id is not found")
     return {"message":"The borrow id is found","borrow":borrow}

## Return Book 
@route.put("/{borrow_id}/return")
async def return_book(borrow_id:int,db:Session=Depends(get_db)): 

    borrow_update=db.query(Borrow).filter(Borrow.id ==borrow_id).first()
    if borrow_update is None:
         raise HTTPException(status_code=404, detail="The Borrow id is not found")
    if borrow_update.status == "returned":
         raise HTTPException(status_code=400, detail="Already returned")
    
    borrow_update.status="returned"
    borrow_update.return_date = str(date.today())
    book=db.query(Book).filter(Book.id ==borrow_update.book_id).first()
    if book is not None: 
        book.available_copies+=1
       
    db.commit()
    db.refresh(borrow_update)
    
    return {"message": "Book returned successfully", "borrow": borrow_update}
