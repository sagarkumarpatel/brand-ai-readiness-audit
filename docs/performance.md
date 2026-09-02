# Performance

The typical audit must complete in **less than 5 minutes**.

## Optimization Strategies
1. **Bounded Crawling**: Enforce strict limits on `max_pages` (e.g., 50 by default) and `max_depth`.
2. **URL Deduplication**: Prevent redundant fetching.
3. **Selective Rendering**: Do not launch a headless browser for every page. Render only when raw HTML heuristics suggest a heavy JS framework or missing content.
4. **Concurrency**: Fetch and analyze independent pages concurrently using asynchronous I/O.
5. **Early Stopping**: If the time budget (e.g., 4m 30s) is approaching, gracefully halt further crawling and begin report generation.
6. **Caching**: Cache HTTP responses locally during the audit to prevent re-fetching.

## Telemetry
Record the following metrics in the final report metadata:
- `crawl_time`
- `render_time`
- `analysis_time`
- `fact_resolution_time`
- `finding_generation_time`
- `report_generation_time`
- `total_time`
