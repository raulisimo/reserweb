from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookingCreate(BaseModel):
    restaurant_id: int
    booking_time: datetime
    number_of_people: int
    special_request: Optional[str] = None


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

class BookingWithUserOut(BaseModel):
    id: int
    created_at: datetime
    booking_time: datetime
    number_of_people: int
    special_request: Optional[str] = None

    restaurant_id: int
    restaurant_name: str

    user_id: int
    user_name: str

    class Config:
        from_attributes = True