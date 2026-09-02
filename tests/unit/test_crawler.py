import unittest
from unittest.mock import patch, MagicMock
from src.crawler.crawler import SafeCrawler
from src.crawler.models import CrawlConfig

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.config = CrawlConfig(
            max_pages=5,
            max_depth=2,
            allowed_domains=["example.com"]
        )
        self.crawler = SafeCrawler(self.config)
        # Mock robots.txt to always allow
        self.crawler.robots_handler.is_allowed = MagicMock(return_value=True)

    @patch('src.crawler.crawler.SafeCrawler._fetch')
    def test_basic_crawl(self, mock_fetch):
        mock_fetch.return_value = {
            'status': 200,
            'html': '<a href="/page2">Link</a>',
            'headers': {'Content-Type': 'text/html'},
            'content_type': 'text/html',
            'timing': 0.1
        }
        
        results = self.crawler.crawl(['http://example.com/'])
        self.assertEqual(len(results), 2) # Home and page2 (due to max_pages limitation/mock)
        self.assertEqual(results[0].url, 'http://example.com/')
        self.assertEqual(results[1].url, 'http://example.com/page2')
        self.assertEqual(results[1].parent_url, 'http://example.com/')
        self.assertEqual(results[1].depth, 1)

    @patch('src.crawler.crawler.SafeCrawler._fetch')
    def test_redirects(self, mock_fetch):
        def side_effect(url):
            if url == 'http://example.com/redirect':
                return {'status': 301, 'headers': {'Location': '/target'}, 'timing': 0.1}
            return {'status': 200, 'html': '', 'headers': {'Content-Type': 'text/html'}, 'timing': 0.1}
        mock_fetch.side_effect = side_effect
        
        results = self.crawler.crawl(['http://example.com/redirect'])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].url, 'http://example.com/target')
        self.assertEqual(len(results[0].redirect_chain), 1)
        self.assertEqual(results[0].redirect_chain[0], 'http://example.com/target')

    def test_domain_restriction(self):
        self.assertTrue(self.crawler._is_allowed_domain('http://example.com/test'))
        self.assertTrue(self.crawler._is_allowed_domain('http://sub.example.com/test'))
        self.assertFalse(self.crawler._is_allowed_domain('http://other.com/test'))

if __name__ == '__main__':
    unittest.main()
