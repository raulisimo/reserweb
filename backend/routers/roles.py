from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.roles import RolesRepository
from schemas.roles import RoleOut

router = APIRouter()
roles_repo = RolesRepository()


@router.get("/get-standard-roles", response_model=List[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return roles_repo.fetch_standard_roles(db)
