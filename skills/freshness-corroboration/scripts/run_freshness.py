import argparse
import sys
import json
from urllib.parse import urlparse
from dataclasses import asdict
from src.crawler.crawler import SafeCrawler
from src.crawler.models import CrawlConfig
from src.parser.html_analyzer import parse_html
from src.freshness.engine import FreshnessCorroborationEngine

def main():
    parser = argparse.ArgumentParser(description="Freshness & Corroboration Audit Skill")
    parser.add_argument("--url", required=True, help="Target URL to audit")
    args = parser.parse_args()

    print(f"Starting Freshness & Corroboration audit for: {args.url}")
    
    # 1. Crawl
    domain = urlparse(args.url).netloc
    config = CrawlConfig(max_pages=10, allowed_domains=[domain])
    crawler = SafeCrawler(config)
    crawl_responses = crawler.crawl([args.url])
    
    # 2. Parse
    parsed_pages = {}
    for resp in crawl_responses:
        try:
            if resp.html:
                parsed = parse_html(resp.html, resp.url)
                if parsed:
                    parsed_pages[parsed.url] = parsed
        except Exception as e:
            print(f"Error parsing {resp.url}: {e}")
            
    # 3. Analyze Freshness & Corroboration
    issues = FreshnessCorroborationEngine.analyze(parsed_pages)
    
    # 4. Report
    report = [asdict(issue) for issue in issues]
    
    with open("freshness_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Audit complete. Found {len(issues)} issues. Wrote to freshness_report.json")

if __name__ == "__main__":
    main()
