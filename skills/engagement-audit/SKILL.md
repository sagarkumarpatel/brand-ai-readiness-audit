---
name: engagement-audit
description: Evaluates observable on-site engagement risks such as weak navigation and poor information clarity.
license: UNLICENSED
---

# Engagement Audit Skill

## When to use
Invoked to analyze website structure and layout to identify objective, evidence-backed friction points that hinder visitor engagement. Do NOT use this to fabricate analytics data (e.g. bounce rate, conversion rate).

## Inputs
- `url`: The starting URL of the website to audit (string).
- `max_pages`: The maximum number of pages to crawl (integer, default 10).

## Procedure
1. Execute `scripts/engagement-audit.py <url> --max-pages <max_pages>`
2. The script will initialize the crawler, parse the raw HTML, and run the `EngagementAnalyzer`.
3. The engine deterministically evaluates:
   - Thin / Blank content (<15 words, lacking media).
   - Dead End pages (0 internal links on non-root pages).
   - Wall of Text (>3000 words without semantic headings).
4. Extract the findings from the generated `engagement_audit_report.json`.
5. Return the findings to the caller. Do NOT add subjective assumptions about user behavior.

## Output
A list of engagement findings containing `severity`, `confidence`, `evidence`, `why`, and `action`.

## Allowed Tools
- `run_command` (to execute the orchestration script).
- `view_file` (to read the JSON output).
