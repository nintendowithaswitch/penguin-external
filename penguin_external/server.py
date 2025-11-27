import json
import threading
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path

_UI_PATH = Path(__file__).parent / "ui.html"

def _load_ui():
    try:
        return _UI_PATH.read_text(encoding='utf-8')
    except Exception:
        return ""

def make_handler(penguin):
    ui_html = _load_ui()

    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/c':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = json.dumps({
                    'enabled': penguin.enabled,
                    'delay': penguin.delay,
                    'key': penguin.key
                }).encode()
                self.wfile.write(data)
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(ui_html.encode())

        def do_POST(self):
            if self.path == '/c':
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                config = json.loads(body)
                with penguin.lock:
                    penguin.enabled = bool(config.get('enabled', False))
                    penguin.delay = max(0.05, float(config.get('delay', 0.68)))
                    # store full key string (no arbitrary truncation)
                    penguin.key = str(config.get('key', 'f')).lower()
                self.send_response(200)
                self.end_headers()

        def log_message(self, *args, **kwargs):
            # suppress default logging
            return

    return Handler


def start_server(port: int, penguin):
    server = TCPServer(('', port), make_handler(penguin))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
