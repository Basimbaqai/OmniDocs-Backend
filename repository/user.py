from fastapi import status,HTTPException
from hashing import HashPassword
import models
from sqlalchemy.orm import Session

def get_current_user(db: Session,user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

def get_user(id: int, db: Session,user_id:int):
    if id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


def create_user(request, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=HashPassword.bcrypt(request.password)  # Hash the password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(id: int, request, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user.update({
        'name': request.name,
        'email': request.email,
        'password': HashPassword.bcrypt(request.password)  # Hash the password
    })
    db.commit()
    return user.first()



def delete_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted successfully"}
