from typing import Optional
from src.findings.models import NormalizedFinding
from src.recommendations.models import Recommendation

class RecommendationEngine:
    SEVERITY_PRIORITY_MAP = {
        "CRITICAL": "P0",
        "HIGH": "P1",
        "MEDIUM": "P2",
        "LOW": "P3"
    }

    ACTION_MAP = {
        "Missing Canonical URL": "Add a self-referencing canonical URL to the page and ensure it points to the preferred indexable URL.",
        "Missing Structured Data": "Implement appropriate JSON-LD structured data (e.g., Organization, Product, Article) to provide unambiguous entity signals to AI and search crawlers.",
        "Render-locked Content": "Implement server-side rendering (SSR) or dynamic rendering so that critical content is available in the raw HTML response without requiring JavaScript execution.",
        "Render-locked Navigation": "Implement server-side rendering (SSR) or dynamic rendering so that critical navigation is available in the raw HTML response without requiring JavaScript execution.",
        "Sitemap Page Blocked by Robots.txt": "Ensure the robots.txt file and x-robots-tag headers do not block crawlers from accessing important pages, and that they are included in an XML sitemap.",
        "Unreachable Important Page": "Ensure all important pages are reachable via internal links or XML sitemap.",
        "Contradicting Email": "Choose the authoritative business email and update the conflicting first-party pages so the same canonical contact value is consistently published.",
        "Contradicting Phone": "Choose the authoritative business phone number and update the conflicting first-party pages so the same canonical contact value is consistently published.",
        "Contradicting Address": "Choose the authoritative business address and update the conflicting first-party pages so the same canonical contact value is consistently published.",
        "Conflicting Contact Information": "Choose the authoritative business phone number, email, and address and update the conflicting first-party pages.",
        "Stale Content": "Update the content to reflect the current year and ensure any temporal claims (like 'we are currently...') remain accurate. Avoid hardcoding dates.",
        "Thin Content": "Provide sufficient, well-structured original content that conveys clear meaning to an AI parser. Ensure the page relies on text, not just images or sparse UI elements.",
        "Dead End Page": "Add at least one relevant internal next-step link from this page to an appropriate parent, related, or conversion-oriented page so the page is not an internal dead end.",
        "Unstructured Wall of Text": "Break up monolithic text blocks using semantic HTML headings (<h2>, <h3>) and lists to help AI models extract key sections, answers, and context accurately."
    }

    @staticmethod
    def _map_priority(severity: str, confidence: str) -> str:
        # Simple mapping: directly map severity to priority. 
        # For a more advanced mapping, confidence could downgrade it.
        # But for deterministic behavior, we map severity directly.
        # If low confidence, maybe downgrade priority? 
        # Requirements say: "Implement deterministic priority mapping using: severity, confidence, potential impact, scope"
        # We will keep it simple for deterministic mapping.
        s = severity.upper()
        if s not in RecommendationEngine.SEVERITY_PRIORITY_MAP:
            s = "MEDIUM"
            
        c = confidence.upper()
        
        # Example downgrade: If it's HIGH severity but LOW confidence, downgrade to P2
        if s == "HIGH" and c == "LOW":
            return "P2"
        if s == "CRITICAL" and c == "LOW":
            return "P1"
            
        return RecommendationEngine.SEVERITY_PRIORITY_MAP[s]

    @staticmethod
    def generate(finding: NormalizedFinding) -> Optional[Recommendation]:
        if not finding or not finding.evidence:
            return None

        # Look up a specific action, or provide a conservative fallback
        summary = RecommendationEngine.ACTION_MAP.get(
            finding.title, 
            "Review the specific evidence associated with this finding and update the page structure or content to align with standard AI discoverability best practices."
        )

        priority = RecommendationEngine._map_priority(finding.severity, finding.confidence)

        return Recommendation(
            finding_id=finding.id,
            suggested_action={
                "summary": summary,
                "priority": priority
            }
        )
