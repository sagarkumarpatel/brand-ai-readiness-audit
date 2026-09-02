import http.server
import threading
import urllib.parse
from tests.generalization.fixtures import GENERALIZATION_FIXTURES

class GeneralizationServerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_HEAD(self):
        self.server.request_log.append({"method": "HEAD", "path": self.path})
        self._serve_response(is_head=True)

    def do_GET(self):
        self.server.request_log.append({"method": "GET", "path": self.path})
        self._serve_response(is_head=False)

    def do_POST(self):
        self.send_error(405, "Method Not Allowed")

    def do_PUT(self):
        self.send_error(405, "Method Not Allowed")

    def do_PATCH(self):
        self.send_error(405, "Method Not Allowed")

    def do_DELETE(self):
        self.send_error(405, "Method Not Allowed")

    def _serve_response(self, is_head):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        fixture = None
        if path in GENERALIZATION_FIXTURES:
            fixture = GENERALIZATION_FIXTURES[path]
        else:
            if path.endswith("/") and path[:-1] in GENERALIZATION_FIXTURES:
                fixture = GENERALIZATION_FIXTURES[path[:-1]]
            elif not path.endswith("/") and path + "/" in GENERALIZATION_FIXTURES:
                fixture = GENERALIZATION_FIXTURES[path + "/"]

        if fixture is None:
            for k in GENERALIZATION_FIXTURES:
                if k.endswith("*") and path.startswith(k[:-1]):
                    fixture = GENERALIZATION_FIXTURES[k]
                    break

        if fixture is None:
            self.send_response(404)
            self.end_headers()
            if not is_head:
                self.wfile.write(b"Not Found")
            return

        status = fixture.get("status", 200)
        
        # Check if the fixture itself is a redirect logic
        if status in (301, 302, 303, 307, 308):
            self.send_response(status)
            if "location" in fixture:
                self.send_header("Location", fixture["location"])
            self.end_headers()
            return
            
        self.send_response(status)

        headers = fixture.get("headers", {})
        if "content_type" in fixture:
            headers["Content-Type"] = fixture["content_type"]

        for k, v in headers.items():
            self.send_header(k, v)

        if "body" in fixture:
            body_bytes = fixture["body"].encode("utf-8")
        elif "body_bytes" in fixture:
            body_bytes = fixture["body_bytes"]
        else:
            body_bytes = b""

        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()

        if not is_head and body_bytes:
            self.wfile.write(body_bytes)

class GeneralizationServer:
    def __init__(self, port=8082):
        self.port = port
        self.server = http.server.HTTPServer(("127.0.0.1", self.port), GeneralizationServerHandler)
        self.server.request_log = []
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def get_logs(self):
        return self.server.request_log

    def clear_logs(self):
        self.server.request_log = []

