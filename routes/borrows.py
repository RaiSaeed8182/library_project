from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 
from datetime import date 
from typing import Optional

from models import Book, Member, Borrow, User    
from schemas import BorrowCreate
from database import get_db
from auth import get_current_user               


route = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)


@route.post("/", status_code=201)
async def create_borrow(
    new_borrow: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Step 1: Find book in database
    book = db.query(Book).filter(Book.id == new_borrow.book_id).first()
    if book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Step 2: Check available copies
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for borrowing")
    
    # Step 3: Find member
    member = db.query(Member).filter(Member.id == new_borrow.member_id).first()
    if member is None: 
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Step 4: Decrement available copies
    book.available_copies -= 1
    
    # Step 5: Create borrow record
    new_borrow_db = Borrow(
        book_id=new_borrow.book_id,
        member_id=new_borrow.member_id,
        borrow_date=str(date.today()),
        return_date=None,
        status="active"
    )
    
    db.add(new_borrow_db)
    db.commit()
    db.refresh(new_borrow_db)
    
    return {"message": "Book borrowed successfully", "borrow": new_borrow_db}


@route.get("/")
async def get_borrows(
    member_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    query = db.query(Borrow)
    if member_id is not None: 
        query = query.filter(Borrow.member_id == member_id)
    if status is not None: 
        query = query.filter(Borrow.status == status)
    
    return query.all()


@route.get("/{borrow_id}")
async def get_borrow_by_id(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if borrow is None: 
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return {"message": "Borrow record found", "borrow": borrow}


@route.put("/{borrow_id}/return")
async def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    borrow_update = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if borrow_update is None:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    if borrow_update.status == "returned":
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Update borrow record
    borrow_update.status = "returned"
    borrow_update.return_date = str(date.today())
    
    # Increment available copies
    book = db.query(Book).filter(Book.id == borrow_update.book_id).first()
    if book is not None: 
        book.available_copies += 1
       
    db.commit()
    db.refresh(borrow_update)
    
    return {"message": "Book returned successfully", "borrow": borrow_update}