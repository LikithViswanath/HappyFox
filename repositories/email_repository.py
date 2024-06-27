from config.db_config import get_connection
from models.email import Email
import json


class EmailRepository:
    def __init__(self):
        self.conn = get_connection()
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS emails (id TEXT PRIMARY KEY, snippet TEXT, payload TEXT)''')
        self.conn.commit()

    def save(self, email):
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO emails (id, snippet, payload) VALUES (?, ?, ?)''',
                  (email.id, email.snippet, json.dumps(email.payload)))
        self.conn.commit()

    def fetch_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM emails')
        rows = c.fetchall()
        emails = [Email(row[0], row[1], json.loads(row[2])) for row in rows]
        return emails
