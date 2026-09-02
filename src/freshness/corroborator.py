from typing import List, Dict, Tuple
from collections import defaultdict
from src.freshness.models import Fact, FactType, ResolutionState, FactResolution, FactSource

class FactCorroborator:
    @staticmethod
    def corroborate(facts: List[Fact]) -> List[FactResolution]:
        # Group by fact type
        grouped: Dict[FactType, List[Fact]] = defaultdict(list)
        for f in facts:
            grouped[f.type].append(f)
            
        resolutions = []
        
        for ftype, type_facts in grouped.items():
            if ftype in (FactType.PHONE, FactType.EMAIL, FactType.BRAND_NAME, FactType.COPYRIGHT_YEAR):
                resolutions.append(FactCorroborator._resolve_singular_fact(ftype, type_facts))
            elif ftype == FactType.PRODUCT:
                # Products aren't singular per site, they just accumulate.
                # Just emit them as RESOLVED or PROBABLE based on occurrence count.
                pass 
                
        return resolutions
        
    @staticmethod
    def _normalize(val: str, ftype: FactType) -> str:
        if ftype == FactType.PHONE:
            # strip all non-numeric characters for comparison
            return ''.join(filter(str.isdigit, val))
        if ftype == FactType.EMAIL:
            return val.lower()
        if ftype == FactType.BRAND_NAME:
            return val.lower()
        return val

    @staticmethod
    def _resolve_singular_fact(ftype: FactType, facts: List[Fact]) -> FactResolution:
        # We expect a site to generally have one primary brand name, or one primary support phone,
        # but in reality they might have multiples. If they have totally different ones across 
        # different pages in the same context (e.g. global footer), it's a contradiction.
        
        normalized_map: Dict[str, List[Fact]] = defaultdict(list)
        for f in facts:
            norm = FactCorroborator._normalize(f.value, ftype)
            if norm:
                normalized_map[norm].append(f)
                
        all_values = list(normalized_map.keys())
        
        if not all_values:
            return FactResolution(
                fact_type=ftype,
                primary_value=None,
                state=ResolutionState.INSUFFICIENT_EVIDENCE,
                corroborating_sources=[],
                contradicting_sources=[],
                all_values=[]
            )
            
        if len(all_values) == 1:
            val = all_values[0]
            sources = [f.source for f in normalized_map[val]]
            # If it only appears on one page, it's PROBABLE. If multiple, RESOLVED.
            unique_urls = {s.url for s in sources}
            state = ResolutionState.RESOLVED if len(unique_urls) > 1 else ResolutionState.PROBABLE
            return FactResolution(
                fact_type=ftype,
                primary_value=normalized_map[val][0].value,
                state=state,
                corroborating_sources=sources,
                contradicting_sources=[],
                all_values=all_values
            )
            
        # Contradiction: Multiple distinct values found for a singular fact type
        # Sort by frequency to find a "primary" candidate, though it's unresolved.
        sorted_vals = sorted(all_values, key=lambda v: len({f.source.url for f in normalized_map[v]}), reverse=True)
        primary_val = sorted_vals[0]
        
        primary_sources = [f.source for f in normalized_map[primary_val]]
        contradicting_sources = []
        for v in sorted_vals[1:]:
            contradicting_sources.extend([f.source for f in normalized_map[v]])
            
        return FactResolution(
            fact_type=ftype,
            primary_value=normalized_map[primary_val][0].value,
            state=ResolutionState.UNRESOLVED,
            corroborating_sources=primary_sources,
            contradicting_sources=contradicting_sources,
            all_values=all_values
        )
