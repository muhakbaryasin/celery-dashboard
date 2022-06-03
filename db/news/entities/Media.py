from sqlalchemy import (
    String,
    Column,
)
from db.abstract.BaseNameEntity import BaseNameEntityIdNews


class Media(BaseNameEntityIdNews):
    __tablename__ = 'medias'
    logo = Column(String(length=255))
    url = Column(String(length=255), nullable=False)
