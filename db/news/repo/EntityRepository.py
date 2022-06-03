from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from db.abstract.BaseEntity import BaseEntityIdNews
from db.session_manager import session_manager_news
from models.Logger import Logger


class EntityRepository(object):
    def __init__(self, entity_model, session_manager_=None):
        self.entity_model = entity_model
        self.session_manager = session_manager_

        if session_manager_ is None:
            self.session_manager = session_manager_news

    def add(self, entity):
        with self.session_manager() as session:
            entry = self.entity_model(**entity)
            session.add(entry)
            session.commit()
            session.refresh(entry)
        return entry

    def update(self, entry_update):
        with self.session_manager() as session:
            entry = session.query(self.entity_model).filter(self.entity_model.id == entry_update.id).one_or_none()

            if entry is None:
                return

            mapper = inspect(entry)

            for column in mapper.attrs:
                type_entry = type(entry.__getattribute__(column.key))

                if type_entry is InstrumentedList:
                    continue

                if EntityRepository.hasParentBaseEntity(type_entry):
                    continue

                setattr(entry, column.key, entry_update.__getattribute__(column.key))

            entry.updated_at = datetime.now()
            session.commit()
            session.refresh(entry)
        return entry

    def get(self, id_):
        with self.session_manager() as session:
            return session.query(self.entity_model).filter(self.entity_model.id == id_).one_or_none()

    def get_all(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).all()

    def get_first(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).first()

    def get_oldest_updated(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).order_by(self.entity_model.updated_at.asc()).first()

    def get_latest_updated(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).order_by(self.entity_model.updated_at.desc()).first()

    def get_latest_created(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).order_by(self.entity_model.created_at.desc()).first()

    def get_created_at_date(self, date):
        from_ = datetime.strptime('{} {}'.format(datetime.strftime(date, '%Y-%m-%d'), '00:00:00'), '%Y-%m-%d %H:%M:%S')
        to_ = datetime.strptime('{} {}'.format(datetime.strftime(date, '%Y-%m-%d'), '23:59:59'), '%Y-%m-%d %H:%M:%S')

        with self.session_manager() as session:
            return session.query(self.entity_model).filter(self.entity_model.created_at >= from_,
                                                           self.entity_model.created_at <= to_).\
                order_by(self.entity_model.created_at.asc()).all()

    def delete(self, id_):
        entry = self.get(id_)

        with self.session_manager() as session:
            session.delete(entry)
            session.commit()

        return entry

    @staticmethod
    def updateEntityFromDict(entity_obj, entity_dict):
        for each_property in entity_obj.__dict__:
            if each_property in entity_dict:
                try:
                    setattr(entity_obj, each_property, entity_dict[each_property])
                except AttributeError as ae:
                    error_message = 'Unable to setattr of {}::{} -> {}'.format(type(entity_obj), each_property, str(ae))
                    print(error_message)
                    Logger.warning(error_message)

        return entity_obj

    @staticmethod
    def hasParentBaseEntity(obj, loop=0):
        if loop > 5:
            return False

        bases = obj.__bases__

        result = None

        if len(bases) > 0:
            if bases[0] is BaseEntityIdNews:
                return True

            result = EntityRepository.hasParentBaseEntity(bases[0], loop=loop+1)

        return result

    def count(self):
        with self.session_manager() as session:
            return session.query(self.entity_model).count()
