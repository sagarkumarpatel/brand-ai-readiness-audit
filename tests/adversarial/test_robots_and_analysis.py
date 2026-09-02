import unittest
import asyncio
import json
import time

from tests.adversarial.server import AdversarialServer
from scripts.benchmark import audit_orchestrator

class TestAdversarialRobotsAnalysis(unittest.IsolatedAsyncioTestCase):
    
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

    async def test_robots_conflicts(self):
        # The parser/crawler should not crash
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/robots-conflicts/", max_pages=5)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/robots-conflicts/")
        
    async def test_malformed_sitemap(self):
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/malformed-sitemap/", max_pages=1)
        report = json.loads(res["json"])
        self.assertEqual(report["site"], "http://127.0.0.1:8081/malformed-sitemap/")
        
    async def test_engagement_false_positives(self):
        # A legitimate short page (contact page) should NOT flag Thin Content or Dead End
        # We need to make sure the crawler doesn't hallucinate.
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/legit-short/", max_pages=1)
        report = json.loads(res["json"])
        titles = [f["title"] for f in report.get("findings", [])]
        # Should not flag thin content if the page has sufficient utility/type metadata
        self.assertNotIn("Thin Content", titles)
        
    async def test_freshness_future_date(self):
        # It shouldn't crash or report 'Stale Content' if date is in future
        res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/future-date/", max_pages=1)
        report = json.loads(res["json"])
        titles = [f["title"] for f in report.get("findings", [])]
        self.assertNotIn("Stale Content", titles)

if __name__ == '__main__':
    unittest.main()
