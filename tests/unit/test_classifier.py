import unittest
from src.parser.models import ParsedPage
from src.parser.classifier import PageClassifier

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = PageClassifier()

    def test_url_heuristics(self):
        page = ParsedPage(url="http://example.com/", final_url="http://example.com/", status_code=200, content_type="text/html")
        self.assertEqual(self.classifier.classify(page), "homepage")

        page.url = "http://example.com/product/123"
        self.assertEqual(self.classifier.classify(page), "product")

    def test_json_ld_heuristics(self):
        page = ParsedPage(url="http://example.com/random", final_url="http://example.com/random", status_code=200, content_type="text/html")
        page.json_ld_blocks = ['{"@type": "Article"}']
        self.assertEqual(self.classifier.classify(page), "article")

    def test_open_graph_heuristics(self):
        page = ParsedPage(url="http://example.com/random", final_url="http://example.com/random", status_code=200, content_type="text/html")
        page.open_graph = {"og:type": "product"}
        self.assertEqual(self.classifier.classify(page), "product")

    def test_generic_fallback(self):
        page = ParsedPage(url="http://example.com/random", final_url="http://example.com/random", status_code=200, content_type="text/html")
        self.assertEqual(self.classifier.classify(page), "generic")

if __name__ == '__main__':
    unittest.main()
