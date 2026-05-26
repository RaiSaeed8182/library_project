from optparse import Option
from typing import Optional
from routes.books import book_list
from routes.members import members_list 
from fastapi import APIRouter , HTTPException
from models import Borrow
from datetime import date

route= APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)

borrow_list=[]
 
@route.post("/", status_code=201)
async def create_borrow(new_borrow: Borrow):
    # Step 1: Find book
    found_book = None
    for book in book_list:
        if book.id == new_borrow.book_id:
            found_book = book
            break
    
    if found_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Step 2: Check availability
    if found_book.available_copies <=0 : 
        raise HTTPException(status_code=404, detail="Book not available")
    
    # Step 3: Find member
    member_found=None
    for member in members_list: 
        if  member.id ==new_borrow.member_id: 
            member_found=member
            break

    if member_found is None:
        raise HTTPException(status_code=404, detail="Member is not found")
    
    
    # Step 4: Decrement
    # tum likho...
    found_book.available_copies-=1
    
    # Step 5: Append + return
    # tum likho...
    borrow_list.append(new_borrow)
    return{"message": "Book borrowed successfully", "borrow": new_borrow}

@route.get("/")
async def get_borrows(member_id: Optional[int]=None, status: Optional[str]=None): 
    filter_borrows=[]
    for borrow  in borrow_list: 
        if member_id is not None and borrow.member_id != member_id : 
            continue
        if status is not None and borrow.status != status : 
            continue
        filter_borrows.append(borrow)
    return filter_borrows


## Find Specif Book/Member   

@route.get("/{borrow_id}")
async def get_borrow_by_id(borrow_id:int): 
    for borrow in borrow_list: 
      if borrow.id == borrow_id: 
        return borrow
    raise HTTPException (status_code=404, detail="The borrow  is not found")

## Return Book 
@route.put("/{borrow_id}/return")
async def return_book(borrow_id:int): 
    borrow_update=None
    for borrow in borrow_list: 
        if borrow.id == borrow_id:
            borrow_update=borrow
            break
    
    if borrow_update is None:
     raise HTTPException(status_code=404, detail="The Borrow id is not found")

    # Check if already returned
    if borrow_update.status == "returned":
       raise HTTPException(status_code=400, detail="Already returned")

# Update status
    borrow_update.status = "returned"
    borrow_update.return_date = str(date.today())    
    
    for book in book_list:
        if book.id == borrow_update.book_id:
            book.available_copies += 1
            break
    
    return {"message": "Book returned successfully", "borrow": borrow_update}
