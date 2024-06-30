from datetime import datetime, timedelta
from dao.models import Email
from entities.rule_entity import Rule
from utils.constants import AND, OR
from sqlalchemy import Column


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

            print(rule.field, rule.value, rule.predicate)

            if rule.time:
                kwargs = {rule.time: rule.value}
                query = query_method(column, rule.value, **kwargs)
            else:
                kwargs = {}
                query = query_method(column, rule.value, **kwargs)

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
        print(column.ilike(f"%{value.lower()}%"))
        return column.ilike(f"%{value.lower()}%")

    def not_contains(self, column: Column, value: str, **kwargs):
        return not column.ilike(f"%{value.lower()}%")

    def equals(self, column: Column, value: str, **kwargs):
        return column == value

    def not_equals(self, column: Column, value, **kwargs):
        return column != value
