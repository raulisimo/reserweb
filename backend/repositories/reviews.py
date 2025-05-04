from sqlalchemy.orm import Session

from models.restaurants import Restaurant
from models.reviews import Review
from models.user import User
from repositories.base import BaseRepository
from schemas.review import ReviewCreate, ReviewRead


class ReviewRepository(BaseRepository[Review]):
    def __init__(self):
        super().__init__(Review)

    def get_all_reviews(self, db: Session):
        reviews_query = db.query(
            Review.id,
            Review.comment,
            Review.created_at,
            Review.rating,
            User.name.label('user_name'),
            Restaurant.name.label('restaurant_name'),
        ).join(User, User.id == Review.user_id).join(Restaurant, Restaurant.id == Review.restaurant_id)

        reviews = reviews_query.all()

        return reviews

    def create_review(self, db: Session, review_create: ReviewCreate) -> Review:
        db_review = Review(
            user_id=review_create.user_id,
            restaurant_id=review_create.restaurant_id,
            rating=review_create.rating,
            comment=review_create.comment
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    def get_reviews_by_restaurant(self, db: Session, restaurant_id: int) -> list[Review]:
        reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()

        result = []
        for review in reviews:
            result.append(ReviewRead(
                id=review.id,
                comment=review.comment,
                created_at=review.created_at,
                rating=review.rating,
                user_name=review.user.name,
                restaurant_name=review.restaurant.name
            ))
        return result

    def get_reviews_by_user(self, db: Session, user_id: int) -> list[Review]:
        reviews = db.query(Review).filter(Review.user_id == user_id).all()

        result = []
        for review in reviews:
            result.append(ReviewRead(
                id=review.id,
                comment=review.comment,
                created_at=review.created_at,
                rating=review.rating,
                user_name=review.user.name,
                restaurant_name=review.restaurant.name
            ))
        return result

    def get_review(self, db: Session, review_id: int) -> Review:
        return db.query(Review).filter(Review.id == review_id).first()

    def update_review(self, db: Session, review_id: int, review_update: ReviewCreate) -> Review | None:
        review = self.get_review(db, review_id)
        if review:
            for field, value in review_update.dict(exclude_unset=True).items():
                setattr(review, field, value)
            db.add(review)
            db.commit()
            db.refresh(review)
            return review
        return None

    def delete_review(self, db: Session, review_id: int) -> bool:
        review = self.get_review(db, review_id)
        if review:
            db.delete(review)
            db.commit()
            return True
        return False
