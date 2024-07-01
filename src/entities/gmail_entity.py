import base64
from datetime import datetime


class GmailEntity(object):
    def __init__(self, raw_data):
        self.data = raw_data
        self.payload = raw_data['payload']
        self.headers = self.payload['headers']
        self.parts = self.payload.get('parts', [])
        self.body = self.payload.get('body', None)

    def _fetch_header_data(self, key):
        for header in self.headers:
            if header['name'] == key:
                return header['value']
        return None

    def get_id(self):
        return self.data['id']

    def get_thread_id(self):
        return self.data['threadId']

    def get_to_email(self):
        return self._fetch_header_data('To')

    def get_from_email(self):
        return self._fetch_header_data('From')

    def get_subject(self):
        return self._fetch_header_data('Subject')

    def get_body(self):
        if self.parts:
            text_body = None
            html_body = None
            parts_data = self.parts
            for part in self.parts:
                if part['mimeType'] == 'multipart/alternative':
                    parts_data = part['parts']
                    break

            for part in parts_data:
                if part['mimeType'] == 'text/plain':
                    text_body = base64.urlsafe_b64decode(part['body']['data'])
                if part['mimeType'] == 'text/html':
                    html_body = base64.urlsafe_b64decode(part['body']['data'])
            return text_body or html_body

        return None

    def get_received_date(self):
        internal_date = self.data['internalDate']
        datetime_obj = datetime.fromtimestamp(int(internal_date) / 1000)
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
