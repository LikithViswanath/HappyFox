class Email:
    def __init__(self, id, snippet, payload):
        self.id = id
        self.snippet = snippet
        self.payload = payload

    @staticmethod
    def from_dict(email_dict):
        return Email(email_dict['id'], email_dict['snippet'], email_dict['payload'])
