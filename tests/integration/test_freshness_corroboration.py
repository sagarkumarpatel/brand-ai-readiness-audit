import unittest
from src.parser.models import ParsedPage, Link
from src.freshness.engine import FreshnessCorroborationEngine

class TestFreshnessCorroboration(unittest.TestCase):
    def test_consistent_facts_no_finding(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[Link("tel:+123", "Phone", True)],
                           main_content="", visible_text="Copyright 2026")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[Link("tel:+123", "Call us", True)],
                           main_content="", visible_text="Copyright 2026")
        
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        self.assertEqual(len(issues), 0)

    def test_contradictory_phone_numbers(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[Link("tel:+123", "Phone", True)],
                           main_content="", visible_text="Copyright 2026")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[Link("tel:+456", "Call us", True)],
                           main_content="", visible_text="Copyright 2026")
        
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        phone_issues = [i for i in issues if "Contradicting Phone" in i.title]
        self.assertEqual(len(phone_issues), 1)

    def test_stale_content_finding(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[],
                           main_content="", visible_text="© 2023 Acme Corp")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[],
                           main_content="", visible_text="Copyright 2021")
                           
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        stale_issues = [i for i in issues if i.title == "Stale Content"]
        self.assertEqual(len(stale_issues), 1)
        self.assertIn("2023", stale_issues[0].evidence[0])

    def test_stale_and_contradiction(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[Link("mailto:a@b.com", "Email", True)],
                           main_content="", visible_text="Copyright 2024")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[Link("mailto:b@c.com", "Email", True)],
                           main_content="", visible_text="Copyright 2024")
                           
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        stale_issues = [i for i in issues if i.title == "Stale Content"]
        self.assertEqual(len(stale_issues), 1)
        email_issues = [i for i in issues if "Contradicting Email" in i.title]
        self.assertEqual(len(email_issues), 1)

if __name__ == '__main__':
    unittest.main()
