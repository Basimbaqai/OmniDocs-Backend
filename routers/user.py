from fastapi import APIRouter, Depends, status, HTTPException
from hashing import HashPassword
import oauth
import schemas
from database import get_db
import models
from sqlalchemy.orm import Session
from repository import user

router = APIRouter(
    prefix="/users", tags=["Users"]  # Prefix for all routes in this router
)


# User CRUD Operations
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get("", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_current_user(
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth.get_current_user),
):
    if get_current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user.get_current_user(db, get_current_user.user_id)


@router.get("/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth.get_current_user),
):
    if get_current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user.get_user(id, db, get_current_user.user_id)


@router.put("", response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED)
def update_user(
    request: schemas.User,
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth.get_current_user),
):
    if get_current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user.update_user(get_current_user.user_id, request, db)


@router.delete("", status_code=status.HTTP_200_OK)
def delete_user(
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth.get_current_user),
):
    if get_current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user.delete_user(get_current_user.user_id, db)
