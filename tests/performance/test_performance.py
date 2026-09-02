import unittest
import time
import asyncio
from unittest.mock import patch

from src.crawler.models import CrawlResponse
from scripts.benchmark import audit_orchestrator

class TestPerformance(unittest.IsolatedAsyncioTestCase):
    
    @patch('audit_orchestrator.SafeCrawler.crawl')
    async def test_processing_pipeline_performance(self, mock_crawl):
        """
        Tests that the non-crawling portion of the pipeline (parsing + analysis + reporting)
        can process a medium site (100 pages) well within the 5 minute constraint.
        Since we proved crawler delay is the only significant overhead, this ensures
        the actual compute components do not regress.
        """
        
        # Generate 100 mock pages
        pages = []
        for i in range(100):
            html = f"""
            <html>
                <head><title>Page {i}</title></head>
                <body>
                    <h1>Welcome to Page {i}</h1>
                    <p>Some text content {i}</p>
                    <a href="/page{i+1}.html">Next</a>
                </body>
            </html>
            """
            pages.append(CrawlResponse(
                url=f"http://example.com/page{i}.html",
                status_code=200,
                headers={"Content-Type": "text/html"},
                content_type="text/html",
                html=html,
                redirect_chain=[],
                depth=1,
                parent_url="http://example.com",
                timing_ms=50.0,
                error=None
            ))
            
        mock_crawl.return_value = pages
        
        start_time = time.perf_counter()
        
        # Run the audit
        report = await audit_orchestrator.run_audit("http://example.com", max_pages=100)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # The computation for 100 simple pages should be well under 2.0 seconds
        # (Observed baseline is ~0.35s).
        self.assertLess(total_time, 2.0, "Pipeline compute for 100 pages exceeded 2.0 seconds")
        
        # Verify it actually produced a report
        self.assertIsNotNone(report["data"])
        self.assertGreaterEqual(report["data"].summary.total_findings, 2)

if __name__ == '__main__':
    unittest.main()
