from sqlalchemy.orm import Session

from constants.roles import RoleEnum
from models.roles import Role


def init_roles(db: Session) -> None:
    """Create default roles if they don't exist."""
    for role_name in RoleEnum:
        existing_role = db.query(Role).filter_by(name=role_name.value).first()
        if not existing_role:
            new_role = Role(name=role_name.value)
            db.add(new_role)
    db.commit()
