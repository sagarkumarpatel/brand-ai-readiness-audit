from typing import List, Dict
from src.parser.models import ParsedPage
from src.analysis.models import Issue

class EngagementAnalyzer:
    @staticmethod
    def analyze(parsed_pages: Dict[str, ParsedPage]) -> List[Issue]:
        issues = []
        
        # We need to know what the homepage is to avoid flagging it as a dead-end if it's genuinely 1-page.
        # But generally, a 1-page site has 0 internal links. That's a valid 1-page site.
        # We flag dead-ends only for pages that are NOT the single root page of the site.
        # Let's find the shortest URL to act as the root.
        if not parsed_pages:
            return issues
            
        root_url = min(parsed_pages.keys(), key=len)

        for url, page in parsed_pages.items():
            if page.status_code != 200:
                continue
                
            is_root = (url == root_url)
            
            # 1. Thin / Blank Content
            # Less than 15 words and no media (we use a simple proxy for media: no links/json_ld/etc, 
            # but visible text is the main driver here)
            word_count = len(page.visible_text.split())
            if word_count < 15 and not page.json_ld_blocks:
                issues.append(Issue(
                    title="Thin Content",
                    severity="HIGH",
                    confidence="HIGH",
                    evidence=[f"Page '{url}' contains only {word_count} words and lacks structured content."],
                    why="Pages with extremely sparse text provide almost no value to visitors or AI assistants, causing immediate bounces or drops in engagement.",
                    action="Flesh out the page with meaningful content, or remove/redirect it if it is unnecessary."
                ))
                continue # No need to analyze thin pages for walls of text or dead ends
                
            # 2. Dead End / Orphan-like
            # If a page is not the root, and has 0 internal links (excluding itself/homepage)
            internal_links = [l for l in page.links if l.is_internal]
            
            if not is_root and len(internal_links) == 0:
                issues.append(Issue(
                    title="Dead End Page",
                    severity="HIGH",
                    confidence="HIGH",
                    evidence=[f"Page '{url}' contains 0 internal navigation links."],
                    why="Visitors landing on this page have no clear path forward into the rest of the website.",
                    action="Add contextual internal links or a global navigation menu to guide users."
                ))
                
            # 3. Wall of Text
            # > 3000 words without a single heading
            if word_count > 3000 and len(page.headings) == 0:
                issues.append(Issue(
                    title="Unstructured Wall of Text",
                    severity="MEDIUM",
                    confidence="HIGH",
                    evidence=[f"Page '{url}' contains {word_count} words but 0 heading tags (H1/H2/H3)."],
                    why="Extremely long content without structural segmentation is difficult for humans to scan, increasing bounce rates.",
                    action="Break up the content using semantic headings (H2, H3) to improve readability and AI comprehension."
                ))

        return issues
