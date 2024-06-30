from dao.sql_db_manager import SqlDbManager
from services.gmail_service import GmailService
from utils.logger import Logger

log = Logger(__name__).get_logger()


def fetch_and_store_gmail():
    log.info("Starting Gmail fetching and storing process...")

    sql_db_manager = SqlDbManager()
    email_service = GmailService(sql_db_manager)

    try:
        emails = email_service.fetch_emails()
        log.info(f"Fetched {len(emails)} emails from Gmail.")
        email_service.store_email(emails)
        log.info(f"Successfully stored {len(emails)} emails in the database.")
    except Exception as e:
        log.error(f"Error during email fetching or storing: {e}")

    log.info("Gmail fetching and storing process completed.")


if __name__ == '__main__':
    fetch_and_store_gmail()
