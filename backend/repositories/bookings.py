import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.booking import Booking
from models.restaurants import Restaurant
from models.user import User
from repositories.base import BaseRepository
from repositories.restaurant import RestaurantRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self):
        super().__init__(Booking)

    def get_booking_by_id(self, db: Session, booking_id: int) -> Optional[Booking]:
        return db.query(Booking).filter(Booking.id == booking_id).first()

    def delete_booking(self, db: Session, booking_id: int):
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            db.delete(booking)
            db.commit()

    def create_booking(self, db: Session, restaurant_id: int, booking_time: datetime, number_of_people: int,
                       special_request: str, user_id: int) -> Booking:
        booking = Booking(
            restaurant_id=restaurant_id,
            booking_time=booking_time,
            number_of_people=number_of_people,
            special_request=special_request,
            user_id=user_id
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    def get_bookings_by_user(self, db: Session, user_id: int):
        bookings_query = db.query(
            Booking.id,
            Booking.created_at,
            Booking.booking_time,
            Booking.number_of_people,
            Booking.special_request,
            Restaurant.name.label('restaurant_name'),
            Restaurant.id.label('restaurant_id')
        ).join(Restaurant, Restaurant.id == Booking.restaurant_id).filter(Booking.user_id == user_id)
        bookings = bookings_query.all()

        return bookings

    def get_bookings_by_restaurant(self, db: Session, restaurant_id: int):
        restaurant = RestaurantRepository().get_by_user_id(db, restaurant_id)

        bookings_query = db.query(
            Booking.id,
            Booking.created_at,
            Booking.booking_time,
            Booking.number_of_people,
            Booking.special_request,
            Booking.restaurant_id,
            Restaurant.name.label('restaurant_name'),
            Booking.user_id,
            User.name.label('user_name'),
            User.id.label('user_id')
        ).join(User, User.id == Booking.user_id) \
            .join(Restaurant, Restaurant.id == Booking.restaurant_id) \
            .filter(Booking.restaurant_id == restaurant.id)

        results = bookings_query.all()

        return [
            {
                "id": r[0],
                "created_at": r[1],
                "booking_time": r[2],
                "number_of_people": r[3],
                "special_request": r[4],
                "restaurant_id": r[5],
                "restaurant_name": r[6],
                "user_id": r[7],
                "user_name": r[8],
            }
            for r in results
        ]
