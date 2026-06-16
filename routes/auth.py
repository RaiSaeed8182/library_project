import email
from pstats import Stats
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 

from database import get_db
from models import User 
from schemas import UserCreate, Token 
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import BackgroundTasks
from audit_log import log_user_signup

route = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@route.post("/signup", status_code=201)
async def signup(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Step 1: Email check (EXISTING)
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Step 2: Hash password (EXISTING)
    hashed_pw = hash_password(user_data.password)
    
    # Step 3: Create user (EXISTING)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        role="user"
    )
    
    # Step 4: Save to database (EXISTING)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Step 5: NEW! Schedule background task
    background_tasks.add_task(
        log_user_signup,
        user_email=new_user.email,
        user_id=new_user.id
    )
    
    # Step 6: Return response (EXISTING)
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email
        }
    }

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