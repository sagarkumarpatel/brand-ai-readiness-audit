import sys
import importlib.util
import time
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

spec = importlib.util.spec_from_file_location("audit_orchestrator", "scripts/audit-orchestrator.py")
audit_orchestrator = importlib.util.module_from_spec(spec)
sys.modules["audit_orchestrator"] = audit_orchestrator
spec.loader.exec_module(audit_orchestrator)

class DummySiteHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging to keep output clean

    def do_GET(self):
        self.send_response(200)
        
        if self.path == "/robots.txt":
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"User-agent: *\nAllow: /\n")
            return
            
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        size = 10
        if "tiny" in self.path:
            size = 5
        elif "small" in self.path:
            size = 25
        elif "medium" in self.path:
            size = 100
        
        links = ""
        prefix = self.path.split('/')[1] if len(self.path) > 1 and "page" not in self.path else "medium"
        for i in range(1, size):
            links += f'<a href="/{prefix}/page{i}.html">Page {i}</a><br>'
                
        html = f"""
        <html>
        <head><title>Test Page {self.path}</title></head>
        <body>
            <h1>Welcome to {self.path}</h1>
            <p>This is a test page for performance benchmarking.</p>
            {links}
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

def start_server():
    server = HTTPServer(('127.0.0.1', 8080), DummySiteHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

async def run_benchmark(size_name, max_pages):
    print(f"\n--- Running benchmark for {size_name.upper()} site (up to {max_pages} pages) ---")
    start_time = time.perf_counter()
    report = await audit_orchestrator.run_audit(f"http://127.0.0.1:8080/{size_name}/", max_pages=max_pages)
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    print(f"\nTotal time: {total_time:.2f} seconds")
    if report.get("data"):
        data = report["data"]
        print(f"Total findings: {data.summary.total_findings}")
    else:
        print("Failed to get report data.")

async def main():
    server = start_server()
    time.sleep(1) # wait for server
    
    # Temporarily override max_pages in config if needed, or we just let it use the default (100)
    
    await run_benchmark("tiny", 5)
    await run_benchmark("small", 25)
    await run_benchmark("medium", 100)
    
    server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
