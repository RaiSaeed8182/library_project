from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from database import get_db
from models import User 



# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Password functions
def hash_password(password: str) -> str:
    """Plain password ko hash karta hai using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Plain password aur hash compare karta hai"""
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)) -> User: 
  credentials_exception= HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail= "Invalid authentication credentials ",
    headers={"WWW-AUthentication":"Bearer"}
)

  payload=decode_access_token(token)
  if payload is None: 
    raise credentials_exception 
  user_id = payload.get("user_id")
  if user_id is None: 
    raise credentials_exception
  user= db.query(User).filter(User.id==user_id).first()
  if user is None: 
    raise credentials_exception
  
  return user 


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user