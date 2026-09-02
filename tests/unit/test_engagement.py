import unittest
from src.parser.models import ParsedPage, Link, Heading
from src.engagement.engine import EngagementAnalyzer

class TestEngagementAnalyzer(unittest.TestCase):
    def test_valid_page_no_finding(self):
        page = ParsedPage(
            url="http://example.com/", 
            final_url="http://example.com/", 
            status_code=200, 
            content_type="text/html",
            visible_text="This is a perfectly normal page with enough content to pass the fifteen word count threshold successfully.",
            links=[Link("http://example.com/about", "About", True)]
        )
        issues = EngagementAnalyzer.analyze({page.url: page})
        self.assertEqual(len(issues), 0)

    def test_thin_content(self):
        page = ParsedPage(
            url="http://example.com/", 
            final_url="http://example.com/", 
            status_code=200, 
            content_type="text/html",
            visible_text="Too short",
            links=[]
        )
        issues = EngagementAnalyzer.analyze({page.url: page})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].title, "Thin Content")

    def test_dead_end_page(self):
        page1 = ParsedPage(
            url="http://example.com/", 
            final_url="http://example.com/", 
            status_code=200, 
            content_type="text/html",
            visible_text="This is the root page with enough content to pass the fifteen word count threshold easily.",
            links=[]
        )
        # Deep page with 0 internal links = Dead end
        page2 = ParsedPage(
            url="http://example.com/deep", 
            final_url="http://example.com/deep", 
            status_code=200, 
            content_type="text/html",
            visible_text="This is a deep page with enough content to pass the thin content threshold but it has absolutely no internal links.",
            links=[]
        )
        issues = EngagementAnalyzer.analyze({page1.url: page1, page2.url: page2})
        dead_ends = [i for i in issues if i.title == "Dead End Page"]
        self.assertEqual(len(dead_ends), 1)

    def test_wall_of_text(self):
        page = ParsedPage(
            url="http://example.com/", 
            final_url="http://example.com/", 
            status_code=200, 
            content_type="text/html",
            visible_text="word " * 3001,
            headings=[]
        )
        issues = EngagementAnalyzer.analyze({page.url: page})
        wall = [i for i in issues if i.title == "Unstructured Wall of Text"]
        self.assertEqual(len(wall), 1)

    def test_well_structured_long_page(self):
        page = ParsedPage(
            url="http://example.com/", 
            final_url="http://example.com/", 
            status_code=200, 
            content_type="text/html",
            visible_text="word " * 3001,
            headings=[Heading(1, "Title")]
        )
        issues = EngagementAnalyzer.analyze({page.url: page})
        wall = [i for i in issues if i.title == "Unstructured Wall of Text"]
        self.assertEqual(len(wall), 0)

if __name__ == '__main__':
    unittest.main()
