from sqlalchemy.orm import Session

from models.roles import Role
from repositories.base import BaseRepository


class RolesRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def fetch_standard_roles(self, db: Session):
        return db.query(Role).filter(~Role.name.ilike(f"%admin%")
                                     ).all()
