from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
import configparser
from pathlib import Path


def parse_db_config_file(file_path=None):
    if file_path is None:
        file_path = 'db_config.ini'

    db_config_file = Path(file_path)
    config = configparser.ConfigParser()
    config['CONNECTION'] = {}

    if not db_config_file.is_file():
        with open(file_path, 'w') as configfile:  # save
            config.write(configfile)

    config.read(file_path)

    params = {}
    params_prefix = "params."

    for each_key in config['CONNECTION']:
        if each_key[0:7] == params_prefix:
            params[each_key[7:]] = config['CONNECTION'][each_key]

    return config, params


def get_db_config(db=None):
    config, params = parse_db_config_file()

    dialect = config['CONNECTION']['dialect']
    user = config['CONNECTION']['user']
    password = config['CONNECTION']['password']
    server_name = config['CONNECTION']['server_name']
    db_name = config['CONNECTION']['db_name']

    if db is not None:
        db_name = db

    url = '{}://{}:{}@{}/{}'.format(dialect, user, password, server_name, db_name)

    return url, params


@contextmanager
def session_maker(session):
    """provide a transactional scope around a series of operations."""
    session_ = session()
    try:
        yield session_
    except:
        session_.rollback()
        raise
    finally:
        session_.close()


def session_maker(db_config):
    connect_args = {'connect_timeout': 1000}
    connect_args.update(db_config[1])
    engine = create_engine(db_config[0], connect_args=connect_args, pool_size=20, pool_pre_ping=True,
                            pool_recycle=3600)

    return sessionmaker(bind=engine)


@contextmanager
def session_manager_news():
    db_config = get_db_config(db='prod_id_news')
    session = session_maker(db_config)()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
