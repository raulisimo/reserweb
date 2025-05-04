from typing import Generic, TypeVar, Type, Optional, Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.orm import Session

from config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_all(self, db: Session) -> Sequence[Row[Any] | RowMapping | Any]:
        return db.scalars(select(self.model)).all()

    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> None:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
