from typing import List, Dict, Any
from datetime import datetime, timezone
from .models import AuditReportData, FinalFinding, SuggestedAction, ReportSummary

class ReportGenerator:
    SEVERITY_RANKS = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    PRIORITY_RANKS = {
        "CRITICAL": 0,
        "P0": 0,
        "HIGH": 1,
        "P1": 1,
        "MEDIUM": 2,
        "P2": 2,
        "LOW": 3,
        "P3": 3
    }

    @staticmethod
    def build_report(site: str, raw_findings: List[Dict[str, Any]], audited_at: str = None) -> AuditReportData:
        if not site:
            raise ValueError("Site URL is required")
        
        if not audited_at:
            audited_at = datetime.now(timezone.utc).isoformat()
            
        validated_findings = []
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for f in raw_findings:
            # Validate required fields
            required_keys = ["id", "title", "severity", "evidence", "suggested_action"]
            for key in required_keys:
                if key not in f:
                    raise ValueError(f"Finding missing required field: {key}")
                if not f[key]:
                    raise ValueError(f"Finding field cannot be empty: {key}")
                    
            severity = f["severity"].upper()
            if severity not in ReportGenerator.SEVERITY_RANKS:
                raise ValueError(f"Invalid severity: {severity}")
                
            action = f["suggested_action"]
            if not isinstance(action, dict):
                raise ValueError("suggested_action must be a dictionary")
                
            if "summary" not in action or "priority" not in action:
                raise ValueError("suggested_action must contain summary and priority")
                
            if not action["summary"] or not action["priority"]:
                raise ValueError("suggested_action summary and priority cannot be empty")
                
            priority = action["priority"].upper()
            if priority not in ReportGenerator.PRIORITY_RANKS:
                raise ValueError(f"Invalid priority: {priority}")

            if not isinstance(f["evidence"], list) or not f["evidence"]:
                raise ValueError("Evidence must be a non-empty list")
                
            counts[severity.lower()] += 1
            
            validated_findings.append(FinalFinding(
                id=str(f["id"]),
                title=str(f["title"]),
                severity=severity,
                evidence=f["evidence"],
                suggested_action=SuggestedAction(
                    summary=str(action["summary"]),
                    priority=priority
                ),
                confidence=f.get("confidence", ""),
                why_it_matters=f.get("why", ""), # Map "why" from Issue to "why_it_matters" if present
                affected_urls=f.get("affected_urls", [])
            ))
            
        # Sort deterministicly: Severity -> Priority -> ID
        validated_findings.sort(key=lambda x: (
            ReportGenerator.SEVERITY_RANKS[x.severity],
            ReportGenerator.PRIORITY_RANKS[x.suggested_action.priority],
            x.id
        ))

        summary = ReportSummary(
            total_findings=len(validated_findings),
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"]
        )
        
        return AuditReportData(
            site=site,
            audited_at=audited_at,
            summary=summary,
            findings=validated_findings
        )
