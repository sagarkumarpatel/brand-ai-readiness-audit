from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.crawler.models import CrawlResponse

@dataclass
class Link:
    url: str
    anchor_text: str
    is_internal: bool

@dataclass
class Heading:
    level: int  # 1 for H1, 2 for H2, etc.
    text: str

@dataclass
class ParsedPage:
    url: str
    final_url: str
    status_code: int
    content_type: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    robots_directives: List[str] = field(default_factory=list)
    canonical_url: Optional[str] = None
    headings: List[Heading] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    visible_text: str = ""
    main_content: str = ""
    json_ld_blocks: List[str] = field(default_factory=list)
    open_graph: Dict[str, str] = field(default_factory=dict)
    page_type: str = "generic"
    parsing_warnings: List[str] = field(default_factory=list)
