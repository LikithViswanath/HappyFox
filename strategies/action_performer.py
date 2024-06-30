from services.authentication_service import EmailAuthenticationService


class EmailActionPerformer:

    def __init__(self, email_authentication_service: EmailAuthenticationService):
        self.service = email_authentication_service.get_service()

    def perform_action(self, payload):
        request = (self.service.users().messages().batchModify(userId="me", body=payload))
        request.execute()
