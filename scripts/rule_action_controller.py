import json
import argparse
from dao.sql_db_manager import SqlDbManager
from services.action_service import GmailActionService
from utils.helper import RuleParser
from utils.env_vars import RULES_FILE
from utils.logger import Logger

log = Logger(__name__).get_logger()


def parse_rules_and_perform_actions(rules_meta):
    log.info("Starting email action processing...")

    sql_db_manager = SqlDbManager()
    action_service = GmailActionService(
        sql_db_manager=sql_db_manager
    )

    try:
        email_actions = RuleParser().parse_rules(rules_meta.get('test_cases'))
        action_service.perform_actions(email_actions)
    except Exception as e:
        log.error(f"Error during rule parsing or action execution: {e}")

    log.info("Finished email action processing.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to execute set of rules")
    parser.add_argument("--test_path", type=str, help="Testcase file path",
                        required=False, default=RULES_FILE)

    args = parser.parse_args()
    testcase_file = args.testcase_path

    with open(testcase_file, "r") as rules_file:
        rules_meta_json = json.load(rules_file)
        log.info(f"Loaded rules configuration from: {testcase_file}")

    parse_rules_and_perform_actions(rules_meta_json)
