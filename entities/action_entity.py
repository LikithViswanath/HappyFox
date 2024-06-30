class EmailAction:
    def __init__(self, rules, condition, action_payloads, rule_description):
        self.rules = rules
        self.rule_description = rule_description
        self.condition = condition
        self.action_payloads = action_payloads
