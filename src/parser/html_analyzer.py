from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from .models import ParsedPage, Link, Heading

class HTMLAnalyzer(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.parsed = ParsedPage(url=base_url, final_url=base_url, status_code=200, content_type="text/html")
        
        self.in_title = False
        self.in_script_json_ld = False
        self.in_main = False
        self.current_heading_level = 0
        self.current_anchor: dict = None
        self.current_text = []
        
        self.script_content = []
        self.main_content = []
        self.visible_text_chunks = []
        
        self.ignore_text_tags = {'script', 'style', 'noscript', 'meta', 'link'}
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        attrs_dict = dict(attrs)

        if tag == 'title':
            self.in_title = True
        
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            prop = attrs_dict.get('property', '').lower()
            content = attrs_dict.get('content', '')
            
            if name == 'description':
                if not self.parsed.meta_description:
                    self.parsed.meta_description = content
                else:
                    self.parsed.parsing_warnings.append("Duplicate meta description")
            elif name == 'robots':
                self.parsed.robots_directives.extend([d.strip().lower() for d in content.split(',')])
            elif prop.startswith('og:'):
                self.parsed.open_graph[prop] = content

        elif tag == 'link':
            rel = attrs_dict.get('rel')
            href = attrs_dict.get('href')
            if rel == 'canonical' and href:
                if not self.parsed.canonical_url:
                    self.parsed.canonical_url = urljoin(self.base_url, href)
                else:
                    self.parsed.parsing_warnings.append("Duplicate canonical URL")

        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.current_heading_level = int(tag[1])
            self.current_text = []

        elif tag == 'a':
            href = attrs_dict.get('href')
            if href:
                # Handle relative urls
                full_url = urljoin(self.base_url, href)
                parsed_full = urlparse(full_url)
                parsed_base = urlparse(self.base_url)
                
                is_internal = parsed_full.netloc == parsed_base.netloc or not parsed_full.netloc
                self.current_anchor = {'url': full_url, 'is_internal': is_internal, 'text': []}

        elif tag == 'script':
            type_attr = attrs_dict.get('type', '').lower()
            if type_attr == 'application/ld+json':
                self.in_script_json_ld = True
                self.script_content = []

        elif tag == 'main' or attrs_dict.get('role') == 'main':
            self.in_main = True

    def handle_endtag(self, tag):
        if self.tag_stack:
            if self.tag_stack[-1] == tag:
                self.tag_stack.pop()
            else:
                # Malformed HTML handling: unclosed tags
                pass
                
        if tag == 'title':
            self.in_title = False
        
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if self.current_heading_level > 0:
                text = ' '.join(self.current_text).strip()
                if text:
                    self.parsed.headings.append(Heading(level=self.current_heading_level, text=text))
                self.current_heading_level = 0
                self.current_text = []

        elif tag == 'a':
            if self.current_anchor:
                anchor_text = ' '.join(self.current_anchor['text']).strip()
                self.parsed.links.append(Link(
                    url=self.current_anchor['url'],
                    anchor_text=anchor_text,
                    is_internal=self.current_anchor['is_internal']
                ))
                self.current_anchor = None

        elif tag == 'script':
            if self.in_script_json_ld:
                self.parsed.json_ld_blocks.append(''.join(self.script_content))
                self.in_script_json_ld = False

        elif tag == 'main':
            self.in_main = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return

        if self.in_title:
            self.parsed.title = data

        if self.current_heading_level > 0:
            self.current_text.append(data)

        if self.current_anchor:
            self.current_anchor['text'].append(data)

        if self.in_script_json_ld:
            self.script_content.append(data)
            return

        # Visible text extraction
        current_tag = self.tag_stack[-1] if self.tag_stack else None
        if current_tag not in self.ignore_text_tags:
            self.visible_text_chunks.append(data)
            if self.in_main:
                self.main_content.append(data)

    def finalize(self):
        self.parsed.visible_text = ' '.join(self.visible_text_chunks)
        self.parsed.main_content = ' '.join(self.main_content)
        return self.parsed

def parse_html(html: str, base_url: str) -> ParsedPage:
    parser = HTMLAnalyzer(base_url)
    try:
        parser.feed(html)
    except Exception as e:
        parser.parsed.parsing_warnings.append(f"HTML Parse Error: {str(e)}")
    return parser.finalize()
