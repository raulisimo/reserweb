from fastapi import APIRouter

from routers.auth import router as auth_router
from routers.restaurants import router as restaurants_router
from routers.reviews import router as reviews_router
from routers.bookings import router as booking_router
from routers.users import router as users_router
from routers.roles import router as roles_router
from routers.discounts import router as discounts_router
from routers.menu import router as menu_router

# Create a main router to include all sub-routers
api_router = APIRouter()

# Include route modules
api_router.include_router(restaurants_router, prefix="/restaurants", tags=["Restaurants"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(reviews_router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(roles_router, prefix="/roles", tags=["Roles"])
api_router.include_router(discounts_router, prefix="/discounts", tags=["Discounts"])
api_router.include_router(menu_router, prefix="/menu", tags=["Menu"])