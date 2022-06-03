from sqlalchemy import (
    String,
    Column,
    Text,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship
from db.abstract.BaseEntity import BaseEntityIdNews
from db.news.entities.Media import Media
from db.news.entities.Language import Language
from db.news.entities.Journalist import Journalist


class Article(BaseEntityIdNews):
    __tablename__ = 'articles'
    slug = Column(String(length=255), nullable=False)
    url = Column(String(length=255), nullable=False)
    title_original = Column(String(length=255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary_original = Column(Text, nullable=True)
    title_eng = Column(String(length=255), nullable=True)
    summary_eng = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    date = Column(Date)
    media_id = Column(ForeignKey(Media.id))
    media = relationship(Media, lazy='joined', backref='article_media')
    language_id = Column(ForeignKey(Language.id))
    language = relationship(Language, lazy='joined', backref='article_language')
    journalist_id = Column(ForeignKey(Journalist.id))
    journalist = relationship(Journalist, lazy='joined', backref='article_journalist')
