import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from config.gmail_config import TOKEN_FILE, CREDENTIALS_FILE, SCOPES


class GoogleAuthenticator:
    def __init__(self):
        self.credentials_file = CREDENTIALS_FILE
        self._load_credentials()

    def _load_credentials(self):
        with open(self.credentials_file) as f:
            self.credentials = json.load(f)

    def authenticate_oauth(self):
        client_id = self.credentials.get("client_id")
        client_secret = self.credentials.get("client_secret")
        redirect_uri = self.credentials.get("redirect_uri")

        auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=" + "+".join(
            SCOPES)

        # Use webdriver_manager to automatically find the Chrome driver path
        chrome_driver_path = ChromeDriverManager().install()

        # Set Chrome options to run in headless mode (without opening the browser window)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Comment this line if you want to see the browser window

        # Factory method to create a configured Chrome WebDriver instance

        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

        try:
            # Open the Google OAuth authorization URL using Selenium WebDriver
            driver.get(auth_url)

            # Example steps to interact with the Google OAuth consent screen using Selenium
            # Replace these with specific interactions based on your OAuth flow

            # Example: Finding and clicking on the 'Next' button
            next_button = WebDriverWait(driver, 10).until(
                expected_conditions.element_to_be_clickable((By.ID, "identifierNext"))
            )
            next_button.click()

            # Example: Finding and filling the password field
            password_field = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys("YOUR_PASSWORD")
            password_field.submit()

            # Example: Waiting for the redirect and extracting the authorization code from the URL
            WebDriverWait(driver, 10).until(
                expected_conditions.url_contains(redirect_uri)
            )
            authorization_code = driver.current_url.split('code=')[1]
            driver.quit()

            # Exchange the authorization code for an access token
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": authorization_code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
            response = requests.post(token_url, data=data)

            # Print the access token
            if response.status_code == 200:
                access_token = response.json()["access_token"]
                print("Access Token:", access_token)
            else:
                print("Failed to get access token:", response.text)

        except Exception as e:
            print("Error:", e)
            driver.quit()

    def _get_gmail_service(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)


# Example usage:
if __name__ == "__main__":
    authenticator = GoogleAuthenticator()
    authenticator.authenticate_oauth()
