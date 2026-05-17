"""
Run this once to authorize your YouTube account.

Usage: python youtube_auth.py

You'll need a client_secrets.json from Google Cloud Console:
  1. Go to https://console.cloud.google.com/
  2. Create a project → Enable "YouTube Data API v3"
  3. Go to APIs & Services → Credentials → Create OAuth 2.0 Client ID
  4. Application type: Desktop app
  5. Download JSON → save as client_secrets.json in this folder
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "youtube_token.json"


def authenticate() -> Credentials:
    if not os.path.exists(SECRETS_FILE):
        print(f"ERROR: {SECRETS_FILE} not found.")
        print("Download it from Google Cloud Console → APIs & Services → Credentials")
        raise FileNotFoundError(SECRETS_FILE)

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8081)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"Credentials saved to {TOKEN_FILE}")

    return creds


if __name__ == "__main__":
    authenticate()
    print("YouTube authorization successful!")
