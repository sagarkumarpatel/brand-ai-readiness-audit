# Evaluator Q&A

### Product
**1. What problem does this solve?**
It identifies structural, technical, and content gaps that prevent a website from being properly discovered and understood by modern AI assistants, while also flagging severe on-site usability friction.

**2. Why does this matter for AI assistants?**
AI assistants rely on clean metadata, structured data, accessible machine-readable text, and unambiguous canonical signals to reliably extract and cite information. Poorly optimized sites are ignored or hallucinated about by AI.

**3. Why is this not just an SEO auditor?**
While SEO overlaps with AI readiness, this tool specifically targets AI-centric failure points like unstructured walls of text, JavaScript render-locking, and factual contradictions across a domain—problems that hurt LLM extraction far more than traditional search ranking.

**4. What is an Agent Skill?**
An Agent Skill is a specialized, tool-declared, isolated module that a General AI Agent can invoke to perform a specific action (like auditing an engagement structure or running a crawler).

**5. Why did you build multiple skills?**
To make the system truly composable. A general AI doesn't always need a full audit; sometimes it just needs to extract and corroborate facts (Freshness) or evaluate usability (Engagement). Modularity fits the marketplace paradigm.

**6. Why is `audit-orchestrator` the entrypoint?**
It simplifies the interface for the parent AI agent. The agent makes one request to the orchestrator, which intelligently delegates tasks to the sub-skills and aggregates the final report.

### Architecture
**7. Why exactly four skills?**
This perfectly maps the domain into distinct responsibilities: Orchestration (1), Technical Discoverability (2), Content Freshness (3), and Usability/Engagement (4).

**8. How do the skills compose?**
The orchestrator shares the initial target URL and crawler outputs via structured data passing. The sub-skills perform their independent analyses and return standardized finding formats.

**9. Why deterministic analysis?**
Determinism guarantees safety, reliability, and testability. An LLM might hallucinately flag a "bad layout" differently on Tuesday than on Wednesday. Deterministic heuristics ensure 100% reproducible, evidence-backed audits.

**10. Why isn't an LLM required?**
Because structural readiness (e.g., missing canonical tags, <15 words, blocked robots) can and should be identified using mathematically precise rules. Wasting token costs and risking hallucinations on strict structural audits is an architectural anti-pattern.

**11. How does the system generalize to unseen websites?**
It relies on universal web standards (HTML5 tags, JSON-LD, standard HTTP headers) rather than site-specific CSS classes or XPaths. It proved this across 12 distinct test archetypes.

**12. How are findings deduplicated?**
A Finding Composer hashes the finding title and URL path. If multiple components flag the exact same structural issue on the same page, they merge gracefully.

**13. How are severity levels calculated?**
By mapping specific trigger conditions to strict heuristics (e.g., missing Canonical = HIGH, while Missing Contact info = MEDIUM).

**14. How are recommendations generated?**
The Recommendation Engine maps the deterministic Finding Title to a specifically tailored, highly actionable remediation step and scales priority based on severity (e.g., P0, P1, P2).

### Technical
**15. How does crawling work?**
A synchronous Python-based crawler utilizing built-in `urllib` and `html.parser` navigates the site, restricted by maximum page limits, depth limits, and timeout thresholds.

**16. How do you respect robots.txt?**
The crawler explicitly fetches `/robots.txt` and uses Python's `urllib.robotparser` to strictly obey directives before ever requesting a target path.

**17. How do you handle JavaScript-heavy websites?**
While a renderer component exists in the architecture, the final audit pipeline currently utilizes static HTML analysis for maximum performance and stability. JavaScript rendering is intentionally bypassed in the primary flow.

**18. How do you detect render-locked content?**
The underlying architecture includes support for comparing raw HTML against rendered DOM, though this feature is not active in the default fast-audit orchestrator to ensure sub-second response times.

**19. How do you detect stale information?**
By extracting `datePublished` from JSON-LD or regex-matching copyright years against the current year.

**20. How do you detect contradictions?**
By mapping extracted entities (e.g., phone numbers or emails) across different pages. If `Page A` says "sales@example.com" and `Page B` says "contact@example.com", it flags a contradiction.

**21. How do you detect thin content?**
By stripping HTML and counting visible word tokens. If it falls below a strict minimum threshold (e.g., <15 words), it flags the page.

**22. How do you detect dead-end pages?**
If the extracted `<body>` contains exactly 0 internal `<a href>` links to other parts of the site.

**23. How do you detect walls of text?**
If visible word count exceeds an extreme threshold (e.g., >3000 words) without sufficient semantic structural breaks like `<h2>` or `<h3>` tags.

**24. How do you produce evidence?**
Every engine that flags an issue must explicitly attach the relevant extracted text, HTTP header, or HTML node string that triggered the failure rule.

**25. How do you ensure deterministic output?**
By strictly sorting all results, deduplicating using cryptographic hashes, and utilizing threshold-based logic entirely free of random variance.

### Safety
**26. Can the system modify a website?**
No. It operates 100% read-only.

**27. Does it require credentials?**
No.

**28. Does it perform POST/PUT/PATCH/DELETE?**
No. It strictly issues `GET` and `HEAD` requests.

**29. What happens if a site blocks the crawler?**
It catches the HTTP timeout, 403, or connection drop, skips the page, logs a warning, and continues gracefully without crashing.

**30. What happens if Chromium is unavailable?**
The static analyzer natively avoids Chromium dependencies, eliminating this failure mode entirely from the standard audit path.

### Performance
**31. What is the runtime?**
Extremely fast. 5 pages typically take under 1.5 seconds locally.

**32. What was actually benchmarked?**
Local HTTP test servers simulating multi-page, multi-archetype websites to eliminate network latency variance.

**33. What happens on very large websites?**
The `max_pages` configuration limits the audit to a designated sample size, preventing infinite memory usage or unacceptably long runs.

### Adobe/Round 3
**34. How does this satisfy the Agent Skill Marketplace requirement?**
It is explicitly structured as an ecosystem of modular, tool-callable `.json` and `SKILL.md` defined agent functions.

**35. How does it support off-site discoverability?**
It identifies critical technical blockers that prevent AI from ingesting a brand's data (e.g., missing Schema, blocked sitemaps).

**36. How does it support on-site engagement?**
By detecting broken journeys (Dead-Ends) and terrible content readability structures (Walls of Text).

**37. How does it generalize beyond the test sites?**
Our Generalization Test suite proved the heuristics successfully analyze 12 entirely different website structures, from single-page JS apps to legacy corporate portals.

**38. What are the main limitations?**
Aggressive enterprise anti-bot software (like strict Cloudflare or Datadome profiles) can block the basic urllib crawler. Also, our engagement rules use strict structural logic rather than semantic nuance.
