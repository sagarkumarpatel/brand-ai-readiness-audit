import unittest
import asyncio
import sys
from typing import Dict
from unittest.mock import patch, MagicMock
from src.crawler.models import CrawlResponse
from src.parser.models import ParsedPage, Link, Heading
from src.engagement.engine import EngagementAnalyzer

class TestEngagementSkill(unittest.TestCase):
    def setUp(self):
        # We can test the skill execution by mocking the Crawler and Parser, but since we just
        # need to verify the orchestration logic, we can directly test the engine logic or we can
        # mock CrawlResponse -> ParsedPage to test end-to-end analyzer behavior.
        self.analyzer = EngagementAnalyzer()
        
    def _create_mock_parsed_page(self, url: str, visible_text: str, links: list = None, headings: list = None, status_code: int = 200) -> ParsedPage:
        return ParsedPage(
            url=url,
            final_url=url,
            status_code=status_code,
            content_type="text/html",
            visible_text=visible_text,
            links=links or [],
            headings=headings or []
        )

    def test_thin_blank_page(self):
        page = self._create_mock_parsed_page(
            url="http://test.com/thin",
            visible_text="Too short text."
        )
        issues = self.analyzer.analyze({page.url: page})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].title, "Thin Content")
        
        # Verify evidence does not contain fabricated analytics
        self.assertNotIn("bounce rate", issues[0].evidence[0].lower())
        self.assertNotIn("visitors", issues[0].evidence[0].lower())

    def test_valid_content_page(self):
        page = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="This is a valid content page with enough words to bypass the thin content filter.",
            links=[Link("http://test.com/about", "About", True)]
        )
        issues = self.analyzer.analyze({page.url: page})
        self.assertEqual(len(issues), 0)

    def test_dead_end_non_root_page(self):
        root = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="This is a valid root content page with enough words.",
            links=[Link("http://test.com/deep", "Deep", True)]
        )
        deep = self._create_mock_parsed_page(
            url="http://test.com/deep",
            visible_text="This is a deep page with enough words but it lacks any internal navigation links.",
            links=[]
        )
        issues = self.analyzer.analyze({root.url: root, deep.url: deep})
        dead_ends = [i for i in issues if i.title == "Dead End Page"]
        self.assertEqual(len(dead_ends), 1)
        self.assertIn("0 internal navigation links", dead_ends[0].evidence[0])

    def test_root_page_no_internal_links(self):
        # Should not incorrectly trigger dead-end rule
        root = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="This is a valid root content page with enough words to pass thin content but no links.",
            links=[]
        )
        issues = self.analyzer.analyze({root.url: root})
        dead_ends = [i for i in issues if i.title == "Dead End Page"]
        self.assertEqual(len(dead_ends), 0)

    def test_well_linked_page(self):
        root = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="This is a valid root content page with enough words to bypass the thin content filter successfully.",
            links=[Link("http://test.com/deep", "Deep", True)]
        )
        deep = self._create_mock_parsed_page(
            url="http://test.com/deep",
            visible_text="This is a deep page with enough words to bypass the thin content filter and it has some internal navigation links.",
            links=[Link("http://test.com/about", "About", True)]
        )
        issues = self.analyzer.analyze({root.url: root, deep.url: deep})
        self.assertEqual(len(issues), 0)

    def test_very_long_unstructured_content(self):
        root = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="word " * 3001,
            headings=[]
        )
        issues = self.analyzer.analyze({root.url: root})
        walls = [i for i in issues if i.title == "Unstructured Wall of Text"]
        self.assertEqual(len(walls), 1)
        self.assertIn("0 heading tags", walls[0].evidence[0])

    def test_long_content_with_headings(self):
        root = self._create_mock_parsed_page(
            url="http://test.com/",
            visible_text="word " * 3001,
            headings=[Heading(1, "Title"), Heading(2, "Subtitle")]
        )
        issues = self.analyzer.analyze({root.url: root})
        walls = [i for i in issues if i.title == "Unstructured Wall of Text"]
        self.assertEqual(len(walls), 0)

    def test_malformed_html(self):
        # The parser handles malformed HTML, and the engine acts purely on parsed results.
        # We simulate the parser output for malformed HTML (e.g., no text extracted).
        page = self._create_mock_parsed_page(
            url="http://test.com/malformed",
            visible_text=""
        )
        issues = self.analyzer.analyze({page.url: page})
        thin = [i for i in issues if i.title == "Thin Content"]
        self.assertEqual(len(thin), 1)

    def test_empty_page(self):
        page = self._create_mock_parsed_page(
            url="http://test.com/empty",
            visible_text=""
        )
        issues = self.analyzer.analyze({page.url: page})
        thin = [i for i in issues if i.title == "Thin Content"]
        self.assertEqual(len(thin), 1)

if __name__ == '__main__':
    unittest.main()
