import argparse
import json
import logging
import sys
import os
import dataclasses

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.crawler.crawler import SafeCrawler
from src.crawler.models import CrawlConfig
from src.parser.html_analyzer import parse_html
from src.engagement.engine import EngagementAnalyzer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Engagement Audit Skill")
    parser.add_argument("url", help="Target URL to audit")
    parser.add_argument("--max-pages", type=int, default=10, help="Max pages to crawl")
    parser.add_argument("--output", type=str, default="engagement_audit_report.json", help="Output file")
    
    args = parser.parse_args()
    
    logging.info(f"Crawling {args.url} (max {args.max_pages} pages)...")
    
    config = CrawlConfig(max_pages=args.max_pages, allowed_domains=[])
    crawler = SafeCrawler(config)
    crawl_responses = crawler.crawl(args.url)
    
    logging.info(f"Parsing {len(crawl_responses)} pages...")
    parsed_pages = {}
    for resp in crawl_responses:
        if resp.html:
            parsed = parse_html(resp.html, resp.url)
            if parsed:
                parsed_pages[resp.url] = parsed
            
    logging.info("Analyzing engagement signals...")
    issues = EngagementAnalyzer.analyze(parsed_pages)
    
    report = {
        "target": args.url,
        "pages_analyzed": len(parsed_pages),
        "issues_found": len(issues),
        "findings": [dataclasses.asdict(i) for i in issues]
    }
    
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
        
    logging.info(f"Audit complete. Found {len(issues)} issues. Wrote to {args.output}")

if __name__ == "__main__":
    main()
