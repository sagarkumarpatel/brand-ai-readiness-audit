from urllib.parse import urlparse
from .models import ParsedPage
import json

class PageClassifier:
    def classify(self, page: ParsedPage) -> str:
        # Heuristic and generic classification
        parsed_url = urlparse(page.url)
        path = parsed_url.path.lower()
        
        # 1. URL based heuristics
        if path == "" or path == "/":
            return "homepage"
            
        if "/product" in path or "/item/" in path or "/p/" in path:
            return "product"
            
        if "/category" in path or "/collections" in path:
            return "category"
            
        if "/blog" in path or "/article" in path or "/news" in path:
            return "article"
            
        if "/about" in path or "/company" in path:
            return "organization"
            
        if "/contact" in path:
            return "contact"
            
        if "/search" in path:
            return "search"
            
        if "/docs" in path or "/documentation" in path or "/help" in path:
            return "documentation"
            
        # 2. Open Graph based heuristics
        og_type = page.open_graph.get("og:type", "").lower()
        if og_type == "product":
            return "product"
        if og_type == "article":
            return "article"
            
        # 3. JSON-LD based heuristics
        for block in page.json_ld_blocks:
            try:
                data = json.loads(block)
                types = data.get("@type", "")
                if not isinstance(types, list):
                    types = [types]
                
                for t in types:
                    t_lower = str(t).lower()
                    if t_lower == "product":
                        return "product"
                    elif t_lower in ("article", "newsarticle", "blogposting"):
                        return "article"
                    elif t_lower in ("organization", "localbusiness"):
                        return "organization"
                    elif t_lower == "contactpage":
                        return "contact"
            except Exception:
                continue
                
        return "generic"
