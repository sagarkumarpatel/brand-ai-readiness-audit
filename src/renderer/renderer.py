import time
from typing import Optional
from .models import RenderResult

class SafeRenderer:
    def __init__(self, timeout_seconds: int = 10, max_size_bytes: int = 5 * 1024 * 1024):
        self.timeout_ms = timeout_seconds * 1000
        self.max_size_bytes = max_size_bytes
        self.browser = None
        self.playwright_context = None

    def start(self):
        try:
            from playwright.sync_api import sync_playwright
            self.playwright_context = sync_playwright().start()
            self.browser = self.playwright_context.chromium.launch(headless=True)
        except ImportError:
            raise RuntimeError("Playwright is not installed. Please run: pip install playwright && playwright install chromium")
        except Exception as e:
            raise RuntimeError(f"Failed to start browser: {str(e)}")

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright_context:
            self.playwright_context.stop()
            
    def __enter__(self):
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def render(self, url: str) -> RenderResult:
        if not self.browser:
            return RenderResult(url, url, None, False, "", error="Browser not started")

        start_time = time.time()
        try:
            page = self.browser.new_page()
            # Set default timeouts
            page.set_default_navigation_timeout(self.timeout_ms)
            page.set_default_timeout(self.timeout_ms)
            
            # Read-only configuration
            page.route("**/*", lambda route: route.continue_() if route.request.resource_type in ["document", "script", "stylesheet", "image", "font", "fetch", "xhr"] else route.abort())

            response = page.goto(url, wait_until="domcontentloaded")
            
            status = response.status if response else 0
            
            # Allow some time for scripts to execute post-load
            try:
                page.wait_for_load_state("networkidle", timeout=self.timeout_ms // 2)
            except Exception:
                pass # Timeout on networkidle is fine, we just take what we have
                
            html = page.content()
            if len(html.encode('utf-8')) > self.max_size_bytes:
                page.close()
                return RenderResult(url, page.url, status, False, "", timing_ms=(time.time() - start_time) * 1000, error="Oversized rendered response")

            # Simple extraction from playwright
            visible_text = page.evaluate("document.body ? document.body.innerText : ''")
            
            # Extract links using evaluate for safe read-only DOM inspection
            links_data = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText
                })).filter(a => a.href);
            }''')
            
            from src.parser.models import Link
            from urllib.parse import urlparse
            base_netloc = urlparse(url).netloc
            links = []
            for l in links_data:
                parsed_href = urlparse(l['href'])
                is_internal = parsed_href.netloc == base_netloc or not parsed_href.netloc
                links.append(Link(url=l['href'], anchor_text=l['text'].strip(), is_internal=is_internal))

            page.close()
            return RenderResult(
                requested_url=url,
                final_url=page.url,
                status_code=status,
                rendered_successfully=True,
                html=html,
                visible_text=visible_text,
                links=links,
                timing_ms=(time.time() - start_time) * 1000
            )

        except Exception as e:
            return RenderResult(url, url, None, False, "", timing_ms=(time.time() - start_time) * 1000, error=str(e))
