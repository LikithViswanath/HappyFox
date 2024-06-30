DEFAULT_FETCH_LIMIT = 10
TIME_ENTITIES = ["days", "weeks", "months"]
ALLOWED_FIELDS = ["to_email", "from_email", "subject", "body", "received_date"]
ALLOWED_PREDICATES = ["less_than", "greater_than", "contains", "equals", "not_equals"]
ALLOWED_VALUE_TYPES = ["string"]
DATETIME_FIELDS = ["received_date"]
ALLOWED_TIME_VALUES = {
    "weeks": 7,
    "months": 30,
    "days": 1
}
AND = 'all'
OR = 'any'
ALLOWED_LABELS = {'inbox', 'spam', 'trash', 'starred', 'read', 'unread'}
