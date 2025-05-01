from typing import Optional

from pydantic import BaseModel


class MenuItemRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True


class MenuItemUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]
    is_available: Optional[bool]

class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True

