import json
from .models import AuditReportData

class ReportSerializer:
    @staticmethod
    def to_json(report: AuditReportData) -> str:
        # Convert dataclass to dict cleanly
        data = {
            "site": report.site,
            "audited_at": report.audited_at,
            "summary": {
                "total_findings": report.summary.total_findings,
                "critical": report.summary.critical,
                "high": report.summary.high,
                "medium": report.summary.medium,
                "low": report.summary.low
            },
            "findings": []
        }
        
        for f in report.findings:
            finding_data = {
                "id": f.id,
                "title": f.title,
                "severity": f.severity,
                "evidence": f.evidence,
                "suggested_action": {
                    "summary": f.suggested_action.summary,
                    "priority": f.suggested_action.priority
                }
            }
            # Add metadata if present (these are optional in the prompt but allowed)
            if f.confidence:
                finding_data["confidence"] = f.confidence
            if f.why_it_matters:
                finding_data["why_it_matters"] = f.why_it_matters
            if f.affected_urls:
                finding_data["affected_urls"] = f.affected_urls
                
            data["findings"].append(finding_data)
            
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def to_markdown(report: AuditReportData) -> str:
        lines = []
        lines.append("# AI Website Readiness Audit")
        lines.append("")
        lines.append("## Site")
        lines.append(report.site)
        lines.append("")
        lines.append("## Audit Time")
        lines.append(report.audited_at)
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append("| Severity | Count |")
        lines.append("|----------|-------|")
        lines.append(f"| Critical | {report.summary.critical} |")
        lines.append(f"| High | {report.summary.high} |")
        lines.append(f"| Medium | {report.summary.medium} |")
        lines.append(f"| Low | {report.summary.low} |")
        lines.append(f"| Total | {report.summary.total_findings} |")
        lines.append("")
        
        if report.findings:
            lines.append("## Findings")
            lines.append("")
            
            for idx, f in enumerate(report.findings, start=1):
                lines.append(f"### {idx}. {f.title}")
                lines.append("")
                lines.append(f"**Severity:** {f.severity.upper()}")
                lines.append("")
                lines.append("**Evidence:**")
                for ev in f.evidence:
                    lines.append(f"- {ev}")
                lines.append("")
                
                if f.why_it_matters:
                    lines.append("**Why it matters:**")
                    lines.append(f.why_it_matters)
                    lines.append("")
                    
                lines.append("**Suggested action:**")
                lines.append(f.suggested_action.summary)
                lines.append("")
                lines.append(f"**Priority:** {f.suggested_action.priority.upper()}")
                lines.append("")
        
        return "\n".join(lines).strip()
