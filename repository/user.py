from fastapi import status, HTTPException
from hashing import HashPassword
import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def get_current_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user


def get_user(id: int, db: Session, user_id: int):
    if id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user",
        )
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


def create_user(request, db: Session):
    try:
        # Check if user already exists
        existing_user = (
            db.query(models.User).filter(models.User.email == request.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = models.User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            password=HashPassword.bcrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )


def update_user(current_user, request, db: Session):
    user = db.query(models.User).filter(models.User.user_id == current_user.user_id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {current_user.user_id} not found",
        )

    update_data = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email,
    }

    # Only update password if provided
    if hasattr(request, "password") and request.password:
        update_data["password"] = HashPassword.bcrypt(request.password)

    user.update(update_data)
    db.commit()
    return user.first()


def delete_user(id: int, db: Session):
    user_obj = db.query(models.User).filter(models.User.user_id == id).first()

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    db.delete(user_obj)
    db.commit()
    # No return needed for 200 OK with status code HTTP_200_OK
