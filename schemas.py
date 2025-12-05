from pydantic import BaseModel
from typing import List, Optional


class ShowUser(BaseModel):

    first_name: str
    last_name: str
    email: str
    password: str

    # Use forward reference for ShowBlogs
    class Config:
        from_attributes = True


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
