import urllib.robotparser
from urllib.parse import urlparse
import urllib.request

class RobotsTxtHandler:
    def __init__(self, user_agent: str, timeout: int = 10):
        self.user_agent = user_agent
        self.timeout = timeout
        self.parsers = {}

    def is_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.parsers:
            robots_url = f"{base_url}/robots.txt"
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            try:
                # Custom fetch to enforce timeout
                req = urllib.request.Request(robots_url, headers={'User-Agent': self.user_agent})
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    content = response.read().decode('utf-8', errors='ignore')
                    rp.parse(content.splitlines())
                self.parsers[base_url] = rp
            except Exception:
                # If robots.txt can't be fetched or parsed, assume allowed per standard conventions
                self.parsers[base_url] = None
                
        rp = self.parsers.get(base_url)
        if rp is None:
            return True
            
        return rp.can_fetch(self.user_agent, url)
