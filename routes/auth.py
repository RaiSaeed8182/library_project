import email
from pstats import Stats
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 

from database import get_db
from models import User 
from schemas import UserCreate, Token 
from auth import hash_password, verify_password, create_access_token

route = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@route.post("/Signup", status_code=201)
async def signup (user_data:UserCreate, db:Session=Depends(get_db)): 
    existing_user= db.query(User).filter(User.email==user_data.email)
    if existing_user is None: 
        raise HTTPException(status_code=404, detail="Email is already register")
    hashed_pwd= hash_password(user_data.password)

    new_user=User(
        email=user_data.email,
        hashed_password=hashed_pwd,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"User is registered Successfully","user":{"id":new_user.id,"email":new_user.email}}


@route.post("/login",response_model=Token)
async def login(user_data:UserCreate, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_data.email).first()
    if user is None: 
        raise HTTPException(status_code=401,detail="Invalid email and password ")
    if not verify_password(user_data.password,user.hashed_password): 
        raise HTTPException(status_code=401, detail="Invalid email and password")
        
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    
    # Step 4: Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }