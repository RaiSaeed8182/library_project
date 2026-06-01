from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Member                    # SQLAlchemy
from schemas import Member as MemberSchema   # Pydantic alias


route = APIRouter(
    prefix="/members",
    tags=["Members"]
)

members_list =[]

@route.post("/", status_code=201)
async def add_member(member:MemberSchema, db:Session=Depends(get_db)):
      new_member=Member(
        name = member.name,
        email= member.email,
        phone = member.phone,
        membership_type= member.membership_type
      )
      db.add(new_member)
      db.commit()
      db.refresh(new_member)
      return {"message":"The Member is add successfully","member":new_member}

@route.get("/")
async def get_data(db:Session=Depends(get_db)):
    member=db.query(Member).all()
    return member

@route.get("/{member_id}")
async def get_specific_data(member_id:int, db:Session=Depends(get_db)): 
      member = db.query(Member).filter(Member.id==member_id).first()
      if member is None:
             raise HTTPException(status_code=404, detail="Member  is not found")
        
      return {"message":"The member is here", "member":member}
   


@route.put("/{member_id}")
async def update_member(member_id: int , update_member: MemberSchema, db:Session=Depends(get_db)): 
    member= db.query(Member).filter(Member.id ==member_id).first()
    if member is None: 
          raise HTTPException(status_code=404, detail="Member not Found")
        
    member.email= update_member.email
    member.membership_type= update_member.membership_type
    member.name= update_member.name
    member.phone= update_member.phone
    db.commit()
    db.refresh(member)
    return member
  

@route.delete("/{member_id}")
async def delete_member(member_id:int,db:Session=Depends(get_db)) : 
    member=db.query(Member).filter(Member.id ==member_id ).first()
    if member is None:
         raise HTTPException (status_code=404, detail="The member  not found ")
    db.delete(member)
    db.commit()
    return {"message":"The member is deleted successfully"}
   
