import unittest
import os
import json
import tempfile
import sys
import importlib.util
from unittest.mock import patch, MagicMock

# Dynamically import the run_audit script because of the hyphen in directory name
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../skills/crawl-render-audit/scripts/run_audit.py'))
spec = importlib.util.spec_from_file_location("run_audit", script_path)
run_audit = importlib.util.module_from_spec(spec)
sys.modules["run_audit"] = run_audit
spec.loader.exec_module(run_audit)

class TestCrawlRenderAuditSkill(unittest.TestCase):
    @patch('run_audit.SafeCrawler')
    @patch('run_audit.SafeRenderer')
    def test_run_audit_script(self, mock_renderer_class, mock_crawler_class):
        # Setup mocks
        mock_crawler = MagicMock()
        mock_crawler_class.return_value = mock_crawler
        
        from src.crawler.models import CrawlResponse
        resp = CrawlResponse(
            url="http://example.com", 
            status_code=200, 
            headers={}, 
            content_type="text/html", 
            html="<html><head><title>Test</title></head><body></body></html>", 
            redirect_chain=[], 
            depth=0, 
            parent_url=None, 
            timing_ms=50.0
        )
        mock_crawler.crawl.return_value = [resp]
        mock_crawler.sitemap_urls = []
        
        # We mock SafeRenderer to raise RuntimeError to simulate missing playwright
        # so we don't try to launch a real browser in unit tests
        mock_renderer_class.side_effect = RuntimeError("Playwright not installed")
        
        # Run script with arguments
        test_args = ["run_audit.py", "--start-url", "http://example.com"]
        with patch.object(sys, 'argv', test_args):
            # Change working directory to a temp dir so we don't clutter the project
            with tempfile.TemporaryDirectory() as temp_dir:
                original_cwd = os.getcwd()
                os.chdir(temp_dir)
                try:
                    run_audit.main()
                    self.assertTrue(os.path.exists("audit_report.json"))
                    with open("audit_report.json", "r") as f:
                        data = json.load(f)
                        # We expect "Missing Canonical URL" and "Missing Structured Data"
                        # because our mock HTML doesn't have them
                        self.assertTrue(len(data) > 0)
                finally:
                    os.chdir(original_cwd)

if __name__ == '__main__':
    unittest.main()
