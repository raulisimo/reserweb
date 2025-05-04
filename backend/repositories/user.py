from typing import Optional

from sqlalchemy.orm import Session

from models.roles import Role
from models.user import User
from repositories.base import BaseRepository
from schemas.user import UserCreate
from services.security import hash_password


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_all_users(self, db: Session):
        users_query = db.query(
            User.id,
            User.name,
            User.email,
            User.phone,
            User.created_at,
            Role.name.label('role'),
        ).join(User, User.role_id == Role.id)
        users = users_query.all()
        return users

    def create_with_role(self, db: Session, user_create: UserCreate, role_id: int) -> User:
        # Hash the password before creating the user
        hashed_password = hash_password(user_create.password)

        db_user = User(
            name=user_create.name,
            email=user_create.email,
            phone=user_create.phone,
            password_hash=hashed_password,
            role_id=role_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def update(self, db: Session, user_id: int, user_update: dict) -> Optional[User]:
        user = self.get_by_id(db, user_id)
        if not user:
            return None

        if "role" in user_update:
            role = db.query(Role).filter_by(name=user_update["role"]).first()
            if not role:
                raise ValueError(f"Role '{user_update['role']}' not found.")
            user.role = role
            user_update.pop("role")

        if "role_id" in user_update:
            user.role_id = user_update["role_id"]
            user_update.pop("role_id")
        if "password" in user_update and user_update["password"]:
            user.password_hash = hash_password(user_update["password"])
            user_update.pop("password")
        for attr, value in user_update.items():
            setattr(user, attr, value)

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> bool:
        user = self.get_by_id(db, user_id)
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
