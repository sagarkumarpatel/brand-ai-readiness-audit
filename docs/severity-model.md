# Severity Model

Severity indicates the impact of a finding on AI discoverability or user engagement.

## Levels
1. **CRITICAL**: Issues that completely block AI crawlers or users from accessing core content (e.g., site-wide robots.txt block, completely broken main navigation, raw HTML is entirely empty).
2. **HIGH**: Issues that significantly hinder understanding or trust (e.g., strong contradictions in pricing, missing structured data for key products, render-locked primary content).
3. **MEDIUM**: Issues that cause friction but don't entirely break the experience (e.g., excessive redirect chains, some stale secondary content).
4. **LOW**: Minor deviations from best practices (e.g., missing optional meta tags).

## Determining Factors
- **Impact**: Does this prevent discovery/engagement, or just add friction?
- **Scope**: Number of affected pages (site-wide vs isolated).
- **Business Significance**: Is this a core product page or a legal disclaimer?
- **Confidence**: If confidence is low, severity should typically be bounded.

Do not escalate severity solely because a rule failed. Assess the practical impact on a generic web entity.
