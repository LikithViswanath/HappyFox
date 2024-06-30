from utils.model_mapper import EmailModelEntityMapper
from utils.logger import DualLogger
from dao.sql_db_manager import SqlDbManager
from services.authentication_service import EmailAuthenticationService
from config.constants import DEFAULT_FETCH_LIMIT

log = DualLogger(__name__).get_logger()


class EmailService:

    def __init__(self, email_authentication_service: EmailAuthenticationService, sql_db_manager: SqlDbManager):
        self.db_manager = sql_db_manager
        self.service = email_authentication_service.get_service()

    def fetch_emails(self, limit=DEFAULT_FETCH_LIMIT):
        results = self.service.users().messages().list(userId='me', maxResults=limit).execute()
        messages = results.get('messages', [])
        model_mapper = EmailModelEntityMapper()
        emails = []

        for msg in messages:
            email_meta_data = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            emails.append(model_mapper.email_meta_data_to_model(email_meta_data))

        return emails

    def store_email(self, emails):
        for email in emails:
            self.db_manager.save(email)
