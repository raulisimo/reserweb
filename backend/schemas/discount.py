from datetime import date
from typing import Optional

from pydantic import BaseModel


class DiscountOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    percentage: float
    valid_from: date
    valid_until: date
    restaurant_id: int

    class Config:
        from_attributes = True


class DiscountUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    percentage: Optional[float]
    valid_from: Optional[date]
    valid_until: Optional[date]
    restaurant_id: Optional[int]


class DiscountCreate(BaseModel):
    title: str
    description: Optional[str]
    percentage: float
    valid_from: date
    valid_until: date
    restaurant_id: int
