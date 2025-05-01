import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.authentication import get_current_user
from dependencies.database import get_db
from models.user import User
from repositories.bookings import BookingRepository
from schemas.booking import BookingOut, BookingCreate

router = APIRouter()

booking_repo = BookingRepository()


@router.post("/", response_model=BookingOut)
def book_restaurant(booking: BookingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    # Validate booking time is not in the past
    if booking.booking_time < datetime.datetime.now(datetime.UTC):
        raise HTTPException(status_code=400, detail="Cannot book a past time")

    # Create a booking using the repository
    new_booking = booking_repo.create_booking(
        db,
        restaurant_id=booking.restaurant_id,
        booking_time=booking.booking_time,
        number_of_people=booking.number_of_people,
        special_request=booking.special_request,
        user_id=user.id
    )

    return new_booking


@router.delete("/user/{booking_id}", response_model=BookingOut)
def delete_booking_by_user(booking_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Fetch the booking to check if the user has permission to delete it
    booking = booking_repo.get_booking_by_id(db, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this booking")

    # Delete the booking
    booking_repo.delete_booking(db, booking_id)

    return booking  # Return the deleted booking information (optional)

@router.get("/user", response_model=list[BookingOut])
def get_bookings_by_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Fetch bookings by user_id
    bookings = booking_repo.get_bookings_by_user(db, user_id=user.id)
    return bookings


@router.get("/restaurant", response_model=list[BookingOut])
def get_bookings_by_restaurant(db: Session = Depends(get_db), restaurant: User = Depends(get_current_user)):
    # Fetch bookings by restaurant_id
    bookings = booking_repo.get_bookings_by_restaurant(db, restaurant_id=restaurant.id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this restaurant")
    return bookings
