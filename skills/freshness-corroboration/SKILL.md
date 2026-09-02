---
name: freshness-corroboration
description: A deterministic Agent Skill to detect fact contradictions and objectively stale content on a website.
---

# Freshness & Corroboration Skill

This skill analyzes a website to detect structural contradictions in objective facts (like conflicting phone numbers or emails) and demonstrably stale content (e.g. copyright dates older than the current year).

## Inputs
- `start_url` (string): The base URL of the website to audit (e.g. `https://example.com`).

## Tools Allowed
- `run_command` (to execute the orchestration script).
- `view_file` (to view the output `freshness_report.json`).

## Execution Procedure

1.  **Run the orchestrator**: Execute the python script to run the crawler, parser, and freshness analysis engine.
    ```bash
    python skills/freshness-corroboration/scripts/run_freshness.py --url <start_url>
    ```
2.  **Review the output**: View the generated `freshness_report.json` file.
    ```bash
    cat freshness_report.json # Or use view_file
    ```
3.  **Produce the final finding**: Use the contents of `freshness_report.json` to construct evidence-backed recommendations for the user. Do not invent any findings not present in the JSON report.

## Evidence Rules
- **No LLM usage:** This skill relies strictly on the deterministic heuristics in `src/freshness`.
- **Evidence-first:** Every finding MUST be backed by multiple conflicting sources (for contradictions) or specific extracted dates (for staleness).
- **Conservative Resolution:** Single-source facts are logged as PROBABLE, not Contradictory. Missing facts are treated as INSUFFICIENT_EVIDENCE, not as errors.
