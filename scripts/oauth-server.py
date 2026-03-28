#!/usr/bin/env python3
"""Simple OAuth redirect catcher for YouTube auth."""
import http.server, socketserver, urllib.parse, sys
from pathlib import Path

PORT = 3000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get('code', [None])[0]
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        if code:
            msg = f'<html><body style="font-family:sans-serif;padding:40px;text-align:center;background:#1a1a1a;color:white"><h1 style="color:#4ade80">✅ Success!</h1><p style="color:#ccc">Code received! Check the terminal.</p><p style="font-family:monospace;font-size:12px;word-break:break-all;background:#333;padding:10px;border-radius:8px;color:#fff">{code[:30]}...</p></body></html>'
            print(f'AUTH_CODE:{code}', flush=True)
        else:
            msg = '<html><body style="font-family:sans-serif;padding:40px;background:#1a1a1a;color:white"><h1 style="color:#4ade80">OK!</h1><p style="color:#ccc">You can close this window.</p></body></html>'
        
        self.wfile.write(msg.encode())
        
    def log_message(self, *args): pass

print(f'Starting server on port {PORT}...', flush=True)
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    httpd.handle_request()
    httpd.handle_request()
