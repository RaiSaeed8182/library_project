from fastapi import APIRouter , HTTPException
from models import Member 


route = APIRouter(
    prefix="/members",
    tags=["Members"]
)


members_list=[]

@route.post("/", status_code=201)
async def add_member(member:Member):
    members_list.append(member)
    return {"message":"member added successfully", "member":member}


@route.get("/")
async def get_data():
    return  members_list 

@route.get("/{member_id}")
async def get_specific_data(member_id:int): 
    for member in members_list : 
        if member.id == member_id: 
            return {"message":"The member is here", "member":member}
    raise HTTPException(status_code=404, detail="Member  is not found")


@route.put("/{member_id}")
async def update_member(member_id: int , update_member: Member): 
    for index, member in enumerate (members_list): 
        if member.id == member_id : 
            members_list[index] = update_member
            return {"message":"member updated successfully"}
    raise HTTPException(status_code=404, detail="Member not Found")

@route.delete("/{member_id}")
async def delete_member(member_id:int) : 
    for index ,member in enumerate(members_list): 
        if member.id == member_id : 
            members_list.pop(index)
            return {"message":"The member is deleted successfully"}
    raise HTTPException (status_code=404, detail="The member  not found ")
