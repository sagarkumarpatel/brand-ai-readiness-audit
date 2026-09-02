import unittest
from unittest.mock import patch
import asyncio
import importlib.util
import sys
from datetime import datetime, timezone

from src.crawler.models import CrawlResponse
from src.analysis.models import Issue, AuditReport

# Dynamically import the script since it has a dash in its name
spec = importlib.util.spec_from_file_location("audit_orchestrator", "scripts/audit-orchestrator.py")
audit_orchestrator = importlib.util.module_from_spec(spec)
sys.modules["audit_orchestrator"] = audit_orchestrator
spec.loader.exec_module(audit_orchestrator)
run_audit = audit_orchestrator.run_audit

class TestSkillOrchestrator(unittest.IsolatedAsyncioTestCase):
    
    @patch('audit_orchestrator.SafeCrawler.crawl')
    @patch('audit_orchestrator.SiteDiscoverabilityEngine.analyze')
    @patch('audit_orchestrator.FreshnessCorroborationEngine.analyze')
    @patch('audit_orchestrator.EngagementAnalyzer.analyze')
    async def test_clean_website(self, mock_eng, mock_fresh, mock_disc, mock_crawl):
        # Setup mocks
        mock_crawl.return_value = []
        mock_disc.return_value = AuditReport()
        mock_fresh.return_value = []
        mock_eng.return_value = []
        
        report = await run_audit("http://example.com")
        
        self.assertEqual(report["site"], "http://example.com")
        self.assertEqual(report["summary"]["total_findings"], 0)
        self.assertEqual(report["summary"]["critical"], 0)
        self.assertEqual(len(report["findings"]), 0)
        self.assertIn("audited_at", report)

    @patch('audit_orchestrator.SafeCrawler.crawl')
    @patch('audit_orchestrator.SiteDiscoverabilityEngine.analyze')
    @patch('audit_orchestrator.FreshnessCorroborationEngine.analyze')
    @patch('audit_orchestrator.EngagementAnalyzer.analyze')
    async def test_multiple_issues_across_engines(self, mock_eng, mock_fresh, mock_disc, mock_crawl):
        mock_crawl.return_value = []
        
        # Discoverability finds Missing Canonical
        disc_report = AuditReport()
        disc_report.add_issue(Issue("Missing Canonical", "HIGH", "HIGH", ["ev1"], "why", "act"))
        mock_disc.return_value = disc_report
        # Freshness finds Stale Content
        mock_fresh.return_value = [
            Issue("Stale Content", "MEDIUM", "HIGH", ["ev2"], "why", "act")
        ]
        # Engagement finds Dead-End Page
        mock_eng.return_value = [
            Issue("Dead-End Page", "LOW", "HIGH", ["ev3"], "why", "act")
        ]
        
        report = await run_audit("http://example.com")
        
        self.assertEqual(report["summary"]["total_findings"], 3)
        self.assertEqual(report["summary"]["high"], 1)
        self.assertEqual(report["summary"]["medium"], 1)
        self.assertEqual(report["summary"]["low"], 1)
        
        titles = [f["title"] for f in report["findings"]]
        self.assertIn("Missing Canonical", titles)
        self.assertIn("Stale Content", titles)
        self.assertIn("Dead-End Page", titles)

    @patch('audit_orchestrator.SafeCrawler.crawl')
    @patch('audit_orchestrator.SiteDiscoverabilityEngine.analyze')
    @patch('audit_orchestrator.FreshnessCorroborationEngine.analyze')
    @patch('audit_orchestrator.EngagementAnalyzer.analyze')
    async def test_duplicate_cross_engine_findings_deduplicated(self, mock_eng, mock_fresh, mock_disc, mock_crawl):
        mock_crawl.return_value = []
        
        disc_report2 = AuditReport()
        disc_report2.add_issue(Issue("Render-locked Content", "CRITICAL", "HIGH", ["ev1"], "why", "act"))
        mock_disc.return_value = disc_report2
        # Simulate another engine also flagging the exact same issue
        mock_fresh.return_value = [
            Issue("Render-locked Content", "CRITICAL", "HIGH", ["ev2"], "why", "act")
        ]
        mock_eng.return_value = []
        
        report = await run_audit("http://example.com")
        
        self.assertEqual(report["summary"]["total_findings"], 1)
        self.assertEqual(report["summary"]["critical"], 1)
        
        finding = report["findings"][0]
        self.assertEqual(finding["title"], "Render-locked Content")
        # Evidence should be merged
        self.assertEqual(len(finding["evidence"]), 2)
        
        # Recommendation attached
        self.assertIn("server-side rendering", finding["suggested_action"]["summary"])
        
    @patch('audit_orchestrator.SafeCrawler.crawl')
    async def test_crawl_failure_safe_handling(self, mock_crawl):
        mock_crawl.side_effect = Exception("Network timeout")
        
        report = await run_audit("http://example.com")
        
        # Should fail safely with error message, not crash
        self.assertEqual(report["summary"]["total_findings"], 0)
        self.assertIn("error", report)
        self.assertIn("Network timeout", report["error"])

if __name__ == '__main__':
    unittest.main()
