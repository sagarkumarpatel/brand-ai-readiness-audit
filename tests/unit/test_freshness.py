import unittest
import json
from src.parser.models import ParsedPage, Link
from src.freshness.engine import FreshnessCorroborationEngine

class TestFreshnessEngine(unittest.TestCase):
    def test_consistent_facts(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[Link("tel:+123", "Phone", True)],
                           main_content="", visible_text="")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[Link("tel:+123", "Call us", True)],
                           main_content="", visible_text="")
        
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        self.assertEqual(len(issues), 0)

    def test_contradicting_facts(self):
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[Link("tel:+123", "Phone", True)],
                           main_content="", visible_text="")
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[Link("tel:+456", "Phone", True)],
                           main_content="", visible_text="")
        
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        
        # Depending on if we check BRAND_NAME, we might get missing brand name issue as well.
        # Let's filter for Contradicting Phone
        phone_issues = [i for i in issues if "Contradicting Phone" in i.title]
        self.assertEqual(len(phone_issues), 1)
        self.assertEqual(phone_issues[0].severity, "HIGH")

    def test_json_ld_extraction(self):
        json_ld = json.dumps({"@type": "Organization", "name": "Acme Corp", "telephone": "999-999-9999"})
        page1 = ParsedPage(url="http://example.com/1", final_url="http://example.com/1", status_code=200, content_type="text/html",
                           title="Example", canonical_url="", headings=[], links=[],
                           main_content="", visible_text="", json_ld_blocks=[json_ld])
        
        json_ld2 = json.dumps({"@type": "Organization", "name": "Acme Corp", "telephone": "888-888-8888"})
        page2 = ParsedPage(url="http://example.com/2", final_url="http://example.com/2", status_code=200, content_type="text/html",
                           title="Example 2", canonical_url="", headings=[], links=[],
                           main_content="", visible_text="", json_ld_blocks=[json_ld2])
        
        issues = FreshnessCorroborationEngine.analyze({page1.url: page1, page2.url: page2})
        phone_issues = [i for i in issues if "Contradicting Phone" in i.title]
        self.assertEqual(len(phone_issues), 1)
        self.assertEqual(phone_issues[0].severity, "HIGH")

if __name__ == '__main__':
    unittest.main()
