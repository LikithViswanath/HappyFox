import json
import argparse
from src.services.action_service import GmailActionService
from src.utils.helper import RuleParser
from src.utils.env_vars import RULES_FILE
from src.utils.logger import Logger

log = Logger(__name__).get_logger()


def parse_rules_and_perform_actions(rules_meta):
    log.info("Starting email action processing...")

    action_service = GmailActionService()

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
    testcase_file = args.test_path

    with open(testcase_file, "r") as rules_file:
        rules_meta_json = json.load(rules_file)
        log.info(f"Loaded rules configuration from: {testcase_file}")

    parse_rules_and_perform_actions(rules_meta_json)
