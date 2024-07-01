import argparse
from dao.models import Base
from dao.sql_db_manager import SqlDbManager
from utils.env_vars import SQL_ENGINE
from utils.logger import Logger
from services.gmail_service import GmailService
from utils.constants import DEFAULT_FETCH_LIMIT

log = Logger(__name__).get_logger()


def fetch_and_store_gmail(limit: int, flush: bool):
    log.info("Starting Gmail fetching and storing process...")

    sql_db_manager = SqlDbManager()
    email_service = GmailService(sql_db_manager)

    try:
        if flush:
            Base.metadata.drop_all(SQL_ENGINE)
            Base.metadata.create_all(SQL_ENGINE)
    except Exception as e:
        log.error(f"Error while flushing tables: {e}")

    try:
        emails = email_service.fetch_emails(limit)
        log.info(f"Fetched {len(emails)} emails from Gmail.")
        email_service.store_email(emails)
        log.info(f"Successfully stored {len(emails)} emails in the database.")
    except Exception as e:
        log.error(f"Error during email fetching or storing: {e}")

    log.info("Gmail fetching and storing process completed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to load emails to MySQL DB")
    parser.add_argument("--flush", type=bool, help="To Drop records in MySQL DB, eg: True/False",
                        required=False, default=False)
    parser.add_argument("--limit", type=int, help="Gmail fetch limit, give values between 1 to 20",
                        required=False, default=DEFAULT_FETCH_LIMIT)
    args = parser.parse_args()
    fetch_and_store_gmail(args.limit, args.flush)

