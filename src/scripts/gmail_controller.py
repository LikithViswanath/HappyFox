import argparse
from src.dao.models import flush_db_tables
from src.dao.sql_db_manager import SqlDbManager
from src.utils.logger import Logger
from src.services.gmail_service import GmailService
from src.utils.constants import DEFAULT_FETCH_LIMIT

log = Logger(__name__).get_logger()


def fetch_and_store_gmail(limit: int, flush: bool):
    log.info("Starting Gmail fetching and storing process...")

    sql_db_manager = SqlDbManager()
    email_service = GmailService(sql_db_manager)

    try:
        if flush:
            log.info("Flushing tables...")
            flush_db_tables()
            log.info("tables flushed")
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

