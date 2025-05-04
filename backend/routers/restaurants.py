from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.menu import MenuRepository
from repositories.restaurant import RestaurantRepository
from schemas.menu_item import MenuItemRead
from schemas.restaurant import RestaurantOut, RestaurantCreate, RestaurantUpdate, RestaurantOutScore

router = APIRouter()

restaurant_repo = RestaurantRepository()
menu_repo = MenuRepository()


@router.get("/search", response_model=List[RestaurantOut])
def search_restaurants(query: str, db: Session = Depends(get_db)):
    return restaurant_repo.search_restaurants(db, query)


@router.post("/create", response_model=RestaurantOut)
def create_restaurant(restaurant_in: RestaurantCreate, db: Session = Depends(get_db)):
    return restaurant_repo.create(db, restaurant_in.model_dump())


@router.get("/all", response_model=List[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return restaurant_repo.get_all(db)


@router.get("/user/{user_id}", response_model=Optional[RestaurantOut])
def get_restaurant_by_user_id(user_id: int, db: Session = Depends(get_db)):
    restaurant = restaurant_repo.get_by_user_id(db, user_id)
    if not restaurant:
        return None
    return restaurant


@router.get("/with-scores", response_model=list[RestaurantOutScore])
def list_restaurants_with_scores(db: Session = Depends(get_db)):
    return restaurant_repo.get_restaurants_with_score(db)


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = restaurant_repo.get(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(restaurant_id: int, restaurant_in: RestaurantUpdate, db: Session = Depends(get_db)):
    restaurant = restaurant_repo.get(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant_repo.update(db, restaurant, restaurant_in.model_dump(exclude_unset=True))


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = restaurant_repo.get(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_repo.delete(db, restaurant_id)
    return None


@router.get("/{restaurant_id}/menu", response_model=List[MenuItemRead])
def get_menu_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    menu_items = menu_repo.get_by_restaurant_id(db, restaurant_id)
    return menu_items
