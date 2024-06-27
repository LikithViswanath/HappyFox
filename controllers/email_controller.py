from services.email_service import EmailService
from services.rule_service import RuleService


class EmailController:
    def __init__(self, rules_file):
        self.email_service = EmailService()
        self.rule_service = RuleService(rules_file)

    def fetch_and_store_emails(self):
        self.email_service.fetch_and_store_emails()

    def process_emails(self):
        self.rule_service.process_emails()
