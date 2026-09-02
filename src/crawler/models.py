from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class CrawlConfig:
    max_pages: int = 50
    max_depth: int = 3
    timeout_seconds: int = 10
    max_redirects: int = 5
    max_response_size_bytes: int = 5 * 1024 * 1024 # 5 MB
    user_agent: str = "BrandAIReadinessAuditBot/1.0"
    allowed_domains: List[str] = field(default_factory=list)

@dataclass
class CrawlResponse:
    url: str
    status_code: int
    headers: Dict[str, str]
    content_type: str
    html: str
    redirect_chain: List[str]
    depth: int
    parent_url: Optional[str]
    timing_ms: float
    error: Optional[str] = None
