---
name: audit-orchestrator
description: Entrypoint skill that orchestrates the AI readiness audit, coordinates supporting skills, and emits the final consolidated report.
license: UNLICENSED
---

# Audit Orchestrator

## When to use
Use this skill as the primary and ONLY entrypoint when requested to perform a brand AI readiness audit on a given website. This skill handles the composition of the underlying analysis engines (Discoverability, Freshness, Engagement).

## Inputs
Provide the target website URL.

## Procedure
1. Execute `scripts/audit-orchestrator.py --url <URL>`.
2. The orchestrator will:
   - Perform a single crawl of the target URL.
   - Run the Discoverability analysis (`crawl-render-audit` scope).
   - Run the Freshness analysis (`freshness-corroboration` scope).
   - Run the Engagement analysis (`engagement-audit` scope).
   - Pass all findings through the Finding Composer for deduplication and normalization.
   - Attach actionable recommendations via the Recommendation Engine.
   - Generate a JSON report matching the minimum Adobe schema.
3. Read the output from `audit_report.json`.

## Output
A deterministic, fixed-schema JSON audit report containing:
- `site`: The audited URL.
- `audited_at`: ISO 8601 timestamp.
- `summary`: Object with counts (total, critical, high, medium, low).
- `findings`: Array of findings with `id`, `title`, `severity`, `evidence`, and `suggested_action` (`summary`, `priority`).

## Allowed Tools
- `run_command` (to execute the python orchestration script)
- `view_file` (to view the generated report)
