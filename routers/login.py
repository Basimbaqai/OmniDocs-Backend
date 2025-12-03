from fastapi import APIRouter,Depends,status,HTTPException
from hashing import HashPassword
import schemas
from typing import List
from database import get_db
import models
from sqlalchemy.orm import Session
from token_generation import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    tags=['Login']
    # Tag for the router
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not HashPassword.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    access_token=create_access_token(user.user_id)
    return schemas.Token(access_token=access_token, token_type="bearer")