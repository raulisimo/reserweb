import datetime

from sqlalchemy import Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import ModelBase


class Booking(ModelBase):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))
    booking_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    number_of_people: Mapped[int] = mapped_column(Integer, nullable=False)
    special_request: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="bookings")
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="bookings")
