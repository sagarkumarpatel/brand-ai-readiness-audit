import unittest
import asyncio
import json
import time

from tests.adversarial.server import AdversarialServer
from scripts.benchmark import audit_orchestrator

class TestAdversarialCrawlerNetwork(unittest.IsolatedAsyncioTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.server = AdversarialServer(port=8081)
        cls.server.start()
        time.sleep(0.5)
        
    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        
    def setUp(self):
        self.server.clear_logs()

    async def test_malformed_html_unicode(self):
        # 1. Unicode / Emoji HTML
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/unicode-emoji/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/unicode-emoji/")
        
        # 2. Malformed HTML (massive strings, missing tags)
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/malformed-html/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/malformed-html/")
        
    async def test_crawler_cyclic_links(self):
        # The crawler should terminate and respect max_pages
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/cyclic/1", max_pages=10)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/cyclic/1")
        # Should not crash

    async def test_excessive_redirect_chain(self):
        # It shouldn't crash, and should report the finding.
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/redirect-chain/1", max_pages=5)
        report = json.loads(res["json"])
        titles = [f["title"] for f in report.get("findings", [])]
        self.assertIn("Excessive Redirect Chain", titles)

    async def test_redirect_loop(self):
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/redirect-loop/1", max_pages=5)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/redirect-loop/1")

    async def test_network_hang(self):
        # Should timeout and continue, returning empty/error but not hang forever
        # Default orchestrator timeout might be high, so we just run it and ensure it finishes.
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/hang/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/hang/")

    async def test_network_drop(self):
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/drop/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/drop/")

    async def test_network_incomplete(self):
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/incomplete/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/incomplete/")

    async def test_network_500(self):
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/error-500/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/error-500/")
        
    async def test_readonly_methods(self):
        await audit_orchestrator.run_audit("http://127.0.0.1:8081/legit-short/", max_pages=1)
        logs = self.server.get_logs()
        for req in logs:
            self.assertIn(req["method"], ["GET", "HEAD"])
            
if __name__ == '__main__':
    unittest.main()
