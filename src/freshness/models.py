from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class FactType(Enum):
    BRAND_NAME = "brand_name"
    PHONE = "phone"
    EMAIL = "email"
    DATE = "date"
    COPYRIGHT_YEAR = "copyright_year"
    PRODUCT = "product"
    ADDRESS = "address"

class ResolutionState(Enum):
    RESOLVED = "resolved"
    PROBABLE = "probable"
    UNRESOLVED = "unresolved"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"

@dataclass
class FactSource:
    url: str
    location: str  # e.g., 'json-ld', 'visible_text', 'meta'
    context: str   # Snippet or exact match context

@dataclass
class Fact:
    type: FactType
    value: str
    source: FactSource
    timestamp: Optional[str] = None

@dataclass
class FactResolution:
    fact_type: FactType
    primary_value: Optional[str]
    state: ResolutionState
    corroborating_sources: List[FactSource]
    contradicting_sources: List[FactSource]
    all_values: List[str]  # Distinct values observed
