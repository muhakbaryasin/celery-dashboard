from sqlalchemy import (
    DateTime,
    Column,
    Integer,
)

from sqlalchemy.sql import func
from db.abstract.meta import BaseIdNews


class BaseEntityIdNews(BaseIdNews):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=False), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), default=func.now())
