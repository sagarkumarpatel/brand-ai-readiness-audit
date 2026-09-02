---
name: crawl-render-audit
description: Provides crawling, raw HTML analysis, and optional rendered-DOM comparison for JavaScript-dependent pages to detect missing metadata and crawl barriers.
---

# Crawl & Render Audit Skill

Use this skill to deterministically audit a website's structural AI readiness (discoverability) without relying on arbitrary LLM judgements.

## Inputs
- `start_url` (string, required): The target domain/website to audit. Must include protocol (e.g., `https://example.com`).

## Allowed Tools
- `run_command`: To execute the deterministic python script.
- `view_file`: To view the generated JSON report.

## Procedure
1. Execute the orchestration script against the target URL:
   ```bash
   python skills/crawl-render-audit/scripts/run_audit.py --start-url <start_url>
   ```
2. Wait for the script to finish. The script respects read-only limits, timeouts, and `robots.txt` automatically.
3. Read the output file `audit_report.json` generated in the current directory.
4. Integrate the JSON findings (issues, severities, evidence) into your final response.

## Output Format
The `audit_report.json` contains a structured list of issues containing:
- `title`: Short name of the issue.
- `severity`: CRITICAL, HIGH, MEDIUM, or LOW.
- `confidence`: HIGH, MEDIUM, or LOW.
- `evidence`: Concrete proof of the finding.
- `why`: The impact on AI discoverability.
- `action`: Recommended fix.
