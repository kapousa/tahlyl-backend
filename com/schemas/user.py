from pydantic import BaseModel #, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str #EmailStr
    role: str
    avatar: str

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
    name: Optional[str] = None