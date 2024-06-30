from config.constants import ALLOWED_PREDICATES, ALLOWED_VALUE_TYPES, DATETIME_FIELDS, ALLOWED_TIME_VALUES, ALLOWED_FIELDS
from entities.rule_entity import Rule
from entities.action_entity import EmailAction


class RuleParser:

    def __init__(self):
        self.valid_fields = ALLOWED_FIELDS

    def parse_rules(self, rules_meta_json):

        action_list = []
        for rule_meta in rules_meta_json:

            raw_rules = rule_meta.get('rules')
            rule_description = rule_meta.get('description')
            condition = rule_meta.get('condition')
            action_payloads = self._parse_action_to_payloads(rule_meta.get('action'))

            rules = []

            for raw_rule in raw_rules:

                parse_field = self._validate_and_parse_field(raw_rule['field'])
                parse_predicate = self._validate_and_parse_predicate(raw_rule['predicate'])
                parse_value, parsed_time = self._validate_and_parse_value(
                    raw_rule['field'],
                    raw_rule['value']
                )
                rule = Rule(
                    field=parse_field,
                    predicate=parse_predicate,
                    value=parse_value,
                    time=parsed_time
                )
                rules.append(rule)

            action_list.append(EmailAction(
                rules=rules,
                rule_description=rule_description,
                condition=condition,
                action_payloads=action_payloads
            ))

        return action_list

    def _validate_and_parse_field(self, field):
        if field not in self.valid_fields:
            raise ValueError(f"Invalid Field name, please give anyone of these - {self.valid_fields}")

        return field

    def _validate_and_parse_predicate(self, predicate):
        if predicate not in ALLOWED_PREDICATES:
            raise ValueError(f"Invalid predicate name, please give anyone of these - {ALLOWED_PREDICATES}")

        return predicate

    def _validate_and_parse_value(self, field, value):
        if not isinstance(value, str):
            raise ValueError(f"Invalid value name, supported value types are - {ALLOWED_VALUE_TYPES}")

        if field in DATETIME_FIELDS:
            value = value.split(' ')
            val = value[0]
            time = value[1]

            if time not in ALLOWED_TIME_VALUES.keys():
                raise ValueError(f"Invalid value, supported time shift - {ALLOWED_TIME_VALUES.keys()}")

            if val > ALLOWED_TIME_VALUES[time]:
                raise ValueError(f"Invalid value, supported time shift - {ALLOWED_TIME_VALUES[time]}")

            return val, time
        else:
            return value, None

    def _parse_action_to_payloads(self, action):
        action_mapper = {
            "read": {"removeLabelIds": ["UNREAD"]},
            "unread": {"addLabelIds": ["UNREAD"]},
        }
        for x in action:
            return action_mapper[x] if action_mapper.get(x) else {"addLabelIds": [action.upper()]}
