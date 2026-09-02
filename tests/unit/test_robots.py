import unittest
from unittest.mock import patch
from src.crawler.robots import RobotsTxtHandler

class TestRobots(unittest.TestCase):
    def setUp(self):
        self.handler = RobotsTxtHandler("Bot/1.0")

    @patch('urllib.request.urlopen')
    @patch('urllib.robotparser.RobotFileParser.can_fetch')
    def test_allowed(self, mock_can_fetch, mock_urlopen):
        mock_can_fetch.return_value = True
        self.assertTrue(self.handler.is_allowed("http://example.com/page"))
        mock_can_fetch.assert_called_with("Bot/1.0", "http://example.com/page")

    @patch('urllib.request.urlopen')
    @patch('urllib.robotparser.RobotFileParser.can_fetch')
    def test_disallowed(self, mock_can_fetch, mock_urlopen):
        mock_can_fetch.return_value = False
        self.assertFalse(self.handler.is_allowed("http://example.com/secret"))

    @patch('urllib.request.urlopen')
    def test_fetch_failure_allows(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network error")
        # If robots.txt fails to load, convention is to allow
        self.assertTrue(self.handler.is_allowed("http://example.com/page"))

if __name__ == '__main__':
    unittest.main()
