import re
import xml.etree.ElementTree as ET
from typing import List
import urllib.request

class SitemapParser:
    def __init__(self, user_agent: str = "BrandAIReadinessAuditBot/1.0", timeout: int = 10):
        self.user_agent = user_agent
        self.timeout = timeout

    def extract_urls(self, sitemap_url: str) -> List[str]:
        try:
            req = urllib.request.Request(sitemap_url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.getcode() != 200:
                    return []
                content = response.read()
                
                # Simple extraction, handling nested sitemaps
                urls = []
                try:
                    root = ET.fromstring(content)
                    # Handle namespaces
                    namespace = ''
                    if '}' in root.tag:
                        namespace = root.tag.split('}')[0] + '}'
                    
                    if 'sitemapindex' in root.tag:
                        # Fetch sub-sitemaps
                        for sitemap in root.findall(f".//{namespace}sitemap"):
                            loc = sitemap.find(f"{namespace}loc")
                            if loc is not None and loc.text:
                                urls.extend(self.extract_urls(loc.text.strip()))
                    else:
                        for url_node in root.findall(f".//{namespace}url"):
                            loc = url_node.find(f"{namespace}loc")
                            if loc is not None and loc.text:
                                urls.append(loc.text.strip())
                except ET.ParseError:
                    # Fallback to regex if XML parsing fails
                    locs = re.findall(r'<loc>(.*?)</loc>', content.decode('utf-8', errors='ignore'))
                    urls.extend([l.strip() for l in locs])
                    
                return urls
        except Exception:
            return []
