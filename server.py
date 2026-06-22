#!/usr/bin/env python3
"""
Steel Bar Takeoff - local server + API relay.

Run:  python server.py
Then open the browser at the URL it prints (http://localhost:8765).

This server does two jobs:
  1. Serves steel-bar-takeoff.html over http://localhost (a real origin,
     so the browser doesn't block anything).
  2. Relays the extraction request to the Claude API *server-side*, which
     sidesteps the browser CORS / sandbox restrictions that cause
     "Failed to fetch". Your API key is read from the request and forwarded
     straight to Anthropic - it is never stored or logged.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(HERE, "steel-bar-takeoff.html")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # quieter console - only show our own prints
        pass

    def _send(self, code, body, content_type="application/json"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html", "/steel-bar-takeoff.html"):
            if not os.path.exists(HTML_FILE):
                self._send(404, "steel-bar-takeoff.html not found next to server.py", "text/plain")
                return
            with open(HTML_FILE, "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/extract":
            self._send(404, json.dumps({"error": {"message": "Unknown endpoint"}}))
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        api_key = self.headers.get("x-api-key", "").strip()

        if not api_key:
            self._send(400, json.dumps({"error": {"message": "Missing API key"}}))
            return

        req = urllib.request.Request(
            ANTHROPIC_URL,
            data=raw,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )

        try:
            print("  -> relaying request to Claude API...")
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = resp.read()
                print("  <- got response from Claude")
                self._send(resp.status, body)
        except urllib.error.HTTPError as e:
            body = e.read()
            print(f"  !! API returned error {e.code}")
            self._send(e.code, body)
        except urllib.error.URLError as e:
            msg = f"Could not reach Claude API: {e.reason}. Check your internet connection / firewall."
            print(f"  !! {msg}")
            self._send(502, json.dumps({"error": {"message": msg}}))
        except Exception as e:
            self._send(500, json.dumps({"error": {"message": str(e)}}))


def main():
    if not os.path.exists(HTML_FILE):
        print(f"ERROR: cannot find {HTML_FILE}")
        print("Make sure server.py sits in the same folder as steel-bar-takeoff.html")
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("=" * 56)
    print("  Steel Bar Takeoff is running")
    print(f"  Open your browser at:  {url}")
    print("  Press Ctrl+C here to stop.")
    print("=" * 56)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
