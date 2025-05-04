from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from dependencies.authentication import get_current_user
from dependencies.database import get_db
from models.user import User
from repositories.reviews import ReviewRepository
from schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter()
review_repo = ReviewRepository()


@router.get("/all", response_model=list[ReviewRead])
def get_reviews(db: Session = Depends(get_db)):
    return review_repo.get_all_reviews(db)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_review(review_create: ReviewCreate, db: Session = Depends(get_db)):
    new_review = review_repo.create_review(db, review_create)
    return new_review


@router.get("/restaurant/{restaurant_id}", response_model=list[ReviewRead])
def get_reviews_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    reviews = review_repo.get_reviews_by_restaurant(db, restaurant_id)

    return reviews


@router.get("/user", response_model=list[ReviewRead])
def get_reviews_by_user(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    reviews = review_repo.get_reviews_by_user(db, user.id)
    if not reviews:
        return []
    return reviews


@router.get("/user/{user_id}", response_model=list[ReviewRead])
def get_reviews_by_user(user_id: int,
                        db: Session = Depends(get_db),
                        ):
    reviews = review_repo.get_reviews_by_user(db, user_id)
    if not reviews:
        return []
    return reviews


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    updated_review = review_repo.update_review(db, review_id, review_update)
    if not updated_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
    return updated_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    success = review_repo.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
    return
