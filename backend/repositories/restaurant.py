from sqlalchemy import func
from sqlalchemy.orm import Session

from models.restaurants import Restaurant
from models.reviews import Review
from repositories.base import BaseRepository


class RestaurantRepository(BaseRepository[Restaurant]):
    def __init__(self):
        super().__init__(Restaurant)

    def search_restaurants(self, db: Session, query: str):
        return db.query(Restaurant).filter(
            Restaurant.name.ilike(f"%{query}%")
        ).all()

    def get_restaurants_with_score(self, db: Session):
        return db.query(
            Restaurant.id,
            Restaurant.name,
            Restaurant.description,
            Restaurant.address,
            Restaurant.phone,
            Restaurant.embedded_map,
            func.round(func.avg(Review.rating), 1).label("avg_score")
        ).outerjoin(Review, Restaurant.id == Review.restaurant_id) \
            .group_by(Restaurant.id) \
            .all()

    def get_by_user_id(self, db: Session, user_id: int):
        return db.query(Restaurant).filter(Restaurant.user_id == user_id).first()
