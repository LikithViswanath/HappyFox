import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from utils.env_vars import TOKEN_FILE, CREDENTIALS_FILE, SCOPES, USER_ID
from utils.logger import Logger

log = Logger(__name__).get_logger()


class GmailAuthenticationService:

    def __init__(self):
        log.info("Initializing Gmail Authentication Service...")
        self.service = self._authenticate_gmail()
        self.user_id = USER_ID

    def _authenticate_gmail(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            log.info("Found existing token file, attempting to use it...")
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
                log.info("Successfully loaded credentials from token file.")
            except Exception as e:
                log.error(f"Error loading credentials from token file: {e}")
                raise e

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                log.info("Refreshing expired credentials...")
                creds.refresh(Request())
                log.info("Credentials refreshed successfully.")
            else:
                log.info("No valid credentials found, initiating user authorization flow...")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
                log.info("User authorization complete, saving credentials...")
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        self.auth_headers = {
            "Authorization": f"Bearer {creds.token}",
        }
        log.info("Authentication successful, Gmail service built.")
        return build('gmail', 'v1', credentials=creds)
