# Brand AI Readiness Audit: Agent Skill Marketplace

## The Problem
A website can rank normally for humans while remaining completely invisible, poorly represented, or misunderstood by modern AI assistants. Even when users reach the site, they often encounter stale information, broken journeys, or massive walls of unstructured text that frustrate both human readers and AI parsers. 

## The Solution
We built an **Agent Skill Marketplace**—a suite of composable, reusable Agent Skills that a general AI agent can invoke to audit any arbitrary website for AI readiness. This is not a monolithic script, but a modular ecosystem of specialized skills determining technical discoverability, rendering capability, content freshness, and on-site engagement.

## Architecture & Agent Skill Marketplace
This project implements a true **Agent Skill Marketplace**. 

Instead of a monolithic program, a General AI Agent can seamlessly plug into our `audit-orchestrator` entrypoint skill, which invokes highly specialized, independent supporting skills.

```text
General AI Agent
       |
       v
audit-orchestrator
       |
       +---- crawl-render-audit
       |
       +---- freshness-corroboration
       |
       +---- engagement-audit
       |
       v
Finding Composer
       |
       v
Recommendation Engine
       |
       v
Final Audit Report
```

### The 4 Skills:
1. **`audit-orchestrator` (Entrypoint)**: Receives the audit request and orchestrates specialized supporting skills to produce a final, deduplicated, and prioritized JSON audit report.
2. **`crawl-render-audit`**: Safely crawls websites respecting `robots.txt`, executes fast HTML parsing, and identifies critical technical/structural discoverability issues (e.g., missing canonical tags, blocked sitemaps, missing structured data).
3. **`freshness-corroboration`**: Deterministically analyzes temporal data (e.g., copyright years, `datePublished`) to ensure content is fresh and contact information is internally consistent across pages.
4. **`engagement-audit`**: Checks the site's structural engagement signals (identifying "Thin Content", "Dead-End Pages", and unstructured "Walls of Text").

## Default vs Optional Rendering Architecture
The system is explicitly designed for speed, determinism, and minimal dependencies in its default state, while preserving advanced rendering capabilities when needed.

### Default Audit
- Uses static/read-only HTML analysis
- Built entirely on the Python standard library (`urllib`, `html.parser`)
- Extremely fast and deterministic
- No browser dependency required
- Bypasses JavaScript rendering completely

### Optional Rendered Audit
- Uses Playwright when available
- Useful for JavaScript-heavy Single Page Applications (SPAs)
- Compares raw static HTML with the final rendered DOM
- Helps identify critical content or navigation locked behind JS rendering
- Remains entirely read-only (no website modification)

## Setup & Invocation

### Prerequisites
- Python 3.9+
- Optional: Playwright (only if using the optional rendered-DOM comparison)

### Installation
The default static audit is built entirely using Python's standard library (`urllib`, `html.parser`, `json`, etc.) and requires **no third-party packages**.
```bash
# Clone the repository (or extract the zip)
# No pip install required for the default static audit
```

### Running the Audit
You can invoke the marketplace orchestrator skill using the provided wrapper script:
```bash
python scripts/audit-orchestrator.py --url https://example.com --max-pages 5
```

### Output
The system generates a deterministic, schema-validated JSON report (`audit_report.json`) detailing the findings, their exact evidence, their calculated severities (CRITICAL/HIGH/MEDIUM/LOW), and precise, actionable recommendations.

## Evidence-Backed Analysis
Every finding produced by this system is rooted in strict, observable DOM evidence. The audit does not hallucinate problems; if it flags a missing canonical tag, it explicitly documents the missing tag in the `evidence` field. 

## Safety
- **Read-Only**: The agent operates exclusively via safe `GET` and `HEAD` requests. It never performs `POST`, `PUT`, `PATCH`, or `DELETE`.
- **Robots-Aware**: Strictly adheres to `robots.txt` rules and `<meta name="robots">` tags.
- **No Website Modification**: Will not alter live databases or server state.
- **No Authentication Required**: Tests publicly accessible URLs safely.

## Performance (Measured Benchmarks)
Our lightweight, synchronous engine is incredibly fast. Benchmarks measured locally:
- **5 pages**: ~0.70 seconds
- **25 pages**: ~3.12 seconds
- **100 pages**: ~12.54 seconds

## Testing
This marketplace was rigorously validated for scale and generalization:
- **125 Total Tests**: 100% passing across Unit, Integration, Performance, Adversarial, and Generalization suites.
- **12 Website Archetypes**: Proven to generalize safely across minimal sites, massive corporate portals, JS-heavy SPAs, and defective architectures.
- **Adversarial Resiliency**: Protected against recursive loops, infinite redirects, network hangs, and malformed HTML.

## Limitations
- **Anti-Bot Systems**: Target websites utilizing aggressive anti-bot protection (e.g., strict Cloudflare rules) may block the `urllib` crawler or the optional Playwright rendering engine.
- **Deterministic Heuristics**: The engagement metrics utilize strict deterministic thresholds (e.g., thin content < 15 words) rather than slower, non-deterministic LLM-based semantic analysis.
