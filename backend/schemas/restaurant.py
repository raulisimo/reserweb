from typing import Optional

from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone: Optional[str] = None
    user_id: int


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class RestaurantOutScore(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str
    phone: Optional[str]
    embedded_map: Optional[str]
    avg_score: Optional[float]


class RestaurantOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str
    phone: Optional[str]
    embedded_map: Optional[str]

    class Config:
        from_attributes = True
