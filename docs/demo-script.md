# Demo Script: Brand AI Readiness Audit

## 0:00–0:20 — Problem
**Presenter:** "A website can rank normally for humans while remaining completely invisible or misunderstood by modern AI assistants. Even if users arrive, they often face stale facts or walls of unstructured text. Today we'll show you how an AI Agent can seamlessly audit these issues using our specialized Marketplace."

**Screen:** Display a quick slide or visual of the problem (humans happy vs. AI confused).

## 0:20–0:40 — Marketplace
**Presenter:** "This isn't a monolithic script. It's a reusable Agent Skill Marketplace. We have four distinct skills. Look at `marketplace.json`—an agent only needs to call the `audit-orchestrator` entrypoint, which dynamically coordinates the rest."

**Screen:** Open `marketplace.json` and highlight the four skills, pointing out the single entrypoint. 

## 0:40–1:00 — Input
**Presenter:** "Let's ask the agent to run an audit. We just provide a `start_url` for a test target."

**Screen:** Execute `python scripts/run_audit.py --url http://127.0.0.1:8080/multi/ --max-pages 5` in the terminal.

## 1:00–1:40 — Execution
**Presenter:** "The orchestrator is now working. First, the `crawl-render-audit` skill reads `robots.txt` safely and crawls the site, comparing raw HTML to JavaScript-rendered DOM. Next, the `freshness` and `engagement` skills run in parallel. They're checking for missing structured data, stale copyright years, and structural dead-ends."

**Screen:** Show the terminal logs printing out the concurrent crawling and analysis steps.

## 1:40–2:20 — Results
**Presenter:** "And it's done. The Findings Composer deduplicates everything and the Recommendation Engine maps each finding to a precise priority."

**Screen:** Open `audit_report.json`. Scroll directly to a strong finding, such as `Missing Canonical URL` or `Unstructured Wall of Text`. 

**Presenter:** "Notice the strict evidence extracted straight from the DOM, the deterministic severity score, and the highly actionable recommendation generated."

## 2:20–2:50 — Why it matters
**Presenter:** "Why does this matter? Because the skills are completely reusable. We've proven this generalizing across 12 different website archetypes. It's deterministic, read-only, perfectly safe, and operates entirely without live website modification. This is true composable AI auditing."

**Screen:** Switch to a summary slide showing "Generalization | Determinism | Safety" and end the demo.
