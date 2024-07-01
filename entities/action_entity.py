class GmailAction:
    def __init__(self, rules, condition, action_payload, rule_description):
        self.rules = rules
        self.rule_description = rule_description
        self.condition = condition
        self.action_payload = action_payload
