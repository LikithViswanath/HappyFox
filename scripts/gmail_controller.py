from dao.sql_db_manager import SqlDbManager
from services.email_service import EmailService
from services.authentication_service import EmailAuthenticationService

def fetch_and_store_email():
    sql_db_manager = SqlDbManager()
    email_authentication_service = EmailAuthenticationService()
    email_service = EmailService(
        email_authentication_service=email_authentication_service,
        sql_db_manager=sql_db_manager
    )
    emails = email_service.fetch_emails()
    email_service.store_email(emails)


if __name__ == '__main__':
    fetch_and_store_email()
