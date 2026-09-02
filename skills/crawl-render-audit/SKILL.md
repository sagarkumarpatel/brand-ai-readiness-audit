---
name: crawl-render-audit
description: Audits a website for discoverability problems via safe crawling, DOM rendering, and structured data extraction.
license: UNLICENSED
---

# Crawl and Render Audit

## When to use
Invoked by the `audit-orchestrator` to perform technical HTTP, DOM, and metadata analysis on a website to uncover discoverability barriers.

## Inputs
Target website URL and crawl configuration parameters (e.g., max_pages, max_depth).

## Procedure
1. Enforce strict robots.txt, domain boundaries, and rate limits.
2. Safely crawl URLs starting from the root and sitemap.
3. Selectively render pages suspected of heavy JavaScript dependency.
4. Extract structural components, metadata, JSON-LD, and Schema.org data.
5. Identify crawl barriers, render-locked content, missing metadata, and broken links.
6. Return a normalized set of evidence-backed technical findings.

## Output
A list of preliminary technical findings, each containing observable evidence (e.g., HTML snippets, status codes, DOM diffs).

## Allowed Tools
- Default API tools for HTTP requests and DOM parsing/rendering.
