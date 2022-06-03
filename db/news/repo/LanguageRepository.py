from db.news.repo.BaseNameEntityRepository import BaseNameEntityRepository
from db.news.entities.Language import Language


class LanguageRepository(BaseNameEntityRepository):
    def __init__(self, session_manager_=None):
        super().__init__(Language, session_manager_=session_manager_)
