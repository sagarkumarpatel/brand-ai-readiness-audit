import argparse
import json
import logging
from datetime import datetime, timezone
import asyncio
import sys
from typing import List
from urllib.parse import urlparse

from src.crawler.crawler import SafeCrawler
from src.crawler.models import CrawlConfig, CrawlResponse
from src.parser.models import ParsedPage
from src.parser.html_analyzer import HTMLAnalyzer
from src.analysis.discoverability import SiteDiscoverabilityEngine
from src.freshness.engine import FreshnessCorroborationEngine
from src.engagement.engine import EngagementAnalyzer
from src.findings.composer import FindingComposer
from src.recommendations.engine import RecommendationEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mocked crawl response class because SafeCrawler returns List[CrawlResponse] instead of a single object containing `pages`
class CrawlRunResponse:
    def __init__(self, pages: List[CrawlResponse]):
        self.pages = pages

async def run_audit(url: str):
    logger.info(f"Starting audit for {url}")
    
    # 1. Crawl
    domain = urlparse(url).netloc
    config = CrawlConfig(
        max_pages=10, 
        max_depth=2, 
        allowed_domains=[domain] if domain else []
    )
    crawler = SafeCrawler(config)
    try:
        pages = crawler.crawl([url])
        crawl_response = CrawlRunResponse(pages=pages)
    except Exception as e:
        logger.error(f"Failed to crawl {url}: {e}")
        return _generate_error_report(url, str(e))

    # 2. Parse HTML
    parsed_pages = {}
    for page in crawl_response.pages:
        if page.html and not page.error:
            try:
                parsed = HTMLAnalyzer.parse(page.html, page.url)
                parsed_pages[page.url] = parsed
            except Exception as e:
                logger.warning(f"Failed to parse {page.url}: {e}")

    # 3. Analyze
    raw_issues = []
    
    try:
        disc_analyzer = SiteDiscoverabilityEngine()
        disc_report = disc_analyzer.analyze(crawl_response.pages, parsed_pages, render_comparisons={})
        raw_issues.extend(disc_report.issues)
    except Exception as e:
        logger.error(f"Discoverability analysis failed: {e}")

    try:
        freshness_analyzer = FreshnessCorroborationEngine()
        freshness_issues = freshness_analyzer.analyze(parsed_pages)
        raw_issues.extend(freshness_issues)
    except Exception as e:
        logger.error(f"Freshness analysis failed: {e}")

    try:
        engagement_analyzer = EngagementAnalyzer()
        engagement_issues = engagement_analyzer.analyze(parsed_pages)
        raw_issues.extend(engagement_issues)
    except Exception as e:
        logger.error(f"Engagement analysis failed: {e}")

    # 4. Compose Findings
    try:
        normalized_findings = FindingComposer.compose(raw_issues, source_engine="audit-orchestrator")
    except Exception as e:
        logger.error(f"Finding composer failed: {e}")
        normalized_findings = []

    # 5. Generate Recommendations and Build Report Output
    final_findings = []
    
    for finding in normalized_findings:
        try:
            rec = RecommendationEngine.generate(finding)
            if not rec:
                continue # Safety: if recommendation engine rejects it, drop it.
                
            final_findings.append({
                "id": finding.id,
                "title": finding.title,
                "severity": finding.severity,
                "evidence": finding.evidence,
                "suggested_action": {
                    "summary": rec.suggested_action.get("summary", ""),
                    "priority": rec.suggested_action.get("priority", "LOW")
                },
                "confidence": finding.confidence,
                "why": finding.why_it_matters
            })
        except Exception as e:
            logger.error(f"Failed to generate recommendation for finding {finding.id}: {e}")

    # 6. Final Report via Reporting Layer
    try:
        from src.reporting.generator import ReportGenerator
        from src.reporting.serializer import ReportSerializer
        
        report_data = ReportGenerator.build_report(url, final_findings)
        
        return {
            "json": ReportSerializer.to_json(report_data),
            "markdown": ReportSerializer.to_markdown(report_data),
            "data": report_data
        }
    except Exception as e:
        logger.error(f"Reporting failed: {e}")
        return _generate_error_report(url, f"Reporting failed: {e}")

def _generate_error_report(url: str, error_msg: str):
    return {
        "json": json.dumps({
            "site": url,
            "audited_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_findings": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "findings": [],
            "error": error_msg
        }, indent=2),
        "markdown": f"# AI Website Readiness Audit\n\n## Site\n{url}\n\n## Error\n{error_msg}",
        "data": None
    }

def main():
    parser = argparse.ArgumentParser(description="Audit Orchestrator")
    parser.add_argument("--url", required=True, help="The URL to audit")
    parser.add_argument("--output", default="audit_report", help="Output base filename (without extension)")
    args = parser.parse_args()

    report = asyncio.run(run_audit(args.url))

    with open(f"{args.output}.json", "w", encoding="utf-8") as f:
        f.write(report["json"])
        
    with open(f"{args.output}.md", "w", encoding="utf-8") as f:
        f.write(report["markdown"])
        
    if report["data"]:
        print(f"Audit complete. Found {report['data'].summary.total_findings} issues. Wrote to {args.output}.json and {args.output}.md")
    else:
        print(f"Audit failed. Wrote error report to {args.output}.json")

if __name__ == "__main__":
    main()
