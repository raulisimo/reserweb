from sqlalchemy.orm import Session

from models.discounts import Discount
from schemas.discount import DiscountUpdate, DiscountCreate


class DiscountRepository:
    def get_discounts_by_restaurant(self, db: Session, restaurant_id: int):
        return db.query(Discount).filter(Discount.restaurant_id == restaurant_id).all()
    def update_discount(self, db: Session, discount_id: int, data: DiscountUpdate):
        discount = db.query(Discount).filter_by(id=discount_id).first()
        if not discount:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(discount, key, value)
        db.commit()
        db.refresh(discount)
        return discount

    def delete_discount(self, db: Session, discount_id: int) -> bool:
        discount = db.query(Discount).filter_by(id=discount_id).first()
        if not discount:
            return False
        db.delete(discount)
        db.commit()
        return True

    def create_discount(self, db: Session, data: DiscountCreate):
        new_discount = Discount(**data.model_dump())
        db.add(new_discount)
        db.commit()
        db.refresh(new_discount)
        return new_discount