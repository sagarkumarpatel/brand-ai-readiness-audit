# Evidence Model

Every finding MUST be backed by concrete, observable evidence. Assumptions are not permitted.

## Valid Evidence Types
- **HTTP Context**: URLs, status codes, redirect chains, headers.
- **DOM State**: Specific HTML elements, CSS selectors, raw vs rendered DOM diffs.
- **Metadata**: JSON-LD snippets, meta tag contents, canonical links.
- **Visible Text**: Extracted text content demonstrating a claim.
- **Timestamps**: Explicit dates found in content or metadata.
- **Relationships**: Link graphs or sitemap vs crawl comparisons.

## Required Information for a Finding
1. **What**: What exactly was detected?
2. **Evidence**: Concrete proof (e.g., "URL X returned 404", "Page Y raw HTML length 100 bytes, rendered length 10,000 bytes").
3. **Why**: Why this impacts discoverability or engagement.
4. **Action**: What should be changed.
5. **Confidence**: HIGH, MEDIUM, LOW.

## Finding Schema Context
```json
{
  "evidence": [
    "String describing the exact evidence found, including URLs and snippets if applicable."
  ]
}
```
