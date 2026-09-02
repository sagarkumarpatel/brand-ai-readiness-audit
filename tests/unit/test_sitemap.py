import unittest
from unittest.mock import patch, MagicMock
from src.crawler.sitemap import SitemapParser

class TestSitemap(unittest.TestCase):
    def setUp(self):
        self.parser = SitemapParser()

    @patch('urllib.request.urlopen')
    def test_extract_urls(self, mock_urlopen):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url>
              <loc>http://example.com/page1</loc>
           </url>
           <url>
              <loc>http://example.com/page2</loc>
           </url>
        </urlset>"""
        
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = xml_content
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        urls = self.parser.extract_urls("http://example.com/sitemap.xml")
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0], "http://example.com/page1")
        self.assertEqual(urls[1], "http://example.com/page2")

if __name__ == '__main__':
    unittest.main()
