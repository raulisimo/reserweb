from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from models.roles import Role
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin
from services.security import verify_password, create_access_token

router = APIRouter()

user_repo = UserRepository()


@router.post("/signup")
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if user with email already exists
    existing_user = user_repo.get_by_email(db, email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Get role from DB
    role = db.query(Role).filter(Role.name == user_create.role.lower()).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    user_repo.create_with_role(db, user_create, role_id=role.id)

    return {"message": "Account created successfully."}


@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, email=user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    token = create_access_token({"sub": user.email, "user_id": user.id, "role": user.role.name})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.name
        }
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully."}
