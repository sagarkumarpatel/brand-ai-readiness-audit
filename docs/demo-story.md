# Demo Story: Brand AI Readiness Audit

## Problem
A website can exist and rank normally for humans while still being completely invisible, misunderstood, or unparseable for modern AI assistants. At the same time, users who reach the site may encounter stale information, broken navigation journeys, thin pages, or massive walls of unstructured text. These issues damage brand trust and significantly harm AI discoverability. 

## Solution
We built an **Agent Skill Marketplace** that converts these critical concerns into specialized, reusable Agent Skills. Instead of hardcoding a monolithic audit script, a General AI Agent can invoke our orchestration skill, which dynamically coordinates a suite of specialist skills to analyze discoverability, rendering, freshness, and engagement.

## Architecture
The process is entirely composable:

```text
General AI Agent
       ↓
Entrypoint Skill (audit-orchestrator)
       ↓
Supporting Skills (crawl, freshness, engagement)
       ↓
Analysis Engines
       ↓
Evidence Collection
       ↓
Severity Calculation
       ↓
Recommendation Mapping
       ↓
Final Audit Report
```

## Demo
We will demonstrate the Marketplace auditing a live target URL (e.g., a test server or a simple, standard target site). 
1. We will supply the agent with a `start_url`.
2. The orchestrator will invoke the `crawl-render-audit` skill to extract raw and rendered content, verifying `robots.txt` compliance.
3. The `freshness-corroboration` and `engagement-audit` skills will simultaneously analyze the extracted DOM to locate structural friction and outdated facts.
4. The system will composite these into actionable, deduplicated findings mapped to exact severity scores and targeted recommendations. 
5. The result will be a pristine JSON report produced safely in under 3 seconds.
