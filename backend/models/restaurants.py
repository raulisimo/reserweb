import datetime
from datetime import datetime, UTC

from sqlalchemy import String, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import ModelBase



class Restaurant(ModelBase):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )
    embedded_map: Mapped[str] = mapped_column(Text, nullable=True)
    menu_items: Mapped[list["MenuItem"]] = relationship("MenuItem", back_populates="restaurant")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="restaurant")
    discounts: Mapped[list["Discount"]] = relationship("Discount", back_populates="restaurant")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="restaurant")


