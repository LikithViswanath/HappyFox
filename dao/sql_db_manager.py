from sqlalchemy.orm import scoped_session, sessionmaker
from config.sql_db_config import SQL_ENGINE


class SqlDbManager:
    def __init__(self):
        session_factory = sessionmaker(SQL_ENGINE)
        self.sql_session_obj = scoped_session(session_factory)

    def save(self, model_object):
        with self.sql_session_obj() as sql_session:
            try:
                sql_session.add(model_object)
                sql_session.commit()
            except Exception:
                sql_session.rollback()
                raise
            finally:
                sql_session.close()

    def execute_query(self, query):
        with self.sql_session_obj() as sql_session:
            try:
                results = sql_session.execute(query).all()
                return results
            except Exception:
                raise
            finally:
                sql_session.close()

    def close_connection(self):
        self.sql_session_obj.remove()
