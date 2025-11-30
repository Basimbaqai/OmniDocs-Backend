from datetime import datetime, timedelta
from datetime import timezone
from jose import JWTError, jwt
from typing import Optional
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

load_dotenv()


import models
import schemas
import os 

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Convert to int and provide default

# JWT Configuration

# For production, use a fixed secret key stored in environment variables
# SECRET_KEY = "your-secret-key-here-make-it-very-long-and-secure"

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception,db:Session):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return db.query(models.User).filter(models.User.id == user_id).first()
    except JWTError:
        raise credentials_exception
    