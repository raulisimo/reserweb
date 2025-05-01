from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from constants.roles import RoleEnum
from dependencies.authentication import get_admin_user
from dependencies.database import get_db
from models.roles import Role
from models.user import User
from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate, UserRead

router = APIRouter()
user_repo = UserRepository()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    if user_repo.get_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    role = db.query(Role).filter(Role.name == RoleEnum.CLIENT).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Default role 'client' not found.")

    new_user = user_repo.create_with_role(db, user, role_id=role.id)
    return UserRead(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        phone=new_user.phone,
        role=new_user.role.name
    )


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    return user_repo.get_all_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_admin_user)):
    updated_user = user_repo.update(db, user_id, user_update.model_dump(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
        phone=updated_user.phone,
        role=updated_user.role.name
    )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    success = user_repo.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
