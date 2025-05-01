from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    phone: Optional[str] = None  # Optional field
    password: Optional[str] = None  # Optional for update

class UserRead(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
