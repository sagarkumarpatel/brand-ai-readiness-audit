# Architecture

## Overview
The system is an Agent Skill Marketplace consisting of exactly four skills, coordinated by a single entrypoint skill. 

## Component Diagram
```
1 Marketplace
    │
    ├── 1 Entrypoint Skill
    │      └── audit-orchestrator
    │
    ├── Supporting Skill
    │      └── crawl-render-audit
    │
    ├── Supporting Skill
    │      └── freshness-corroboration
    │
    └── Supporting Skill
           └── engagement-audit
```

## Engines (Shared Library / src/)
The skills depend on the following shared underlying engines:
- **Crawler**: Safe, read-only HTTP engine respecting robots.txt and limits.
- **Renderer**: Selective browser rendering to compare raw vs rendered DOM.
- **Parser**: Extracts HTML tags, text, and structure.
- **Structured Data**: Extracts JSON-LD, schema.org, and Open Graph.
- **Facts**: Determines deterministic facts from parsed content.
- **Freshness**: Assesses temporal relevance based on timestamps and content.
- **Engagement**: Heuristics for CTA, navigation, and usability.
- **Evidence**: Collects robust proofs for detected issues.
- **Findings & Recommendations**: Formats output per the finding schema.
- **Reporting**: Final orchestration to generate JSON output.

## Interactions
1. `audit-orchestrator` receives the request.
2. `audit-orchestrator` delegates data gathering and localized analysis to the supporting skills.
3. Supporting skills rely on engines to parse and evaluate the target.
4. Outputs are aggregated, normalized, deduplicated, and formatted into the final report by `audit-orchestrator`.
