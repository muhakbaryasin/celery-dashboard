from sqlalchemy import (
    String,
    Column
)

from db.abstract.BaseEntity import BaseEntityIdNews


class BaseNameEntityIdNews(BaseEntityIdNews):
    __abstract__ = True
    name = Column(String(length=255), unique=True)
