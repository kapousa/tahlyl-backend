from pydantic import BaseModel #, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str #EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None