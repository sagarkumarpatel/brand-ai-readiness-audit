from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SuggestedAction:
    summary: str
    priority: str

@dataclass
class NormalizedFinding:
    id: str
    title: str
    severity: str
    evidence: List[str]
    suggested_action: SuggestedAction
    
    # Internal metadata
    confidence: str
    affected_urls: List[str]
    why_it_matters: str
    source_engines: List[str]
