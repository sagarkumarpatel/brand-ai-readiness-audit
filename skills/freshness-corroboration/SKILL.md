---
name: freshness-corroboration
description: Analyzes facts extracted from the website for consistency, contradictions, and temporal relevance.
license: UNLICENSED
---

# Freshness and Corroboration Audit

## When to use
Invoked by the `audit-orchestrator` to analyze extracted website facts, ensuring the content is temporally valid and internally consistent.

## Inputs
A dataset of facts and observations gathered during the crawl phase.

## Procedure
1. Map facts to their source URLs, page types, and entity types.
2. Compare structured-data claims against visible text claims.
3. Compare claims across different pages for contradiction or agreement.
4. Evaluate timestamps, publication dates, and modification dates for staleness.
5. Resolve facts into states: RESOLVED, PROBABLE, UNRESOLVED, or INSUFFICIENT_EVIDENCE.
6. Generate findings for contradictions and critically stale content.

## Output
A list of preliminary freshness and corroboration findings, each containing observable evidence (e.g., conflicting text snippets or mismatched timestamps).

## Allowed Tools
- Default API tools for text processing and logic evaluation.
