# AI Website Readiness Audit

## Site
https://www.example.com

## Audit Time
2026-09-02T17:04:43.728981+00:00

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |
| Total | 1 |

## Findings

### 1. Missing Canonical URL

**Severity:** LOW

**Evidence:**
- URL https://www.example.com lacks a <link rel='canonical'> tag.

**Why it matters:**
AI systems need canonical tags to merge duplicate content correctly and attribute facts to the right source.

**Suggested action:**
Add a self-referencing canonical URL to the page and ensure it points to the preferred indexable URL.

**Priority:** P3