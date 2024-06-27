from utils.oauth import authenticate_gmail
from repositories.email_repository.py import EmailRepository
from models.email import Email

class EmailService:
    def __init__(self):
        self.email_repo = EmailRepository()

    def fetch_and_store_emails(self):
        service = authenticate_gmail()
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email = Email.from_dict({
                'id': msg['id'],
                'snippet': msg['snippet'],
                'payload': msg['payload']
            })
            self.email_repo.save(email)
