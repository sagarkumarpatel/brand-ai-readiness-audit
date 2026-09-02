import unittest
from src.parser.html_analyzer import parse_html

class TestParser(unittest.TestCase):
    def test_basic_parsing(self):
        html = """
        <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="A test description">
            <meta name="robots" content="noindex, nofollow">
            <link rel="canonical" href="http://example.com/canonical">
        </head>
        <body>
            <main>
                <h1>Main Heading</h1>
                <p>Some visible text.</p>
                <a href="/internal">Internal Link</a>
                <a href="http://external.com">External Link</a>
            </main>
        </body>
        </html>
        """
        parsed = parse_html(html, "http://example.com")
        self.assertEqual(parsed.title, "Test Page")
        self.assertEqual(parsed.meta_description, "A test description")
        self.assertIn("noindex", parsed.robots_directives)
        self.assertEqual(parsed.canonical_url, "http://example.com/canonical")
        self.assertEqual(len(parsed.headings), 1)
        self.assertEqual(parsed.headings[0].text, "Main Heading")
        self.assertEqual(len(parsed.links), 2)
        self.assertTrue(parsed.links[0].is_internal)
        self.assertFalse(parsed.links[1].is_internal)
        self.assertEqual(parsed.links[0].anchor_text, "Internal Link")

    def test_json_ld(self):
        html = """
        <script type="application/ld+json">
        {"@context": "https://schema.org", "@type": "Product", "name": "Shoe"}
        </script>
        """
        parsed = parse_html(html, "http://example.com")
        self.assertEqual(len(parsed.json_ld_blocks), 1)
        self.assertIn("Product", parsed.json_ld_blocks[0])

    def test_malformed_html(self):
        html = "<title>Unclosed Title <p>Oops</p>"
        parsed = parse_html(html, "http://example.com")
        # html.parser handles this gracefully
        self.assertIsNotNone(parsed)

    def test_empty_html(self):
        parsed = parse_html("", "http://example.com")
        self.assertEqual(parsed.title, None)
        self.assertEqual(len(parsed.links), 0)

if __name__ == '__main__':
    unittest.main()
