# Brand AI Readiness Audit System

## Overview
This Agent Skill Marketplace is a production-quality, generic, website-agnostic system designed to audit any public website for problems affecting:
1. **Off-site AI discoverability**: Getting found and cited by AI assistants.
2. **On-site engagement**: Keeping visitors engaged once they arrive.

The system operates strictly in a read-only, safe, and deterministic manner, never modifying website state, bypassing authentication, or violating robots.txt.

## Marketplace Architecture
The marketplace consists of exactly four specialized Agent Skills:

### 1. `audit-orchestrator` (ENTRYPOINT)
The sole designated entrypoint for the marketplace. It receives the audit request, coordinates the supporting skills, aggregates their findings, deduplicates issues, calculates severities, and generates the final JSON audit report.

### 2. `crawl-render-audit`
Responsible for safe crawling and selective rendering of website pages. Analyzes raw HTML vs. rendered DOM, extracts structured data, evaluates internal links, and identifies technical and rendering gaps hurting discoverability.

### 3. `freshness-corroboration`
Analyzes facts extracted from the website for consistency, temporal relevance (freshness), and corroboration across different pages. Detects contradictions and stale claims using deterministic evidence weighting.

### 4. `engagement-audit`
Evaluates observable usability and engagement risks. Inspects navigation, information hierarchy, and content clarity to detect broken journeys and friction signals.

## Input & Output Concept
- **Input**: The audit request requires at least a target `"site"` URL.
- **Output**: The system emits a structured JSON report containing a summary and a list of evidence-backed findings. Every finding includes a severity level and actionable, prioritized recommendations.
