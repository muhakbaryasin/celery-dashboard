from db.news.repo.EntityRepository import EntityRepository


class BaseNameEntityRepository(EntityRepository):
    def __init__(self, entity_model, session_manager_=None):
        super().__init__(entity_model, session_manager_=session_manager_)

    def get_by_name(self, name):
        with self.session_manager() as session:
            return session.query(self.entity_model).filter(self.entity_model.name == name).one_or_none()
