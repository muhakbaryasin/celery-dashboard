from db.news.repo.BaseNameEntityRepository import BaseNameEntityRepository
from db.news.entities.Media import Media


class MediaRepository(BaseNameEntityRepository):
    def __init__(self, session_manager_=None):
        super().__init__(Media, session_manager_=session_manager_)

    def count(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).count()
