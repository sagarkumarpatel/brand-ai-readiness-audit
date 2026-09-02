from dataclasses import dataclass, field
from typing import List, Optional
from src.parser.models import ParsedPage, Link

@dataclass
class RenderResult:
    requested_url: str
    final_url: str
    status_code: Optional[int]
    rendered_successfully: bool
    html: str
    visible_text: str = ""
    links: List[Link] = field(default_factory=list)
    timing_ms: float = 0.0
    error: Optional[str] = None

@dataclass
class ComparisonResult:
    js_dependent_content: bool = False
    js_dependent_links: bool = False
    js_dependent_metadata: bool = False
    significant_content_change: bool = False
    render_failed: bool = False
    differences: List[str] = field(default_factory=list)
