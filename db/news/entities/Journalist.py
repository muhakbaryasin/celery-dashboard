from sqlalchemy import (
    String,
    Column,
)
from db.abstract.BaseEntity import BaseEntityIdNews


class Journalist(BaseEntityIdNews):
    __tablename__ = 'journalists'
    name = Column(String(length=255), nullable=False)
    photo = Column(String(length=255))
