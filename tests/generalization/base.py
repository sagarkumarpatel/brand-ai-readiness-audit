import unittest
import time
import asyncio
import importlib.util
import sys
import json
from tests.generalization.server import GeneralizationServer
from tests.generalization.scorecard import Scorecard
from tests.generalization.expected import ExpectedFindings

# Dynamically import audit-orchestrator.py
spec = importlib.util.spec_from_file_location("audit_orchestrator", "scripts/audit-orchestrator.py")
audit_orchestrator = importlib.util.module_from_spec(spec)
sys.modules["audit_orchestrator"] = audit_orchestrator
spec.loader.exec_module(audit_orchestrator)
run_audit = audit_orchestrator.run_audit

GLOBAL_SCORECARD = Scorecard()

class GeneralizationTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = GeneralizationServer(port=8082)
        cls.server.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        
    def setUp(self):
        self.server.clear_logs()

    async def run_audit_on(self, path):
        url = f"http://127.0.0.1:8082{path}"
        result = await run_audit(url)
        return json.loads(result["json"])

    def evaluate_findings(self, report, expected_findings, forbidden_findings):
        found_ids = {f["id"] for f in report.get("findings", [])}
        
        for exp_id in expected_findings:
            GLOBAL_SCORECARD.add_result(exp_id, exp_id if exp_id in found_ids else None)
            self.assertIn(exp_id, found_ids, f"Expected finding {exp_id} was missing.")
            
        for forb_id in forbidden_findings:
            if forb_id in found_ids:
                GLOBAL_SCORECARD.add_false_positive()
            self.assertNotIn(forb_id, found_ids, f"Forbidden finding {forb_id} was found.")

