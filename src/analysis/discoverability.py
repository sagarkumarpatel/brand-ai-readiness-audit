from typing import List, Dict, Optional
from src.crawler.models import CrawlResponse
from src.parser.models import ParsedPage
from src.renderer.models import RenderResult, ComparisonResult
from src.parser.classifier import PageClassifier
from .models import Issue, AuditReport

class SiteDiscoverabilityEngine:
    def __init__(self):
        self.classifier = PageClassifier()

    def analyze(self, 
                crawl_responses: List[CrawlResponse], 
                parsed_pages: Dict[str, ParsedPage], 
                render_comparisons: Dict[str, ComparisonResult],
                sitemap_urls: List[str] = None) -> AuditReport:
        
        report = AuditReport()
        sitemap_set = set(sitemap_urls or [])
        
        # 1. Unreachable Important Pages
        for resp in crawl_responses:
            if resp.url in sitemap_set and resp.status_code >= 400:
                report.add_issue(Issue(
                    title="Unreachable Important Page",
                    severity="HIGH",
                    confidence="HIGH",
                    evidence=[f"URL {resp.url} is listed in the sitemap but returned status code {resp.status_code}."],
                    why="AI crawlers and search engines rely on sitemaps to find core content. Dead links in the sitemap erode crawl budget and trust.",
                    action="Remove the URL from the sitemap or restore the page."
                ))
            
            if resp.url in sitemap_set and resp.error and "robots" in resp.error.lower():
                report.add_issue(Issue(
                    title="Sitemap Page Blocked by Robots.txt",
                    severity="CRITICAL",
                    confidence="HIGH",
                    evidence=[f"URL {resp.url} is in the sitemap but blocked by robots.txt directives."],
                    why="Conflicting directives confuse AI agents. If it is in the sitemap, it must be crawlable.",
                    action="Update robots.txt to allow crawling, or remove from sitemap."
                ))
                
            # Crawl Barriers (Redirect Chains)
            if len(resp.redirect_chain) > 3:
                report.add_issue(Issue(
                    title="Excessive Redirect Chain",
                    severity="MEDIUM",
                    confidence="HIGH",
                    evidence=[f"URL {resp.url} redirects {len(resp.redirect_chain)} times before resolving."],
                    why="Excessive redirects slow down discovery and some AI crawlers will abort before reaching the final page.",
                    action="Update internal links to point directly to the final destination."
                ))

        # 2. Render-locked Content & Metadata Gaps
        for url, parsed in parsed_pages.items():
            page_type = self.classifier.classify(parsed)
            
            # Check for missing canonical
            if not parsed.canonical_url:
                report.add_issue(Issue(
                    title="Missing Canonical URL",
                    severity="LOW",
                    confidence="HIGH",
                    evidence=[f"URL {url} lacks a <link rel='canonical'> tag."],
                    why="AI systems need canonical tags to merge duplicate content correctly and attribute facts to the right source.",
                    action="Add self-referencing canonical tags to all indexable pages."
                ))
                
            # Check for missing structured data on important pages
            if page_type in ["product", "article"] and not parsed.json_ld_blocks:
                report.add_issue(Issue(
                    title="Missing Structured Data",
                    severity="HIGH",
                    confidence="HIGH",
                    evidence=[f"URL {url} is classified as a {page_type} but contains no JSON-LD structured data."],
                    why=f"Structured data is the most reliable way for an AI to parse {page_type} facts deterministically.",
                    action="Implement Schema.org JSON-LD matching the page content."
                ))
                
            # 3. Check CSR / Render Locked Content
            comp = render_comparisons.get(url)
            if comp:
                if comp.js_dependent_content:
                    report.add_issue(Issue(
                        title="Render-locked Content",
                        severity="HIGH",
                        confidence="HIGH",
                        evidence=[f"URL {url}: {msg}" for msg in comp.differences if "text added" in msg] or [f"URL {url} relies heavily on JavaScript to render its main text content."],
                        why="Many lightweight AI crawlers do not execute JavaScript. If content is missing from raw HTML, it will not be ingested.",
                        action="Implement Server-Side Rendering (SSR) or dynamic rendering for core text."
                    ))
                if comp.js_dependent_links:
                    report.add_issue(Issue(
                        title="Render-locked Navigation",
                        severity="HIGH",
                        confidence="HIGH",
                        evidence=[f"URL {url}: {msg}" for msg in comp.differences if "links added" in msg] or [f"URL {url} injects internal links via JavaScript."],
                        why="If links are not present in the raw HTML, AI crawlers cannot follow them to discover the rest of the site.",
                        action="Ensure standard <a href='...'> tags exist in the raw HTML response."
                    ))
                    
        return report
