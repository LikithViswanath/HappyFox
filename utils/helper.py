from datetime import datetime, timedelta
from utils.constants import AND, OR
from sqlalchemy import Column
from entities.gmail_entity import GmailEntity
from dao.models import Email
from utils.constants import (ALLOWED_PREDICATES, ALLOWED_VALUE_TYPES, DATETIME_FIELDS, ALLOWED_TIME_VALUES,
                             ALLOWED_FIELDS, ALLOWED_LABELS,LABEL_MAPPER)
from entities.rule_entity import Rule
from entities.action_entity import GmailAction
from utils.logger import Logger

log = Logger(__name__).get_logger()


class Utility:
    def email_meta_data_to_model(self, email_meta_data):
        email = GmailEntity(email_meta_data)
        return Email(**{
            "id": email.get_id(),
            "thread_id": email.get_thread_id(),
            "to_email": email.get_to_email(),
            "from_email": email.get_from_email(),
            "subject": email.get_subject(),
            "body": email.get_body(),
            "received_date": email.get_received_date()
        })


class QueryBuilder:

    def build_action_query(self, rules, action_condition):

        action_query = None

        for rule in rules:

            if not isinstance(rule, Rule):
                raise TypeError(f'Rule must be of type {Rule}')

            query_method = getattr(self, rule.predicate, None)

            if query_method is None:
                raise ValueError(f'Rule {rule.predicate} is not defined')

            column = Email.getattr(rule.field)

            log.debug(
                f"Building query for rule: field - {rule.field}, predicate - {rule.predicate}, "
                f"value - {rule.value}, time - {rule.time}")

            try:
                if rule.time:
                    kwargs = {rule.time: rule.value}
                    query = query_method(column, **kwargs)
                else:
                    kwargs = {}
                    query = query_method(column, rule.value, **kwargs)
            except (ValueError, TypeError) as e:
                log.error(f"Error building query for rule: {e}")
                continue

            if action_query is None:
                action_query = query
            else:
                if action_condition == AND:
                    action_query = action_query & query
                elif action_query == OR:
                    action_query = action_query | query

        return action_query

    def less_than(self, column: Column, **kwargs):
        bound_range = datetime.now().today() - timedelta(**kwargs)
        return column > bound_range

    def greater_than(self, column: Column, **kwargs):
        bound_range = datetime.now().today() - timedelta(**kwargs)
        return column < bound_range

    def contains(self, column: Column, value: str, **kwargs):
        return column.ilike(f"%{value.lower()}%")

    def not_contains(self, column: Column, value: str, **kwargs):
        return not column.ilike(f"%{value.lower()}%")

    def equals(self, column: Column, value: str, **kwargs):
        return column == value

    def not_equals(self, column: Column, value, **kwargs):
        return column != value


class RuleParser:

    def __init__(self):
        self.valid_fields = ALLOWED_FIELDS

    def parse_rules(self, rules_meta_json):

        action_list = []
        for rule_meta in rules_meta_json:

            raw_rules = rule_meta.get('rules')
            rule_description = rule_meta.get('description')
            condition = rule_meta.get('condition')
            action_payload = self._parse_action_to_payload(rule_meta.get('action'))

            log.debug(f"Parsing rule: rule_description - {rule_description}")

            rules = []

            for raw_rule in raw_rules:
                try:
                    parse_field = self._validate_and_parse_field(raw_rule['field'])
                    log.debug(f"Validated field: {parse_field}")
                    parse_predicate = self._validate_and_parse_predicate(raw_rule['predicate'])
                    log.debug(f"Validated predicate: {parse_predicate}")
                    parse_value, parsed_time = self._validate_and_parse_value(
                        raw_rule['field'],
                        raw_rule['value']
                    )
                except Exception as e:
                    log.error(f"Error validating rule: {e}")
                    raise e

                rule = Rule(
                    field=parse_field,
                    predicate=parse_predicate,
                    value=parse_value,
                    time=parsed_time
                )
                rules.append(rule)

            action_list.append(GmailAction(
                rules=rules,
                rule_description=rule_description,
                condition=condition,
                action_payload=action_payload
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

            if int(val) > ALLOWED_TIME_VALUES[time]:
                raise ValueError(f"Invalid value, supported time shift - {ALLOWED_TIME_VALUES[time]}")

            return int(val), time
        else:
            return value, None

    def _parse_action_to_payload(self, action):
        action_payloads = {
            "removeLabelIds": [],
            "addLabelIds": [],
        }
        for x in action:
            if x not in ALLOWED_LABELS:
                raise ValueError(f"Invalid action, supported action types are - {ALLOWED_LABELS}")
            if x in LABEL_MAPPER:
                label_payload = LABEL_MAPPER[x]
                if "removeLabelIds" in label_payload:
                    action_payloads["removeLabelIds"].append(label_payload["removeLabelIds"])
                elif "addLabelIds" in label_payload:
                    action_payloads["addLabelIds"].append(label_payload["addLabelIds"])
            else:
                action_payloads["addLabelIds"].append(x.upper())

        return action_payloads
