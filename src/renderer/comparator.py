from src.parser.models import ParsedPage
from .models import RenderResult, ComparisonResult

class PageComparator:
    def compare(self, parsed: ParsedPage, rendered: RenderResult) -> ComparisonResult:
        result = ComparisonResult()
        
        if not rendered.rendered_successfully:
            result.render_failed = True
            result.differences.append(f"Rendering failed: {rendered.error}")
            return result
            
        # Compare text length
        raw_text_len = len(parsed.visible_text)
        rendered_text_len = len(rendered.visible_text)
        
        if rendered_text_len > raw_text_len * 1.5 and rendered_text_len - raw_text_len > 500:
            result.js_dependent_content = True
            result.significant_content_change = True
            result.differences.append(f"Significant text added after rendering ({rendered_text_len} vs {raw_text_len} chars)")
            
        # Compare links
        raw_links_set = {link.url for link in parsed.links}
        rendered_links_set = {link.url for link in rendered.links}
        
        new_links = rendered_links_set - raw_links_set
        if len(new_links) > len(raw_links_set) * 0.5 and len(new_links) > 5:
            result.js_dependent_links = True
            result.differences.append(f"Significant number of links added after rendering ({len(new_links)} new links)")
            
        return result
