class GmailAction:
    def __init__(self, rules, predicate, action_payload, rule_description):
        self.rules = rules
        self.rule_description = rule_description
        self.predicate = predicate
        self.action_payload = action_payload
