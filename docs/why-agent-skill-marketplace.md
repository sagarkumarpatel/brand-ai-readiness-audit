# Why This is a True Agent Skill Marketplace

A major requirement of Adobe Hackathon Round 3 is to build an **Agent Skill Marketplace**. 

It is easy to misunderstand this requirement and simply build a monolithic, standard Python script that spits out a website audit. We explicitly avoided that anti-pattern. 

## The Old Way: Monolithic Auditor
In a traditional approach, an application takes a URL, runs a massive hardcoded loop to fetch data, parse it, and generate a report.
```text
URL → Monolithic Audit Program → Report
```
The problem? If an AI Agent only wants to extract specific contact facts from a page, it cannot do so without triggering the entire heavy rendering pipeline. 

## The Agent Skill Marketplace Paradigm
Our system flips this model. We built a suite of independent, composable **Agent Skills**. 

```text
General AI Agent
       ↓
Marketplace
       ↓
Entry Skill (audit-orchestrator)
       ↓
Composable Specialist Skills
       ↓
Evidence + Analysis
       ↓
Recommendations
       ↓
Report
```

### The Composable Skills
The important unit in our architecture is not the website audit itself. **The important unit is the reusable skill.**

1. **`audit-orchestrator`**: Acts as the marketplace entrypoint. A general AI agent calls this single skill.
2. **`crawl-render-audit`**: A specialized skill exclusively dealing with technical discoverability and extracting raw vs. JavaScript-rendered content.
3. **`freshness-corroboration`**: A specialized skill determining whether important facts are current, and structurally consistent across multiple pages.
4. **`engagement-audit`**: A specialized skill purely identifying structural usability problems that prevent human and AI agents from navigating properly.

These same skills can be invoked by a general-purpose AI agent independently against different websites without rewriting the audit logic. 

### Why this satisfies the spirit of a Marketplace
- **Reusable**: Each skill has strict inputs and outputs defined by a `SKILL.md` contract.
- **Composable**: The orchestrator ties them together dynamically.
- **Independently Scoped**: A freshness bug will never crash the crawling skill. 
- **Deterministic**: Standardized outputs guarantee reliability.
- **Provider-Neutral**: Built on vanilla Python without being locked into a proprietary LLM API.
- **One Entrypoint**: `marketplace.json` cleanly routes external agents to the single `audit-orchestrator`.

We provide the tools. The AI Agent decides how to use them.
