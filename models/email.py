class Email:
    def __init__(self, email_id, snippet, payload):
        self.packet_id = email_id
        self.snippet = snippet
        self.payload = payload

    @staticmethod
    def from_dict(email_dict):
        return Email(email_dict['id'], email_dict['snippet'], email_dict['payload'])

    def to_dict(self):
        email_dict = {'email_id': self.packet_id, 'snippet': self.snippet}
        return email_dict
