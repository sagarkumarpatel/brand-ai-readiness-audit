import re
import json
from typing import List, Dict, Any
from src.parser.models import ParsedPage
from src.freshness.models import Fact, FactType, FactSource

class FactExtractor:
    @staticmethod
    def extract_facts(page: ParsedPage) -> List[Fact]:
        facts = []
        
        # 1. Contact Info from links
        for link in page.links:
            href = link.url.lower().strip()
            if href.startswith("tel:"):
                val = href.replace("tel:", "").strip()
                facts.append(Fact(
                    type=FactType.PHONE,
                    value=val,
                    source=FactSource(url=page.url, location="html_link", context=link.anchor_text or val)
                ))
            elif href.startswith("mailto:"):
                val = href.replace("mailto:", "").strip()
                facts.append(Fact(
                    type=FactType.EMAIL,
                    value=val,
                    source=FactSource(url=page.url, location="html_link", context=link.anchor_text or val)
                ))
                
        # 2. Organization / Brand Name from metadata and title
        if page.title:
            # Heuristic: Title usually ends with " - BrandName" or " | BrandName"
            match = re.search(r'[-|\|]([^-|]+)$', page.title)
            if match:
                brand = match.group(1).strip()
                if len(brand) > 1 and len(brand) < 50:
                    facts.append(Fact(
                        type=FactType.BRAND_NAME,
                        value=brand,
                        source=FactSource(url=page.url, location="title_tag", context=page.title)
                    ))
        
        # OpenGraph site_name is a strong signal
        og_site_name = page.open_graph.get("og:site_name") if hasattr(page, 'open_graph') else None
        if og_site_name:
            facts.append(Fact(
                type=FactType.BRAND_NAME,
                value=og_site_name.strip(),
                source=FactSource(url=page.url, location="og:site_name", context=og_site_name.strip())
            ))

        # 3. Extract Copyright year from visible text
        # simple heuristic looking for © or Copyright followed by a year
        if page.visible_text:
            match = re.search(r'(?:©|Copyright)\s*(?:[A-Za-z\s]*?)\s*([12][0-9]{3})', page.visible_text, re.IGNORECASE)
            if match:
                year = match.group(1)
                facts.append(Fact(
                    type=FactType.COPYRIGHT_YEAR,
                    value=year,
                    source=FactSource(url=page.url, location="visible_text", context=match.group(0))
                ))
                
        # 4. JSON-LD structured data extraction
        for block in page.json_ld_blocks:
            try:
                data = json.loads(block) if isinstance(block, str) else block
                if isinstance(data, dict):
                    FactExtractor._extract_from_json_ld(data, page.url, facts)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            FactExtractor._extract_from_json_ld(item, page.url, facts)
            except (json.JSONDecodeError, TypeError):
                pass

        return facts
        
    @staticmethod
    def _extract_from_json_ld(data: Dict[str, Any], url: str, facts: List[Fact]):
        # Very simple JSON-LD traversal looking for specific types
        node_type = data.get("@type")
        if not node_type:
            return
            
        if isinstance(node_type, str):
            node_type = [node_type]
            
        for t in node_type:
            if t in ("Organization", "LocalBusiness"):
                name = data.get("name")
                if isinstance(name, str):
                    facts.append(Fact(
                        type=FactType.BRAND_NAME,
                        value=name.strip(),
                        source=FactSource(url=url, location="json-ld", context=f"Organization.name")
                    ))
                tel = data.get("telephone")
                if isinstance(tel, str):
                    facts.append(Fact(
                        type=FactType.PHONE,
                        value=tel.strip(),
                        source=FactSource(url=url, location="json-ld", context=f"Organization.telephone")
                    ))
                email = data.get("email")
                if isinstance(email, str):
                    facts.append(Fact(
                        type=FactType.EMAIL,
                        value=email.strip(),
                        source=FactSource(url=url, location="json-ld", context=f"Organization.email")
                    ))
            elif t == "Product":
                name = data.get("name")
                if isinstance(name, str):
                    facts.append(Fact(
                        type=FactType.PRODUCT,
                        value=name.strip(),
                        source=FactSource(url=url, location="json-ld", context=f"Product.name")
                    ))
            
        date_mod = data.get("dateModified") or data.get("datePublished")
        if isinstance(date_mod, str):
            facts.append(Fact(
                type=FactType.DATE,
                value=date_mod.strip(),
                source=FactSource(url=url, location="json-ld", context=f"dateModified/datePublished")
            ))
            
        # recursive check for nested elements (like ContactPoint)
        for k, v in data.items():
            if isinstance(v, dict):
                FactExtractor._extract_from_json_ld(v, url, facts)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        FactExtractor._extract_from_json_ld(item, url, facts)

