from typing import List, Dict
from src.parser.models import ParsedPage
from src.analysis.models import Issue
from src.freshness.extractor import FactExtractor
from src.freshness.corroborator import FactCorroborator
from src.freshness.models import ResolutionState

class FreshnessCorroborationEngine:
    @staticmethod
    def analyze(parsed_pages: Dict[str, ParsedPage]) -> List[Issue]:
        issues = []
        all_facts = []
        
        # 1. Extract facts from all pages
        for url, page in parsed_pages.items():
            facts = FactExtractor.extract_facts(page)
            all_facts.extend(facts)
            
        # 2. Corroborate facts across the site
        resolutions = FactCorroborator.corroborate(all_facts)
        
        # 3. Generate findings based on resolution states
        for res in resolutions:
            if res.fact_type.name == "COPYRIGHT_YEAR":
                current_year = 2026
                max_year_found = 0
                for val in res.all_values:
                    try:
                        year_int = int(val)
                        max_year_found = max(max_year_found, year_int)
                    except ValueError:
                        pass
                
                if max_year_found > 0 and max_year_found < current_year:
                    issues.append(Issue(
                        title="Stale Content",
                        severity="MEDIUM",
                        confidence="HIGH",
                        evidence=[f"The most recent copyright year found is {max_year_found}, which is older than the current year ({current_year})."],
                        why="Outdated copyright years or missing current temporal markers strongly signal to AI bots that the site may be abandoned or outdated.",
                        action="Update the copyright year in the footer and ensure content timestamps are current."
                    ))
                continue
                
            if res.state == ResolutionState.UNRESOLVED:
                # Direct contradiction found
                primary = res.primary_value
                others = [v for v in res.all_values if v != primary]
                
                evidence = [f"Primary {res.fact_type.value}: '{primary}' found on {len(res.corroborating_sources)} pages.", f"Contradicting values: {others} found on {len(res.contradicting_sources)} pages."]
                
                issues.append(Issue(
                    title=f"Contradicting {res.fact_type.name.title()}",
                    severity="HIGH",
                    confidence="HIGH",
                    evidence=evidence,
                    why=f"AI assistants may present incorrect or hallucinated {res.fact_type.value} to users because the website provides multiple conflicting sources of truth.",
                    action="Ensure core organizational facts are strictly consistent across all pages (header, footer, contact pages, and JSON-LD metadata)."
                ))
            elif res.state == ResolutionState.INSUFFICIENT_EVIDENCE:
                # No evidence found for a core fact
                if res.fact_type.name == "BRAND_NAME":
                    issues.append(Issue(
                        title="Missing Brand Identity",
                        severity="MEDIUM",
                        confidence="HIGH",
                        evidence=["No clear organization or brand name could be extracted from JSON-LD or Meta tags across the crawled pages."],
                        why="Without explicit brand identity markup, AI models may struggle to definitively associate the website content with the correct real-world entity.",
                        action="Add Organization or LocalBusiness JSON-LD markup to the homepage."
                    ))

        return issues
