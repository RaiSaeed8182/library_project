import email
from pstats import Stats
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 

from database import get_db
from models import User 
from schemas import UserCreate, Token 
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"User is registered Successfully","user":{"id":new_user.id,"email":new_user.email}}


@route.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # form_data.username = email (Swagger sends email as username)
    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}