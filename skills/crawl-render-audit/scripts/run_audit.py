import argparse
import json
import dataclasses
import os
import sys
from urllib.parse import urlparse

# Ensure src modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.crawler.crawler import SafeCrawler
from src.crawler.models import CrawlConfig
from src.parser.html_analyzer import parse_html
from src.renderer.renderer import SafeRenderer
from src.renderer.comparator import PageComparator
from src.analysis.discoverability import SiteDiscoverabilityEngine

def main():
    parser = argparse.ArgumentParser(description="Run the Crawl & Render Audit")
    parser.add_argument("--start-url", required=True, help="The target URL to audit")
    parser.add_argument("--max-pages", type=int, default=10, help="Max pages to crawl")
    args = parser.parse_args()

    domain = urlparse(args.start_url).netloc
    config = CrawlConfig(max_pages=args.max_pages, allowed_domains=[domain])
    crawler = SafeCrawler(config)
    
    print(f"Crawling {args.start_url}...")
    crawl_responses = crawler.crawl([args.start_url])
    
    parsed_pages = {}
    for resp in crawl_responses:
        if resp.html:
            parsed = parse_html(resp.html, resp.url)
            if parsed:
                parsed_pages[resp.url] = parsed
                
    render_comparisons = {}
    comparator = PageComparator()
    
    try:
        with SafeRenderer() as renderer:
            print("Rendering pages to detect JS dependencies...")
            for resp in crawl_responses:
                if resp.html and resp.status_code == 200:
                    render_result = renderer.render(resp.url)
                    if render_result.rendered_successfully and resp.url in parsed_pages:
                        comp = comparator.compare(parsed_pages[resp.url], render_result)
                        render_comparisons[resp.url] = comp
    except RuntimeError as e:
        print(f"Skipping rendering: {e}")
        
    print("Analyzing discoverability...")
    engine = SiteDiscoverabilityEngine()
    sitemap_urls = crawler.sitemap_urls if hasattr(crawler, 'sitemap_urls') else []
    report = engine.analyze(crawl_responses, parsed_pages, render_comparisons, sitemap_urls=sitemap_urls)
    
    output_data = [dataclasses.asdict(issue) for issue in report.issues]
    
    with open("audit_report.json", "w") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Audit complete. Found {len(output_data)} issues. Wrote to audit_report.json")

if __name__ == "__main__":
    main()
