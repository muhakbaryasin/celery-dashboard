import contextlib
from mysql.connector import connect, Error
from db.session_manager import parse_db_config_file


@contextlib.contextmanager
def connection(**dbconf):
    conn = connect(**dbconf)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def cursorman(result=False, **dbconf):
    with connection(**dbconf) as conn:
        if result is False:
            conn.commit()

        cursor = conn.cursor(dictionary=True, buffered=True)

        try:
            yield cursor
        finally:
            try:
                cursor.close()
            except Error:
                cursor.reset()


class MysqlNativeQuery(object):
    @staticmethod
    def db_config_to_mysql_conf_dict(file_path=None):
        config, params = parse_db_config_file(file_path=file_path)

        user = config['CONNECTION']['user']
        password = config['CONNECTION']['password']
        server_name = config['CONNECTION']['server_name']
        db_name = config['CONNECTION']['db_name']

        config_dict = {
            "host": server_name,
            "user": user,
            "database": db_name,
            "password": password
        }

        config_dict.update(params)
        return config_dict

    @staticmethod
    def run(query, values=(), result=False, result_many=False, db_name=None):
        db_conf = MysqlNativeQuery.db_config_to_mysql_conf_dict()
        db_conf['database'] = db_name

        with cursorman(result=result, **db_conf) as cursor:
            cursor.execute(query, values)

            if result and result_many:
                return cursor.fetchall()
            elif result:
                return cursor.fetchone()
