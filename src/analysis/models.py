from dataclasses import dataclass, field
from typing import List

@dataclass
class Issue:
    title: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    confidence: str # HIGH, MEDIUM, LOW
    evidence: List[str]
    why: str
    action: str

@dataclass
class AuditReport:
    issues: List[Issue] = field(default_factory=list)
    
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
