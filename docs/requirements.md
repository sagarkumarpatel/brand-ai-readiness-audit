# Requirements

## Core Objective
Build a reusable Agent Skill Marketplace that receives a website audit request and produces a structured, evidence-backed Website AI Readiness Audit Report for arbitrary public websites.

## System Capabilities
- Discoverability Audit: Identifies why AI assistants may fail to discover, understand, trust, or cite the website/brand.
- On-site Engagement Audit: Identifies why visitors may fail to understand the website, trust its content, find important information, navigate effectively, or continue engaging.

## Constraints
- Read-only operations (no modifications, destructive actions, or form submissions).
- No mandatory language model dependency.
- Agent Skills specification format required.
- Typical audit runtime < 5 minutes.
- Final submission zip size < 50 MB.
- Deterministic behavior where possible.
- Evidence-first principle (no evidence = no finding).
- Graceful error handling (no crashing on individual page failures).

## Input Format
```json
{
  "site": "https://example.com"
}
```

## Output Format
```json
{
  "site": "https://example.com",
  "audited_at": "ISO-8601-TIMESTAMP",
  "summary": {
    "total_findings": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  },
  "findings": []
}
```
