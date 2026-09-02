import unittest
from datetime import datetime, timezone
import json
from src.reporting.generator import ReportGenerator
from src.reporting.serializer import ReportSerializer

class TestReportingLayer(unittest.TestCase):
    def test_valid_report_generation(self):
        raw_findings = [
            {
                "id": "1",
                "title": "Title 1",
                "severity": "HIGH",
                "evidence": ["ev1"],
                "suggested_action": {"summary": "act", "priority": "CRITICAL"}
            }
        ]
        
        report = ReportGenerator.build_report("http://example.com", raw_findings)
        
        self.assertEqual(report.site, "http://example.com")
        self.assertEqual(report.summary.total_findings, 1)
        self.assertEqual(report.summary.high, 1)
        self.assertEqual(report.summary.critical, 0)
        self.assertEqual(report.findings[0].id, "1")
        
    def test_empty_report(self):
        report = ReportGenerator.build_report("http://example.com", [])
        
        self.assertEqual(report.summary.total_findings, 0)
        self.assertEqual(report.summary.critical, 0)
        self.assertEqual(report.summary.high, 0)
        self.assertEqual(report.summary.medium, 0)
        self.assertEqual(report.summary.low, 0)
        self.assertEqual(len(report.findings), 0)
        
    def test_severity_counts(self):
        raw_findings = [
            {"id": "1", "title": "t", "severity": "HIGH", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
            {"id": "2", "title": "t", "severity": "MEDIUM", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
            {"id": "3", "title": "t", "severity": "MEDIUM", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
            {"id": "4", "title": "t", "severity": "LOW", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
        ]
        
        report = ReportGenerator.build_report("http://example.com", raw_findings)
        
        self.assertEqual(report.summary.total_findings, 4)
        self.assertEqual(report.summary.critical, 0)
        self.assertEqual(report.summary.high, 1)
        self.assertEqual(report.summary.medium, 2)
        self.assertEqual(report.summary.low, 1)
        
    def test_deterministic_ordering(self):
        # Should sort by Severity -> Priority -> ID
        raw_findings = [
            {"id": "3", "title": "t", "severity": "LOW", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
            {"id": "1", "title": "t", "severity": "HIGH", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
            {"id": "4", "title": "t", "severity": "HIGH", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "CRITICAL"}},
            {"id": "2", "title": "t", "severity": "HIGH", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}},
        ]
        
        report = ReportGenerator.build_report("http://example.com", raw_findings)
        
        # Order should be: id4 (High/Crit), id1 (High/Low), id2 (High/Low), id3 (Low/Low)
        self.assertEqual(report.findings[0].id, "4")
        self.assertEqual(report.findings[1].id, "1")
        self.assertEqual(report.findings[2].id, "2")
        self.assertEqual(report.findings[3].id, "3")

    def test_invalid_severity(self):
        raw_findings = [{"id": "1", "title": "t", "severity": "INVALID", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}}]
        with self.assertRaises(ValueError):
            ReportGenerator.build_report("http://example.com", raw_findings)
            
    def test_missing_evidence(self):
        raw_findings = [{"id": "1", "title": "t", "severity": "HIGH", "evidence": [], "suggested_action": {"summary": "act", "priority": "LOW"}}]
        with self.assertRaises(ValueError):
            ReportGenerator.build_report("http://example.com", raw_findings)
            
    def test_json_serialization(self):
        raw_findings = [{"id": "1", "title": "t", "severity": "HIGH", "evidence": ["ev"], "suggested_action": {"summary": "act", "priority": "LOW"}}]
        report = ReportGenerator.build_report("http://example.com", raw_findings)
        
        json_str = ReportSerializer.to_json(report)
        data = json.loads(json_str)
        
        self.assertEqual(data["site"], "http://example.com")
        self.assertEqual(data["summary"]["total_findings"], 1)
        self.assertEqual(data["findings"][0]["id"], "1")
        self.assertEqual(data["findings"][0]["severity"], "HIGH")

    def test_markdown_serialization(self):
        raw_findings = [{"id": "1", "title": "Test Title", "severity": "HIGH", "evidence": ["Test evidence"], "why": "Because", "suggested_action": {"summary": "Do this", "priority": "LOW"}}]
        report = ReportGenerator.build_report("http://example.com", raw_findings)
        
        md_str = ReportSerializer.to_markdown(report)
        
        self.assertIn("# AI Website Readiness Audit", md_str)
        self.assertIn("## Site", md_str)
        self.assertIn("http://example.com", md_str)
        self.assertIn("| Total | 1 |", md_str)
        self.assertIn("### 1. Test Title", md_str)
        self.assertIn("**Severity:** HIGH", md_str)
        self.assertIn("- Test evidence", md_str)
        self.assertIn("**Why it matters:**\nBecause", md_str)
        self.assertIn("**Suggested action:**\nDo this", md_str)
        self.assertIn("**Priority:** LOW", md_str)

if __name__ == '__main__':
    unittest.main()
