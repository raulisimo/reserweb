from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies.database import get_db
from repositories.discount import DiscountRepository
from schemas.discount import DiscountOut, DiscountUpdate, DiscountCreate

router = APIRouter()

discount_repo = DiscountRepository()

@router.get("/restaurant/{restaurant_id}", response_model=List[DiscountOut])
def get_discounts_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    discounts = discount_repo.get_discounts_by_restaurant(db, restaurant_id)

    return discounts

@router.post("/", response_model=DiscountOut, status_code=201)
def create_discount(discount_data: DiscountCreate, db: Session = Depends(get_db)):
    discount = discount_repo.create_discount(db, discount_data)
    if not discount:
        raise HTTPException(status_code=400, detail="Failed to create discount.")
    return discount


@router.put("/{discount_id}", response_model=DiscountOut)
def update_discount(discount_id: int, discount_data: DiscountUpdate, db: Session = Depends(get_db)):
    updated = discount_repo.update_discount(db, discount_id, discount_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Discount not found.")
    return updated

@router.delete("/{discount_id}", status_code=204)
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    success = discount_repo.delete_discount(db, discount_id)
    if not success:
        raise HTTPException(status_code=404, detail="Discount not found.")
    return