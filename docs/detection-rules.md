# Detection Rules

Detection rules must adhere to the Evidence-First Principle: NO EVIDENCE = NO FINDING.

## Discoverability (crawl-render-audit)
- **Unreachable Important Pages**: Pages present in sitemap but returning 4xx/5xx or blocked by robots.txt in a conflicting way.
- **Render-locked Content**: Important text or links that exist in the rendered DOM but not in the raw HTML.
- **Metadata Gaps**: Missing canonical tags, conflicting canonical tags, or missing structured data for obvious entities.
- **Crawl Barriers**: Excessive redirect chains or broken internal links.

## Freshness & Corroboration (freshness-corroboration)
- **Contradictions**: Mismatched facts across pages (e.g., pricing discrepancy, different phone numbers).
- **Stale Content**: Outdated temporal indicators on pages where currency matters (e.g., an outdated pricing page).
- **Uncorroborated Claims**: Important entities/facts that appear only once without sufficient contextual support.

## Engagement (engagement-audit)
- **Broken Navigation**: Links to dead pages in primary navigation.
- **Weak Information Hierarchy**: Missing obvious structural tags (H1, H2) for core content.
- **Dead-end Pages**: Pages with no internal links or clear calls to action.
- **Client-side Dependency**: Core engagement elements that are inaccessible without heavy JS execution.

## Generalization constraint
Rules must be context-agnostic. No domain-specific logic (`if site == garuda`). Focus on standard web technologies (HTML, HTTP, JSON-LD).
