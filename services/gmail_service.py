from utils.helper import Utility
from utils.logger import Logger
from dao.sql_db_manager import SqlDbManager
from services.auth_service import GmailAuthenticationService
from utils.constants import DEFAULT_FETCH_LIMIT

log = Logger(__name__).get_logger()


class GmailService(GmailAuthenticationService):

    def __init__(self, sql_db_manager: SqlDbManager):
        super().__init__()
        self.db_manager = sql_db_manager

    def fetch_emails(self, limit=DEFAULT_FETCH_LIMIT):
        log.info(f"Fetching emails with limit: {limit}")
        try:
            results = self.service.users().messages().list(userId='me', maxResults=limit).execute()
            messages = results.get('messages', [])
            utility = Utility()
            emails = []

            for msg in messages:
                log.debug(f"Fetching email details for ID: {msg['id']}")
                email_meta_data = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                emails.append(utility.email_meta_data_to_model(email_meta_data))

            log.info(f"Fetched {len(emails)} emails.")
            return emails
        except Exception as e:
            log.error(f"Error fetching emails: {e}")
            return []

    def store_email(self, emails):
        for email in emails:
            try:
                log.info(f"Storing email with ID: {email.id}")
                self.db_manager.save(email)
            except Exception as e:
                log.error(f"Error storing email with ID: {email.id} - {e}")

        log.info(f"Successfully stored {len(emails)} emails.")
