# Module 16: Integration Testing

This document describes the end-to-end integration testing suite for the Agent Skill Marketplace.

## Overview

The integration testing suite validates that all independently developed modules and engines (crawler, parser, renderer, discoverability, freshness, engagement, findings, recommendations, and reporting) function together cohesively.

It removes all previous mocking (`unittest.mock`) and instead relies on a locally spun-up HTTP server serving deterministic, pre-configured HTML fixtures.

## Architecture

1. **Local Test Server (`tests/integration/server.py`)**: A `ThreadingHTTPServer` that serves responses based on requested paths.
2. **Deterministic Fixtures (`tests/integration/fixtures.py`)**: A dictionary defining HTML bodies, HTTP status codes, and headers for specific test paths (e.g., `/clean/`, `/issue-thin/`, `/malformed/`).
3. **End-to-End Test Suite (`tests/integration/test_end_to_end.py`)**: The `unittest` class that starts the server on port `8080`, issues actual requests via `audit-orchestrator`, and asserts on the resulting JSON/Markdown reports.

## Test Matrix Covered

The suite validates the complete 21-point requirement matrix:
- **Clean Sites**: Validates no false positives are reported when best practices are followed.
- **Single-Issue Sites**: Validates deterministic identification and recommendation generation for specific, isolated issues (e.g., Stale Content, Dead End Page, Thin Content, Missing Canonical URL).
- **Multi-Issue Sites**: Validates the orchestrator can cleanly deduplicate, prioritize, and structure findings when multiple issues exist concurrently.
- **Edge Cases**: Validates handling of empty sites, 404/500 network errors, and malformed HTML.
- **Robots.txt & Sitemap Compliance**: Ensures crawling strictly obeys local directives and flags conflicting instructions.
- **Schema Validation**: Ensures the resulting JSON matches the exact required Adobe Round 3 minimum schema.

## How to Run

To run the full suite including integration tests, ensure your current working directory is the project root, and execute:

```bash
$env:PYTHONPATH="."
python -m unittest tests.integration.test_end_to_end
```

## Maintenance

When adding new detection rules or modifying the reporting schema, ensure:
1. A new fixture is added to `fixtures.py` that triggers the rule.
2. A corresponding `test_single_issue_*` method is added to `test_end_to_end.py`.
3. The finding is mapped correctly in `src/recommendations/engine.py` to ensure it resolves to a specific suggested action.
