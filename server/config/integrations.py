import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from slack_sdk import WebClient
from pushbullet import Pushbullet
import telegram


class IntegrationsConfig:
    @staticmethod
    def setup_google_calendar():
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    @staticmethod
    def setup_slack():
        return WebClient(token=os.getenv("SLACK_TOKEN"))

    @staticmethod
    def setup_pushbullet():
        return Pushbullet(os.getenv("PUSHBULLET_TOKEN"))

    @staticmethod
    def setup_telegram():
        return telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
