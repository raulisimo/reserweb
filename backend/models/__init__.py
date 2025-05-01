from sqlalchemy.orm import DeclarativeBase


class ModelBase(DeclarativeBase):
    pass


import models.roles
import models.restaurants
import models.user
import models.booking
import models.menu_item
import models.discounts

metadata = ModelBase.metadata
