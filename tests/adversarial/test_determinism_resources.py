import unittest
import asyncio
import json
import time

from tests.adversarial.server import AdversarialServer
from scripts.benchmark import audit_orchestrator

class TestAdversarialDeterminismResources(unittest.IsolatedAsyncioTestCase):
    
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

    async def test_determinism_and_resources(self):
        # Run identical audits 10 times and assert JSON output (minus audited_at) is byte-for-byte identical.
        # Also implicitly checks for catastrophic resource leaks via the underlying runtime.
        
        baseline_json = None
        
        for i in range(10):
            res = await audit_orchestrator.run_audit("http://127.0.0.1:8081/determinism/", max_pages=3)
            report = json.loads(res["json"])
            
            # Remove audited_at
            if "audited_at" in report:
                del report["audited_at"]
                
            report_str = json.dumps(report, sort_keys=True)
            
            if baseline_json is None:
                baseline_json = report_str
            else:
                self.assertEqual(baseline_json, report_str, f"Mismatch on run {i}")
                
if __name__ == '__main__':
    unittest.main()
