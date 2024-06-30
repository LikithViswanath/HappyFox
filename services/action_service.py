from sqlalchemy import select
from dao.sql_db_manager import SqlDbManager
from entities.action_entity import EmailAction
from dao.models import Email
from strategies.action_performer import EmailActionPerformer
from strategies.query_builder import QueryBuilder

class EmailActionService:
    def __init__(self,
                 sql_db_manager: SqlDbManager,
                 email_action_performer: EmailActionPerformer,
                 query_builder: QueryBuilder
                 ):
        self.sql_db_manager = sql_db_manager
        self.email_action_performer = email_action_performer
        self.query_builder = query_builder

    def perform_actions(self, email_actions):

        for email_action in email_actions:

            if not isinstance(email_action, EmailAction):
                raise ValueError('Action must be an instance of EmailAction')

            action_query = self.query_builder.build_action_query(email_action.rules, email_action.condition)

            query_result = self.sql_db_manager.execute_query(select(Email).filter(action_query))

            filtered_ids = [res[0].id for res in query_result]
            filtered_ids = list(set(filtered_ids))

            payload = email_action.action_payloads
            payload['ids'] = filtered_ids
            self.email_action_performer.perform_action(payload)

