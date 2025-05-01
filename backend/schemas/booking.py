from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    restaurant_id: int
    booking_time: datetime
    number_of_people: int
    special_request: Optional[str] = None  # Comments for allergies, etc.

class BookingOut(BaseModel):
    id: int
    restaurant_id: int
    restaurant_name: Optional[str] = None
    booking_time: datetime
    number_of_people: int
    special_request: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
