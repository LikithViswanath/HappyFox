from sqlalchemy import create_engine

host = 'localhost'
user = 'root'
password = '5134083'
DATA_BASE_NAME = 'mysql'
DATA_BASE_URL = f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{DATA_BASE_NAME}'
SQL_ENGINE = create_engine(DATA_BASE_URL)
DEFAULT_FETCH_LIMIT = 100

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
CREDENTIALS_FILE = '../config/credentials.json'
TOKEN_FILE = '../config/token.json'
RULES_FILE = '../config/rules.json'
USER_ID = "magnetoxmen6@gmail.com"