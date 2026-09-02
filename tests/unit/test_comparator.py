import unittest
from src.parser.models import ParsedPage, Link
from src.renderer.models import RenderResult
from src.renderer.comparator import PageComparator

class TestComparator(unittest.TestCase):
    def setUp(self):
        self.comparator = PageComparator()
        self.parsed = ParsedPage(url="http://example.com", final_url="http://example.com", status_code=200, content_type="text/html")
        self.parsed.visible_text = "Raw content"
        self.parsed.links = [Link(url="http://example.com/1", anchor_text="1", is_internal=True)]
        
        self.rendered = RenderResult(requested_url="http://example.com", final_url="http://example.com", status_code=200, rendered_successfully=True, html="<html></html>", visible_text="Raw content")
        self.rendered.links = [Link(url="http://example.com/1", anchor_text="1", is_internal=True)]

    def test_no_difference(self):
        res = self.comparator.compare(self.parsed, self.rendered)
        self.assertFalse(res.js_dependent_content)
        self.assertFalse(res.js_dependent_links)

    def test_js_dependent_content(self):
        self.rendered.visible_text = "Raw content" + (" and some more" * 50)
        res = self.comparator.compare(self.parsed, self.rendered)
        self.assertTrue(res.js_dependent_content)

    def test_js_dependent_links(self):
        for i in range(10):
            self.rendered.links.append(Link(url=f"http://example.com/{i+2}", anchor_text=str(i+2), is_internal=True))
        res = self.comparator.compare(self.parsed, self.rendered)
        self.assertTrue(res.js_dependent_links)

if __name__ == '__main__':
    unittest.main()
