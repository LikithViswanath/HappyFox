import json
from repositories.email_repository import EmailRepository
from strategies.rule_evaluation import RuleEvaluator
from strategies.action_performance import ActionPerformer

class RuleService:
    def __init__(self, rules_file):
        self.email_repo = EmailRepository()
        self.rules = self._load_rules(rules_file)
        self.rule_evaluator = RuleEvaluator()
        self.action_performer = ActionPerformer()

    def _load_rules(self, rules_file):
        with open(rules_file, 'r') as file:
            rules = json.load(file)
        return rules

    def process_emails(self):
        emails = self.email_repo.fetch_all()
        for email in emails:
            for rule in self.rules['rules']:
                if self.rule_evaluator.evaluate(email, rule):
                    self.action_performer.perform_action(email, rule['action'])
