from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from database import get_db
import token_generation
from sqlalchemy.orm import Session



oauth2_scheme = APIKeyHeader(name="Authorization")


def get_current_user(Token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_generation.verify_token(Token, credentials_exception,db)
   
   