from db.news.repo.BaseNameEntityRepository import BaseNameEntityRepository
from db.news.entities.Journalist import Journalist


class JournalistRepository(BaseNameEntityRepository):
    def __init__(self, session_manager_=None):
        super().__init__(Journalist, session_manager_=session_manager_)