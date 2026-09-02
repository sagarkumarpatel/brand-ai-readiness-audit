# Testing Strategy

The testing strategy ensures generalization, safety, and correctness across diverse web architectures.

## Categories
1. **Unit Tests**: Test individual parsers, fact extraction logic, and severity calculations.
2. **Integration Tests**: Test the composition of skills and engines.
3. **Regression & Golden Tests**: Baseline outputs for known site mockups to prevent regressions.
4. **Adversarial Tests**:
   - Malformed HTML/JSON-LD
   - Hostile URLs (redirect loops, infinite graphs)
   - Extremely slow pages / timeouts
   - Huge payloads
5. **Generalization Tests**: Run the full audit against previously unseen websites spanning:
   - E-commerce
   - SaaS
   - University/Gov
   - Blogs/Portfolios
6. **Safety Tests**: Verify robots.txt compliance, read-only behavior, and rate limit adherence.

## False Positive Control
Optimize for low false positives. Tests will explicitly check that findings are not generated for missing *optional* features unless they demonstrably cause a problem.
