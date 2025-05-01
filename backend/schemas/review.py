from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReviewCreate(BaseModel):
    user_id: int
    restaurant_id: int
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class ReviewRead(BaseModel):
    id: int
    comment: str
    created_at: datetime
    rating: float
    user_name: Optional[str] = None
    restaurant_name: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None