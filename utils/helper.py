from entities.gmail_entity import EmailEntity
from dao.models import Email


class EmailModelEntityMapper:
    def email_meta_data_to_model(self, email_meta_data):
        email = EmailEntity(email_meta_data)
        return Email(**{
            "id": email.get_id(),
            "to_email": email.get_to_email(),
            "from_email": email.get_from_email(),
            "subject": email.get_subject(),
            "body": email.get_body(),
            "received_date": email.get_received_date()
        })
