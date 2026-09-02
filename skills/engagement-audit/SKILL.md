---
name: engagement-audit
description: Evaluates observable on-site engagement risks such as weak navigation and poor information clarity.
license: UNLICENSED
---

# Engagement Audit

## When to use
Invoked by the `audit-orchestrator` to analyze website structure and layout to identify friction points that hinder visitor engagement.

## Inputs
Parsed DOM structures, link graphs, and content hierarchies from the crawled pages.

## Procedure
1. Analyze the main navigation structure and internal linking paths.
2. Evaluate heading hierarchies and structural tags for information clarity.
3. Detect dead-end pages or pages lacking clear calls to action.
4. Identify broken user journeys and client-side usability dependencies.
5. Filter out subjective issues and keep only observable, evidence-backed friction signals.
6. Generate findings for engagement barriers.

## Output
A list of preliminary engagement findings, each containing observable evidence (e.g., broken link targets, missing semantic tags).

## Allowed Tools
- Default API tools for structural and heuristic analysis.
