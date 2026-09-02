import http.server
import threading
import urllib.parse
import time
from tests.adversarial.fixtures import ADVERSARIAL_FIXTURES

class AdversarialServerHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Suppress logging to keep test output clean
        pass
        
    def do_HEAD(self):
        self.server.request_log.append({"method": "HEAD", "path": self.path})
        self._serve_response(is_head=True)
        
    def do_GET(self):
        self.server.request_log.append({"method": "GET", "path": self.path})
        self._serve_response(is_head=False)
        
    def do_POST(self):
        self.server.request_log.append({"method": "POST", "path": self.path})
        self.send_error(405, "Method Not Allowed")
        
    def do_PUT(self):
        self.server.request_log.append({"method": "PUT", "path": self.path})
        self.send_error(405, "Method Not Allowed")
        
    def do_PATCH(self):
        self.server.request_log.append({"method": "PATCH", "path": self.path})
        self.send_error(405, "Method Not Allowed")
        
    def do_DELETE(self):
        self.server.request_log.append({"method": "DELETE", "path": self.path})
        self.send_error(405, "Method Not Allowed")
        
    def _serve_response(self, is_head):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Add a flag to simulate timeout or dropped connection from URL query
        qs = urllib.parse.parse_qs(parsed_path.query)
        
        fixture = None
        if path in ADVERSARIAL_FIXTURES:
            fixture = ADVERSARIAL_FIXTURES[path]
        else:
            if path.endswith('/') and path[:-1] in ADVERSARIAL_FIXTURES:
                fixture = ADVERSARIAL_FIXTURES[path[:-1]]
            elif not path.endswith('/') and path + '/' in ADVERSARIAL_FIXTURES:
                fixture = ADVERSARIAL_FIXTURES[path + '/']

        if fixture is None:
            # Check if there is a wildcard rule like `/wildcard/*`
            for k in ADVERSARIAL_FIXTURES:
                if k.endswith('*') and path.startswith(k[:-1]):
                    fixture = ADVERSARIAL_FIXTURES[k]
                    break

        if fixture is None:
            self.send_response(404)
            self.end_headers()
            if not is_head:
                self.wfile.write(b"Not Found")
            return
            
        # Adversarial behaviors
        if fixture.get("drop_connection"):
            # Simply return and let socket close without HTTP headers
            return
            
        if "delay" in fixture:
            time.sleep(fixture["delay"])
            
        status = fixture.get("status", 200)
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
            
        # For incomplete response attack
        if fixture.get("incomplete_response"):
            self.send_header("Content-Length", str(len(body_bytes) + 100)) # Lie about length
            self.end_headers()
            if not is_head and body_bytes:
                # write half
                self.wfile.write(body_bytes[:len(body_bytes)//2])
            return

        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        
        if not is_head and body_bytes:
            self.wfile.write(body_bytes)

class AdversarialServer:
    def __init__(self, port=8081):
        self.port = port
        self.server = http.server.HTTPServer(('127.0.0.1', self.port), AdversarialServerHandler)
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
