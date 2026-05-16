"""
Run this script once to get your TikTok OAuth access token.
It starts a local server, opens the TikTok auth page, and saves your token.

Usage: python tiktok_auth.py
"""

import os
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "user.info.basic,video.publish,video.upload"

auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorization successful! You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>Authorization failed. Check your app settings.</h2>")

    def log_message(self, format, *args):
        pass  # suppress server logs


def get_access_token(code: str) -> dict:
    resp = requests.post(
        "https://open.tiktokapis.com/v2/oauth/token/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": CLIENT_KEY,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    if not CLIENT_KEY or not CLIENT_SECRET:
        print("ERROR: Set TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET in your .env file first.")
        return

    auth_url = (
        "https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={CLIENT_KEY}"
        f"&scope={SCOPES}"
        f"&response_type=code"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&state=tiktok_auto_poster"
    )

    print("Opening TikTok authorization page...")
    print(f"If it doesn't open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8080), CallbackHandler)
    print("Waiting for authorization (listening on http://localhost:8080)...")
    server.handle_request()

    if not auth_code:
        print("No auth code received.")
        return

    print("Exchanging code for access token...")
    token_data = get_access_token(auth_code)
    access_token = token_data.get("access_token", "")

    if access_token:
        print(f"\nSuccess! Add this to your .env file:\nTIKTOK_ACCESS_TOKEN={access_token}")
        # Append to .env if it exists
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                content = f.read()
            if "TIKTOK_ACCESS_TOKEN=" in content:
                lines = [
                    f"TIKTOK_ACCESS_TOKEN={access_token}" if l.startswith("TIKTOK_ACCESS_TOKEN=") else l
                    for l in content.splitlines()
                ]
                with open(".env", "w") as f:
                    f.write("\n".join(lines))
            else:
                with open(".env", "a") as f:
                    f.write(f"\nTIKTOK_ACCESS_TOKEN={access_token}\n")
            print("Automatically saved to .env!")
    else:
        print(f"Failed to get token: {token_data}")


if __name__ == "__main__":
    main()
