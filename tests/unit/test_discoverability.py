import unittest
from src.analysis.models import Issue, AuditReport
from src.analysis.discoverability import SiteDiscoverabilityEngine
from src.crawler.models import CrawlResponse
from src.parser.models import ParsedPage
from src.renderer.models import ComparisonResult

class TestDiscoverabilityEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SiteDiscoverabilityEngine()

    def test_clean_site(self):
        resp = CrawlResponse("http://example.com/1", 200, {}, "text/html", "", [], 0, None, 50.0)
        parsed = ParsedPage("http://example.com/1", "http://example.com/1", 200, "text/html")
        parsed.canonical_url = "http://example.com/1"
        comp = ComparisonResult()
        
        report = self.engine.analyze([resp], {"http://example.com/1": parsed}, {"http://example.com/1": comp}, ["http://example.com/1"])
        self.assertEqual(len(report.issues), 0)

    def test_unreachable_sitemap_page(self):
        resp = CrawlResponse("http://example.com/dead", 404, {}, "text/html", "", [], 0, None, 50.0)
        report = self.engine.analyze([resp], {}, {}, ["http://example.com/dead"])
        
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].title, "Unreachable Important Page")
        self.assertEqual(report.issues[0].severity, "HIGH")

    def test_robots_blocked_sitemap_page(self):
        resp = CrawlResponse("http://example.com/blocked", 0, {}, "", "", [], 0, None, 50.0, error="Blocked by robots.txt")
        report = self.engine.analyze([resp], {}, {}, ["http://example.com/blocked"])
        
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].title, "Sitemap Page Blocked by Robots.txt")
        self.assertEqual(report.issues[0].severity, "CRITICAL")
        
    def test_render_locked_content(self):
        comp = ComparisonResult(js_dependent_content=True, differences=["Significant text added"])
        parsed = ParsedPage("http://example.com/1", "http://example.com/1", 200, "text/html")
        parsed.canonical_url = "http://example.com/1"
        
        report = self.engine.analyze([], {"http://example.com/1": parsed}, {"http://example.com/1": comp})
        
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].title, "Render-locked Content")
        
    def test_missing_structured_data(self):
        parsed = ParsedPage("http://example.com/product/1", "http://example.com/product/1", 200, "text/html")
        parsed.canonical_url = "http://example.com/product/1"
        # No json_ld_blocks
        report = self.engine.analyze([], {"http://example.com/product/1": parsed}, {})
        
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].title, "Missing Structured Data")

if __name__ == '__main__':
    unittest.main()
