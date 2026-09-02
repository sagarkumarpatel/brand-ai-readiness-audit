import http.server
import threading
import urllib.parse
from tests.integration.fixtures import FIXTURES

class TestServerHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Suppress logging to keep test output clean
        pass
        
    def do_HEAD(self):
        self._serve_response(is_head=True)
        
    def do_GET(self):
        self._serve_response(is_head=False)
        
    def do_POST(self):
        # We should test read-only guarantee. The crawler shouldn't send POST.
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
        
        # Exact match
        if path in FIXTURES:
            fixture = FIXTURES[path]
        else:
            # Add trailing slash or remove trailing slash to try and match
            if path.endswith('/') and path[:-1] in FIXTURES:
                fixture = FIXTURES[path[:-1]]
            elif not path.endswith('/') and path + '/' in FIXTURES:
                fixture = FIXTURES[path + '/']
            else:
                self.send_response(404)
                self.end_headers()
                if not is_head:
                    self.wfile.write(b"Not Found")
                return

        self.send_response(fixture.get("status", 200))
        
        headers = fixture.get("headers", {})
        if "content_type" in fixture:
            headers["Content-Type"] = fixture["content_type"]
            
        for k, v in headers.items():
            self.send_header(k, v)
            
        body_bytes = fixture.get("body", "").encode("utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        
        if not is_head and body_bytes:
            self.wfile.write(body_bytes)

class TestServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = http.server.HTTPServer(('127.0.0.1', self.port), TestServerHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        
    def start(self):
        self.thread.start()
        
    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)
