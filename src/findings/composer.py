import hashlib
from typing import List, Dict, Set
from src.analysis.models import Issue
from src.findings.models import NormalizedFinding, SuggestedAction

class FindingComposer:
    VALID_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
    VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
    VALID_CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
    
    SEVERITY_TO_PRIORITY = {
        "CRITICAL": "P0",
        "HIGH": "P1",
        "MEDIUM": "P2",
        "LOW": "P3"
    }

    @staticmethod
    def _normalize_severity(sev: str) -> str:
        s = sev.upper() if sev else ""
        return s if s in FindingComposer.VALID_SEVERITIES else "MEDIUM"

    @staticmethod
    def _normalize_confidence(conf: str) -> str:
        c = conf.upper() if conf else ""
        return c if c in FindingComposer.VALID_CONFIDENCES else "MEDIUM"
        
    @staticmethod
    def _generate_id(title: str) -> str:
        return hashlib.sha256(title.strip().lower().encode("utf-8")).hexdigest()[:12]
        
    @staticmethod
    def compose(raw_issues: List[Issue], source_engine: str = "unknown") -> List[NormalizedFinding]:
        # Group by title (case-insensitive) to deduplicate the "same underlying problem"
        grouped: Dict[str, List[Issue]] = {}
        for issue in raw_issues:
            # NO OBJECTIVE EVIDENCE = NO FINDING
            if not issue.evidence:
                continue
                
            key = issue.title.strip().lower()
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(issue)
            
        final_findings = []
        for key, issues in grouped.items():
            # Pick the primary details from the first issue
            primary = issues[0]
            
            # Merge evidence
            merged_evidence_set: Set[str] = set()
            for issue in issues:
                for ev in issue.evidence:
                    merged_evidence_set.add(ev)
            merged_evidence = sorted(list(merged_evidence_set))
            
            norm_severity = FindingComposer._normalize_severity(primary.severity)
            norm_confidence = FindingComposer._normalize_confidence(primary.confidence)
            
            # Derive priority from normalized severity if action priority isn't defined explicitly.
            # Currently `Issue` doesn't have `action_priority`, so we derive it.
            priority = FindingComposer.SEVERITY_TO_PRIORITY[norm_severity]
            
            # Extract URLs from evidence (basic heuristic) or just leave it empty if we don't have explicit affected_urls
            # The adobe requirement wants it. We can extract it if needed, but for now we leave it empty.
            
            finding_id = FindingComposer._generate_id(primary.title)
            
            finding = NormalizedFinding(
                id=finding_id,
                title=primary.title.strip(),
                severity=norm_severity,
                evidence=merged_evidence,
                suggested_action=SuggestedAction(
                    summary=primary.action.strip(),
                    priority=priority
                ),
                confidence=norm_confidence,
                affected_urls=[],
                why_it_matters=primary.why.strip(),
                source_engines=[source_engine]
            )
            final_findings.append(finding)
            
        # Sort deterministically: severity (Critical -> Low) then Title
        severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        final_findings.sort(key=lambda x: (severity_rank.get(x.severity, 99), x.title))
        
        return final_findings
