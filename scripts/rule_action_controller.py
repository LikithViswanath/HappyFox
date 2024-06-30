import json
from dao.sql_db_manager import SqlDbManager
from services.action_service import GmailActionService
from utils.helper import RuleParser
from utils.env_vars import RULES_FILE
from utils.logger import Logger

log = Logger(__name__).get_logger()


def parse_rules_and_perform_actions():
    log.info("Starting email action processing...")

    with open(RULES_FILE, "r") as rules_file:
        rules_meta_json = json.load(rules_file)
        log.info(f"Loaded rules configuration from: {RULES_FILE}")

    sql_db_manager = SqlDbManager()
    action_service = GmailActionService(
        sql_db_manager=sql_db_manager
    )

    try:
        email_actions = RuleParser().parse_rules(rules_meta_json.get('test_cases'))
        action_service.perform_actions(email_actions)
    except Exception as e:
        log.error(f"Error during rule parsing or action execution: {e}")

    log.info("Finished email action processing.")


if __name__ == '__main__':
    parse_rules_and_perform_actions()
