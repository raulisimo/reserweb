from sqlalchemy.orm import Session

from models.menu_item import MenuItem
from repositories.base import BaseRepository
from schemas.menu_item import MenuItemUpdate, MenuItemCreate


class MenuRepository(BaseRepository[MenuItem]):
    def __init__(self):
        super().__init__(MenuItem)

    def get_by_restaurant_id(self, db: Session, restaurant_id: int):
        return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

    def create_menu_item(self, db: Session, restaurant_id: int, menu_item: MenuItemCreate):
        # Create a new MenuItem instance
        db_menu_item = MenuItem(
            name=menu_item.name,
            description=menu_item.description,
            price=menu_item.price,
            is_available=menu_item.is_available,
            restaurant_id=restaurant_id
        )

        db.add(db_menu_item)
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item

    def update_menu_item(self, db: Session, menu_item_id: int, data: MenuItemUpdate):
        item = db.query(MenuItem).filter_by(id=menu_item_id).first()
        if not item:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    def delete_menu_item(self, db: Session, menu_item_id: int) -> bool:
        item = db.query(MenuItem).filter_by(id=menu_item_id).first()
        if not item:
            return False
        db.delete(item)
        db.commit()
        return True
