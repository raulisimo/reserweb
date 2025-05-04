from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.menu import MenuRepository
from schemas.menu_item import MenuItemOut, MenuItemUpdate, MenuItemCreate

router = APIRouter()

menu_repo = MenuRepository()


@router.post("/restaurant/{restaurant_id}/items", response_model=MenuItemOut, status_code=201)
def create_menu_item(
        restaurant_id: int,
        menu_item: MenuItemCreate,
        db: Session = Depends(get_db)
):
    created_item = menu_repo.create_menu_item(db, restaurant_id, menu_item)
    if not created_item:
        raise HTTPException(status_code=400, detail="Error creating menu item.")
    return created_item


@router.put("/{menu_item_id}", response_model=MenuItemOut)
def update_menu_item(menu_item_id: int, item_data: MenuItemUpdate, db: Session = Depends(get_db)):
    updated = menu_repo.update_menu_item(db, menu_item_id, item_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found.")
    return updated


@router.delete("/{menu_item_id}", status_code=204)
def delete_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    success = menu_repo.delete_menu_item(db, menu_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found.")
    return
