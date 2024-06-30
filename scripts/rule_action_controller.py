import json
from dao.sql_db_manager import SqlDbManager
from services.authentication_service import EmailAuthenticationService
from services.action_service import EmailActionService
from strategies.action_performer import EmailActionPerformer
from strategies.rule_parse import RuleParser
from strategies.query_builder import QueryBuilder
from utils.gmail_config import RULES_FILE


def parse_rules_and_perform_actions():

    with open(RULES_FILE, "r") as rules_file:
        rules_meta_json = json.load(rules_file)

    email_actions = RuleParser().parse_rules(rules_meta_json.get('test_cases'))

    query_builder = QueryBuilder()
    email_authentication_service = EmailAuthenticationService()
    email_action_performer = EmailActionPerformer(email_authentication_service)
    sql_db_manager = SqlDbManager()
    action_service = EmailActionService(
        sql_db_manager=sql_db_manager,
        email_action_performer=email_action_performer,
        query_builder=query_builder
    )
    action_service.perform_actions(email_actions)

if __name__ == '__main__':
    parse_rules_and_perform_actions()
