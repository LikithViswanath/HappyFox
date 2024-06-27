class Email:
    def __init__(self, email_id, snippet, payload):
        self.email_id = email_id
        self.snippet = snippet
        self.payload = payload

    @staticmethod
    def from_dict(email_dict):
        return Email(email_dict['id'], email_dict['snippet'], email_dict['payload'])
