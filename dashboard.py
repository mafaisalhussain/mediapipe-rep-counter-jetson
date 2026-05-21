import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from config import PLAYER_FILE, SESSION_DIR, DASHBOARD_PORT, BASE_DIR
from session_log import load_recent_sessions

TEMPLATE_PATH = os.path.join(BASE_DIR, "dashboard.html")

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # load player
            if os.path.exists(PLAYER_FILE):
                with open(PLAYER_FILE) as f:
                    player = json.load(f)
            else:
                player = {}

            sessions = load_recent_sessions(10)

            with open(TEMPLATE_PATH) as f:
                html = f.read()

            # inject data
            html = html.replace("__PLAYER_DATA__",  json.dumps(player))
            html = html.replace("__SESSION_DATA__", json.dumps(sessions))

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())

    def log_message(self, *_):
        pass  # silence request logs in terminal

def start_dashboard():
    server = HTTPServer(("localhost", DASHBOARD_PORT), _Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print(f"  Dashboard running → http://localhost:{DASHBOARD_PORT}")
