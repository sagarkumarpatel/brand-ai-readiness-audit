from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SuggestedAction:
    summary: str
    priority: str

@dataclass
class FinalFinding:
    id: str
    title: str
    severity: str
    evidence: List[str]
    suggested_action: SuggestedAction
    confidence: str = ""
    why_it_matters: str = ""
    affected_urls: List[str] = field(default_factory=list)

@dataclass
class ReportSummary:
    total_findings: int
    critical: int
    high: int
    medium: int
    low: int

@dataclass
class AuditReportData:
    site: str
    audited_at: str
    summary: ReportSummary
    findings: List[FinalFinding]
