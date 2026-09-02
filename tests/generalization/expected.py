import hashlib

def _gen_id(title):
    return hashlib.sha256(title.strip().lower().encode("utf-8")).hexdigest()[:12]

class ExpectedFindings:
    STALE_CONTENT = _gen_id("Stale Content")
    MISSING_BRAND_IDENTITY = _gen_id("Missing Brand Identity")
    THIN_CONTENT = _gen_id("Thin Content")
    DEAD_END_PAGE = _gen_id("Dead End Page")
    WALL_OF_TEXT = _gen_id("Unstructured Wall of Text")
    UNREACHABLE_PAGE = _gen_id("Unreachable Important Page")
    SITEMAP_BLOCKED = _gen_id("Sitemap Page Blocked by Robots.txt")
    EXCESSIVE_REDIRECT_CHAIN = _gen_id("Excessive Redirect Chain")
    MISSING_CANONICAL = _gen_id("Missing Canonical URL")
    MISSING_STRUCTURED_DATA = _gen_id("Missing Structured Data")
    RENDER_LOCKED_CONTENT = _gen_id("Render-locked Content")
    RENDER_LOCKED_NAV = _gen_id("Render-locked Navigation")

