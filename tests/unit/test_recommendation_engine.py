import unittest
from src.findings.models import NormalizedFinding, SuggestedAction
from src.recommendations.engine import RecommendationEngine

class TestRecommendationEngine(unittest.TestCase):
    def create_finding(self, title="Test", severity="HIGH", confidence="HIGH", evidence=["ev"]):
        return NormalizedFinding(
            id="123",
            title=title,
            severity=severity,
            confidence=confidence,
            evidence=evidence,
            suggested_action=SuggestedAction(summary="", priority=""),
            affected_urls=[],
            why_it_matters="",
            source_engines=[]
        )

    def test_missing_canonical(self):
        finding = self.create_finding(title="Missing Canonical")
        rec = RecommendationEngine.generate(finding)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.finding_id, "123")
        self.assertIn("Add a self-referencing canonical URL", rec.suggested_action["summary"])

    def test_missing_structured_data(self):
        finding = self.create_finding(title="Missing Structured Data")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("JSON-LD", rec.suggested_action["summary"])

    def test_render_locked_content(self):
        finding = self.create_finding(title="Render-locked Content")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("server-side rendering (SSR)", rec.suggested_action["summary"])

    def test_sitemap_crawl_barrier(self):
        finding = self.create_finding(title="Sitemap/Crawl Barrier")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("robots.txt", rec.suggested_action["summary"])

    def test_conflicting_contact_information(self):
        finding = self.create_finding(title="Conflicting Contact Information")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("authoritative business phone number", rec.suggested_action["summary"])

    def test_stale_content(self):
        finding = self.create_finding(title="Stale Content")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("current year", rec.suggested_action["summary"])

    def test_thin_content(self):
        finding = self.create_finding(title="Thin Content")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("sufficient, well-structured original content", rec.suggested_action["summary"])

    def test_dead_end_page(self):
        finding = self.create_finding(title="Dead-End Page")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("internal next-step link", rec.suggested_action["summary"])

    def test_wall_of_text(self):
        finding = self.create_finding(title="Wall of Text")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("semantic HTML headings", rec.suggested_action["summary"])

    def test_unknown_finding_fallback(self):
        finding = self.create_finding(title="Some Unknown Weird Issue")
        rec = RecommendationEngine.generate(finding)
        self.assertIn("Review the specific evidence", rec.suggested_action["summary"])
        self.assertNotIn("Improve SEO", rec.suggested_action["summary"]) # Should not have generic bad advice

    def test_priority_mapping(self):
        finding1 = self.create_finding(severity="CRITICAL", confidence="HIGH")
        rec1 = RecommendationEngine.generate(finding1)
        self.assertEqual(rec1.suggested_action["priority"], "P0")

        finding2 = self.create_finding(severity="CRITICAL", confidence="LOW")
        rec2 = RecommendationEngine.generate(finding2)
        self.assertEqual(rec2.suggested_action["priority"], "P1") # Downgraded

        finding3 = self.create_finding(severity="HIGH", confidence="LOW")
        rec3 = RecommendationEngine.generate(finding3)
        self.assertEqual(rec3.suggested_action["priority"], "P2") # Downgraded

        finding4 = self.create_finding(severity="INVALID_SEVERITY", confidence="HIGH")
        rec4 = RecommendationEngine.generate(finding4)
        self.assertEqual(rec4.suggested_action["priority"], "P2") # Defaults to MEDIUM -> P2

    def test_missing_evidence_rejected(self):
        finding = self.create_finding(evidence=[])
        rec = RecommendationEngine.generate(finding)
        self.assertIsNone(rec)

    def test_none_finding_rejected(self):
        rec = RecommendationEngine.generate(None)
        self.assertIsNone(rec)

if __name__ == '__main__':
    unittest.main()
