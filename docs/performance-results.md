# Performance Review (Module 15)

## Overview

Module 15 focuses on profiling the Agent Skill Marketplace pipeline to ensure that audits complete within the targeted "< 5 minutes" window for typical sites, without sacrificing the evidence-first, deterministic, read-only approach.

## Benchmark Methodology

A synthetic benchmarking suite (`scripts/benchmark.py`) was created to simulate different website sizes locally. The benchmark measures End-to-End time and logs component-level timings (parsing, discoverability, freshness, engagement, finding composition, and report generation). 

The crawler is hard-coded with a `time.sleep(0.1)` safe rate limit to prevent DDOSing target domains.

## Baseline Results

| Site Size | Pages Crawled | Total E2E Time (s) | Crawl Overhead (s) | Parsing Time (s) | Analysis Time (s) |
|-----------|---------------|--------------------|--------------------|------------------|-------------------|
| **Tiny**  | 5             | 0.70               | ~0.6               | 0.0029           | ~0.001            |
| **Small** | 25            | 3.12               | ~3.0               | 0.0292           | ~0.001            |
| **Medium**| 100           | 12.54              | ~12.2              | 0.3206           | ~0.006            |

## Bottleneck Analysis

1. **Crawler Delay (95%+ of E2E time):** 
   The intentional `time.sleep(0.1)` rate limit between sequential page fetches accounts for nearly all of the runtime. At 100 pages, this adds exactly 10.0 seconds of forced waiting. 
2. **HTML Parsing:**
   The `HTMLAnalyzer` is remarkably efficient. Parsing 100 pages sequentially takes approximately 0.3 seconds.
3. **Analysis Engines:**
   Discoverability, Freshness, and Engagement engines combined take less than 0.01 seconds for 100 pages. 
4. **LLM/API Call Avoidance:**
   Because the entire pipeline is 100% deterministic (regex, HTML parsing, structural checks), we avoid the high latency (5-30s per page) that would typically accompany LLM-based scraping or evaluating.

## Optimization Decisions

1. **No Async Crawler Changes Needed:** 
   Even at 100 pages, the audit takes 12.5 seconds. For a "Max" site of 500 pages, it would take roughly 1 minute (500 * 0.1s = 50s crawl time). This is well under the required < 5 minute window. We intentionally retain sequential execution to keep the codebase simple and the server impact strictly polite.
2. **No Render Context Caching Needed:** 
   Because we only render pages conditionally (e.g., when the structural analysis determines it's necessary for discoverability checks like JS-locked content), the vast majority of pages are fetched as raw HTML. This preserves memory and CPU overhead.
3. **No Intermediate Result Caching Needed:** 
   Given that memory footprint and parsing speed are minimal, memoizing parse trees is completely unnecessary.

## Conclusion

The architecture is highly performant. The primary limit is the polite crawler delay, which ensures adherence to robots.txt and safe scraping. The Agent Skill Marketplace comfortably meets and exceeds the < 5 minutes constraint.
