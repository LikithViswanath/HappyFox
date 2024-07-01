import requests
from sqlalchemy import select
from dao.sql_db_manager import SqlDbManager
from entities.action_entity import GmailAction
from dao.models import Email
from utils.helper import QueryBuilder
from utils.logger import Logger
from services.auth_service import GmailAuthenticationService

log = Logger(__name__).get_logger()


class GmailActionService(GmailAuthenticationService):
    def __init__(self, sql_db_manager: SqlDbManager):
        super().__init__()
        self.sql_db_manager = sql_db_manager
        self.query_builder = QueryBuilder()

    def perform_actions(self, email_actions):

        log.info("Starting email action processing...")

        for email_action in email_actions:

            if not isinstance(email_action, GmailAction):
                raise ValueError('Action must be an instance of EmailAction')

            log.info(f"Processing email action: type={email_action.action_payload}, "
                     f"rule_description={email_action.rule_description}, condition={email_action.condition}")

            try:
                action_query = self.query_builder.build_action_query(email_action.rules, email_action.condition)
                query_result = self.sql_db_manager.execute_query(select(Email).filter(action_query))
                num_matched_emails = len(query_result)
                log.info(f"Found {num_matched_emails} emails matching the action criteria.")
            except Exception as e:
                log.error(f"Error processing email action: {e}")
                continue

            self._modify_labels(email_action.action_payload, query_result)

        log.info("Finished email action processing.")

    def _modify_labels(self, payload, email_models):
        for email_model, in email_models:
            log.info(f"Modifying labels for email {email_model.id}")
            try:
                response = requests.post(
                    url=f"https://gmail.googleapis.com/gmail/v1/users/{self.user_id}/messages/{email_model.id}/modify",
                    data=payload,
                    headers=self.auth_headers
                )
                labels = response.json().get('labelIds')
                if response.status_code == 200:
                    log.info(f"Successfully modified labels for email {email_model.id}: {labels}")
                else:
                    log.error(f"Failed to modify labels for email {email_model.id}: {response.text}")
            except Exception as e:
                log.error(f"Error making request to Gmail API for email {email_model.id}: {e}")
                continue
