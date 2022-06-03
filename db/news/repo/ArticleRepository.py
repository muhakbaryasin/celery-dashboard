from datetime import datetime
from sqlalchemy import or_
from db.news.repo.EntityRepository import EntityRepository
from db.news.entities.Article import Article


class ArticleRepository(EntityRepository):
    def __init__(self, session_manager_=None):
        super().__init__(Article, session_manager_=session_manager_)

    def get_by_title(self, title):
        with self.session_manager() as session:
            return session.query(self.entity_model).filter(self.entity_model.title_original == title).one_or_none()

    def get_last_created(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).order_by(self.entity_model.created_at.desc()).first()

    def get_not_summarized(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).filter(
                or_(
                    self.entity_model.title_eng == None, self.entity_model.summary_original == None,
                    self.entity_model.summary_eng == None
                )
            ).order_by(self.entity_model.created_at.asc()).limit(9).all()

    def get_created_by_media_at_date(self, media_id, date):
        from_ = datetime.strptime('{} {}'.format(datetime.strftime(date, '%Y-%m-%d'), '00:00:00'), '%Y-%m-%d %H:%M:%S')
        to_ = datetime.strptime('{} {}'.format(datetime.strftime(date, '%Y-%m-%d'), '23:59:59'), '%Y-%m-%d %H:%M:%S')

        with self.session_manager() as session:
            return session.query(self.entity_model).filter(
                self.entity_model.media_id == media_id,
                self.entity_model.created_at >= from_,
                self.entity_model.created_at <= to_
            ).order_by(self.entity_model.created_at.asc()).all()

    def get_filtered(self, filter_text, start, length):
        with self.session_manager() as session:
            result = session.query(self.entity_model)

            if filter_text != "":
                result = result.filter(or_(
                    self.entity_model.title_original.like("%{}%".format(filter_text)),
                    self.entity_model.content.like("%{}%".format(filter_text))
                ))

            count = result.count()
            result = result.limit(length).offset(start).all()

            return count, result
