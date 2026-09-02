---
name: audit-orchestrator
description: Entrypoint skill that orchestrates the AI readiness audit, coordinates supporting skills, and emits the final consolidated report.
license: UNLICENSED
---

# Audit Orchestrator

## When to use
Use this skill as the primary entrypoint when requested to perform a brand AI readiness audit on a given website. Do not invoke other skills manually; this skill will handle the composition.

## Inputs
A JSON configuration object containing at least the target website URL:
```json
{
  "site": "https://example.com"
}
```

## Procedure
1. Receive and validate the audit request configuration.
2. Delegate technical parsing and evaluation to `crawl-render-audit`.
3. Delegate fact and temporal analysis to `freshness-corroboration`.
4. Delegate usability and journey analysis to `engagement-audit`.
5. Aggregate findings from all three supporting skills.
6. Normalize and deduplicate findings.
7. Calculate final severity and confidence based on collected evidence.
8. Compose actionable recommendations for each finding.
9. Generate and output the final audit report JSON.

## Output
A fixed-schema JSON audit report containing a summary and an array of findings with evidence and suggested actions.

## Allowed Tools
- Default API tools for reading and writing files.
