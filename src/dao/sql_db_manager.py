from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import inspect
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


class SqlDbManager:
    def __init__(self, engine):
        self._engine = engine
        session_factory = sessionmaker(engine)
        self.sql_session_obj = scoped_session(session_factory)

    def save(self, model_object):
        with self.sql_session_obj() as sql_session:
            try:
                sql_session.add(model_object)
                sql_session.commit()
                log.debug(f"Successfully saved object of type {type(model_object)}")
            except Exception as e:
                sql_session.rollback()
                log.error(f"Error saving object: {e}")
                raise

    def execute_query(self, query):
        log.debug(f"Executing SQL query: {inspect(query).compile(dialect=self._engine.dialect)}")
        with self.sql_session_obj() as sql_session:
            try:
                results = sql_session.execute(query).all()
                return results
            except Exception as e:
                log.error(f"Error executing query: {e}")
                raise
            finally:
                sql_session.close()

    def close_connection(self):
        self.sql_session_obj.remove()
        log.info(f"Closed connection to the database.")
