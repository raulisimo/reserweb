import datetime

from sqlalchemy import String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import ModelBase


class Discount(ModelBase):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    percentage: Mapped[int] = mapped_column(Integer)
    valid_from: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    valid_until: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="discounts")
