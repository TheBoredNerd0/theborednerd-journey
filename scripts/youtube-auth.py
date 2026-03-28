#!/usr/bin/env python3
"""
YouTube OAuth Setup for Mac — run ONCE to authorize.
After this, you can upload videos automatically.

Usage: python3 youtube-auth.py
"""
import json, os, http.server, socketserver, threading, webbrowser, sys, urllib.request, urllib.parse
from urllib.parse import parse_qs, urlparse

# Load credentials from ~/.openclaw/credentials/youtube-oauth.json
CRED_FILE = os.path.expanduser("~/.openclaw/credentials/youtube-oauth.json")
TOKEN_FILE = os.path.expanduser("~/.openclaw/credentials/youtube-token.json")
os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

with open(CRED_FILE) as f:
    creds = json.load(f)
CLIENT_ID = creds["client_id"]
CLIENT_SECRET = creds["client_secret"]
REDIRECT_URI = creds["redirect_uris"][0]

auth_url = (
    "https://accounts.google.com/o/oauth2/v2/auth"
    f"?access_type=offline&scope=https://www.googleapis.com/auth/youtube.upload"
    f"%20https://www.googleapis.com/auth/youtube&prompt=consent"
    f"&response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
)

print("=" * 55)
print("  🎬 YouTube OAuth Setup")
print("=" * 55)
print()
print("🌐 Opening browser for Google authorization...")
print("   (If browser doesn't open, copy the URL printed below)")
print()

received_code = {"code": None}
done = threading.Event()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "code" in params:
            received_code["code"] = params["code"][0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body style='font-family:sans-serif;padding:40px;text-align:center'><h1 style='color:#1a1a1a'>OK!</h1><p>You can close this window.</p></body></html>")
        done.set()
    def log_message(self, *args): pass

PORT = 3000
print(f"URL: {auth_url}\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    t = threading.Thread(target=lambda: webbrowser.open(auth_url))
    t.start()
    httpd.handle_request()

code = received_code.get("code")
if not code:
    print("❌ No code received. Make sure you clicked 'Allow' in the browser.")
    sys.exit(1)

print("✅ Got code! Saving token...")

data = urllib.parse.urlencode({
    "code": code, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI, "grant_type": "authorization_code"
}).encode()

with urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=15) as resp:
    token_data = json.loads(resp.read())
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)

print(f"✅ Saved → {TOKEN_FILE}")
print()
print("🎉 OAuth complete! You can now upload YouTube videos.")
