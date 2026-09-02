import unittest
from src.analysis.models import Issue
from src.findings.composer import FindingComposer

class TestFindingsComposer(unittest.TestCase):
    def test_single_valid_finding_preserved(self):
        issue = Issue(
            title="Missing Canonical",
            severity="HIGH",
            confidence="HIGH",
            evidence=["Missing on /about"],
            why="Because SEO",
            action="Add canonical"
        )
        findings = FindingComposer.compose([issue])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].title, "Missing Canonical")
        self.assertEqual(findings[0].severity, "HIGH")

    def test_duplicate_findings_merged(self):
        issue1 = Issue(
            title="Missing Canonical",
            severity="HIGH",
            confidence="HIGH",
            evidence=["Missing on /about"],
            why="Because SEO",
            action="Add canonical"
        )
        issue2 = Issue(
            title="Missing Canonical",  # Exact same title
            severity="HIGH",
            confidence="HIGH",
            evidence=["Missing on /contact"], # Different evidence
            why="Because SEO",
            action="Add canonical"
        )
        findings = FindingComposer.compose([issue1, issue2])
        self.assertEqual(len(findings), 1)
        # Evidence should be merged and deduplicated/sorted
        self.assertEqual(len(findings[0].evidence), 2)
        self.assertIn("Missing on /about", findings[0].evidence)
        self.assertIn("Missing on /contact", findings[0].evidence)

    def test_distinct_findings_preserved(self):
        issue1 = Issue(
            title="Missing Canonical",
            severity="HIGH",
            confidence="HIGH",
            evidence=["Missing on /about"],
            why="Because SEO",
            action="Add canonical"
        )
        issue2 = Issue(
            title="Missing Structured Data",
            severity="MEDIUM",
            confidence="HIGH",
            evidence=["Missing on /about"],
            why="Because AI",
            action="Add json-ld"
        )
        findings = FindingComposer.compose([issue1, issue2])
        self.assertEqual(len(findings), 2)

    def test_missing_evidence_rejected(self):
        issue = Issue(
            title="Missing Canonical",
            severity="HIGH",
            confidence="HIGH",
            evidence=[], # Empty evidence
            why="Because SEO",
            action="Add canonical"
        )
        findings = FindingComposer.compose([issue])
        self.assertEqual(len(findings), 0)

    def test_invalid_severity_normalized(self):
        issue = Issue(
            title="Missing Canonical",
            severity="SUPER_BAD", # Invalid
            confidence="HIGH",
            evidence=["Missing on /about"],
            why="Because SEO",
            action="Add canonical"
        )
        findings = FindingComposer.compose([issue])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "MEDIUM")
        self.assertEqual(findings[0].suggested_action.priority, "P2")

    def test_deterministic_ordering(self):
        issue1 = Issue(
            title="Zebra Problem",
            severity="LOW",
            confidence="HIGH",
            evidence=["Evidence"],
            why="Why",
            action="Action"
        )
        issue2 = Issue(
            title="Apple Problem",
            severity="CRITICAL",
            confidence="HIGH",
            evidence=["Evidence"],
            why="Why",
            action="Action"
        )
        issue3 = Issue(
            title="Banana Problem",
            severity="CRITICAL",
            confidence="HIGH",
            evidence=["Evidence"],
            why="Why",
            action="Action"
        )
        
        # Order should be Apple (CRITICAL), Banana (CRITICAL), Zebra (LOW)
        findings = FindingComposer.compose([issue1, issue3, issue2])
        self.assertEqual(len(findings), 3)
        self.assertEqual(findings[0].title, "Apple Problem")
        self.assertEqual(findings[1].title, "Banana Problem")
        self.assertEqual(findings[2].title, "Zebra Problem")

if __name__ == '__main__':
    unittest.main()
