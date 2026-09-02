import time
import urllib.request
import urllib.error
from urllib.parse import urlparse, urljoin
import re
from typing import List, Set, Dict

from .models import CrawlConfig, CrawlResponse
from .robots import RobotsTxtHandler

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Disable automatic redirects

class SafeCrawler:
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.robots_handler = RobotsTxtHandler(user_agent=config.user_agent, timeout=config.timeout_seconds)
        self.visited: Set[str] = set()
        self.results: List[CrawlResponse] = []
        self.queue: List[dict] = []
        
        # Setup opener without auto-redirects to track chains
        self.opener = urllib.request.build_opener(NoRedirectHandler())

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        # Drop fragments
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        # Remove trailing slash if path is just '/' or for clean deduplication
        if normalized.endswith('/') and len(parsed.path) > 1:
            normalized = normalized[:-1]
        return normalized

    def _is_allowed_domain(self, url: str) -> bool:
        if not self.config.allowed_domains:
            return True
        parsed = urlparse(url)
        return any(parsed.netloc == domain or parsed.netloc.endswith(f".{domain}") for domain in self.config.allowed_domains)

    def _extract_links(self, html: str, base_url: str) -> List[str]:
        # Simple regex for links, sufficient for foundation module
        links = []
        for match in re.finditer(r'href=[\'"]?([^\'" >]+)', html, re.IGNORECASE):
            link = match.group(1)
            full_url = urljoin(base_url, link)
            parsed = urlparse(full_url)
            if parsed.scheme in ('http', 'https'):
                links.append(full_url)
        return links

    def _fetch(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={'User-Agent': self.config.user_agent})
        start_time = time.time()
        
        try:
            with self.opener.open(req, timeout=self.config.timeout_seconds) as response:
                status = response.getcode()
                headers = dict(response.headers)
                headers_lower = {k.lower(): v for k, v in headers.items()}
                content_type = headers_lower.get('content-type', '')
                
                # Check size limit
                content_length = headers.get('Content-Length')
                if content_length and int(content_length) > self.config.max_response_size_bytes:
                    return {'status': status, 'error': 'Oversized response', 'timing': time.time() - start_time, 'headers': headers}

                # Only read text/html
                if 'text/html' not in content_type.lower():
                    return {'status': status, 'error': 'Unsupported content type', 'timing': time.time() - start_time, 'headers': headers}

                # Read in chunks to enforce size limit dynamically
                body = b""
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    body += chunk
                    if len(body) > self.config.max_response_size_bytes:
                        return {'status': status, 'error': 'Oversized response', 'timing': time.time() - start_time, 'headers': headers}
                
                html = body.decode('utf-8', errors='ignore')
                return {
                    'status': status,
                    'html': html,
                    'headers': headers,
                    'content_type': content_type,
                    'timing': time.time() - start_time
                }
        except urllib.error.HTTPError as e:
            # Catch HTTP errors (e.g. 301, 404)
            return {
                'status': e.code,
                'headers': dict(e.headers),
                'error': None if e.code in (301, 302, 303, 307, 308) else f'HTTP Error {e.code}',
                'timing': time.time() - start_time
            }
        except Exception as e:
            return {'status': 0, 'error': str(e), 'timing': time.time() - start_time, 'headers': {}}

    def crawl(self, start_urls: List[str]):
        for url in start_urls:
            self.queue.append({'url': url, 'depth': 0, 'parent': None})

        while self.queue and len(self.results) < self.config.max_pages:
            item = self.queue.pop(0)
            current_url = item['url']
            depth = item['depth']
            parent = item['parent']

            normalized_url = self._normalize_url(current_url)

            if normalized_url in self.visited:
                continue
            
            if not self._is_allowed_domain(normalized_url):
                continue

            if depth > self.config.max_depth:
                continue

            if not self.robots_handler.is_allowed(normalized_url):
                self.visited.add(normalized_url)
                self.results.append(CrawlResponse(
                    url=normalized_url, status_code=0, headers={}, content_type="", html="", 
                    redirect_chain=[], depth=depth, parent_url=parent, timing_ms=0, error="Blocked by robots.txt"
                ))
                continue

            # Process redirects manually
            redirect_chain = []
            target_url = normalized_url
            redirects = 0
            fetch_result = None
            
            while redirects <= self.config.max_redirects:
                self.visited.add(target_url)
                fetch_result = self._fetch(target_url)
                
                if fetch_result['status'] in (301, 302, 303, 307, 308):
                    location = fetch_result['headers'].get('Location')
                    if location:
                        next_url = urljoin(target_url, location)
                        next_url_norm = self._normalize_url(next_url)
                        redirect_chain.append(next_url_norm)
                        target_url = next_url_norm
                        redirects += 1
                        time.sleep(0.1)  # Safe rate limit
                    else:
                        fetch_result['error'] = 'Redirect missing Location header'
                        break
                else:
                    break

            if redirects > self.config.max_redirects:
                fetch_result['error'] = 'Too many redirects'

            response = CrawlResponse(
                url=target_url,
                status_code=fetch_result['status'],
                headers=fetch_result.get('headers', {}),
                content_type=fetch_result.get('content_type', ''),
                html=fetch_result.get('html', ''),
                redirect_chain=redirect_chain,
                depth=depth,
                parent_url=parent,
                timing_ms=fetch_result.get('timing', 0) * 1000,
                error=fetch_result.get('error')
            )
            
            self.results.append(response)

            if not response.error and response.html:
                links = self._extract_links(response.html, target_url)
                for link in set(links):
                    norm_link = self._normalize_url(link)
                    if norm_link not in self.visited and self._is_allowed_domain(norm_link):
                        self.queue.append({'url': norm_link, 'depth': depth + 1, 'parent': target_url})
            
            time.sleep(0.1)  # Safe rate limit

        return self.results
