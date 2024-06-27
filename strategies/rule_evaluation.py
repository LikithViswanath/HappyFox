class RuleEvaluator:
    def evaluate(self, email, rule):
        field = rule['field']
        predicate = rule['predicate']
        value = rule['value']

        email_field_value = self._extract_email_field_value(email, field)
        return self._evaluate_rule(email_field_value, predicate, value)

    def _extract_email_field_value(self, email, field):
        # For simplicity, assume 'From', 'Subject', 'Message', 'Received Date/Time'
        if field == 'From':
            return email.payload['headers'][0]['value']  # Simplified
        elif field == 'Subject':
            return email.payload['headers'][1]['value']  # Simplified
        elif field == 'Message':
            return email.snippet
        elif field == 'Received Date/Time':
            return email.payload['headers'][2]['value']  # Simplified
        return None

    def _evaluate_rule(self, email_value, predicate, rule_value):
        if predicate == 'Contains':
            return rule_value in email_value
        elif predicate == 'Does not Contain':
            return rule_value not in email_value
        elif predicate == 'Equals':
            return email_value == rule_value
        elif predicate == 'Does not equal':
            return email_value != rule_value
        # Add more conditions for date comparisons if needed
        return False
