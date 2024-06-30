from sqlalchemy import create_engine

host = 'localhost'
user = 'root'
password = '5134083'
DATA_BASE_NAME = 'HappyFox'
DATA_BASE_URL = f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{DATA_BASE_NAME}'
SQL_ENGINE = create_engine(DATA_BASE_URL)
DEFAULT_FETCH_LIMIT = 100
