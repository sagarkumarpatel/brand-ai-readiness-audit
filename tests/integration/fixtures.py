import json
import datetime

def get_current_date():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def get_stale_date():
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=400)).isoformat()

FIXTURES = {
    # ---------------------------------------------------------
    # CLEAN SITE (no findings)
    # ---------------------------------------------------------
    "/clean/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Clean Site</title>
            <meta name="description" content="A perfectly clean site.">
            <link rel="canonical" href="http://127.0.0.1:8080/clean/">
            <script type="application/ld+json">
            {{
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "Clean Corp",
                "url": "http://127.0.0.1:8080/clean/"
            }}
            </script>
        </head>
        <body>
            <h1>Clean Site Home</h1>
            <p>Welcome to the clean site. Last updated: <time datetime="{get_current_date()}">Today</time></p>
            <nav>
                <a href="/clean/about">About Us</a>
                <a href="/clean/contact">Contact</a>
            </nav>
            <address>
                Email: <a href="mailto:contact@cleancorp.com">contact@cleancorp.com</a>
                Phone: <a href="tel:+18005550199">+1-800-555-0199</a>
            </address>
            <p>Some meaningful textual content to ensure this is not thin.</p>
            <p>Another paragraph to make it robust.</p>
        </body>
        </html>
        """
    },
    "/clean/about": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>About Clean Corp</title>
            <meta name="description" content="About our clean site.">
            <link rel="canonical" href="http://127.0.0.1:8080/clean/about">
        </head>
        <body>
            <h1>About Us</h1>
            <p>We are a clean corporation. {"Word " * 50}</p>
            <nav><a href="/clean/">Home</a></nav>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/clean/contact": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Contact Clean Corp</title>
            <meta name="description" content="Contact us.">
            <link rel="canonical" href="http://127.0.0.1:8080/clean/contact">
        </head>
        <body>
            <h1>Contact Us</h1>
            <p>Get in touch. {"Word " * 50}</p>
            <address>
                Email: <a href="mailto:contact@cleancorp.com">contact@cleancorp.com</a>
                Phone: <a href="tel:+18005550199">+1-800-555-0199</a>
            </address>
            <nav><a href="/clean/">Home</a></nav>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/clean/robots.txt": {
        "status": 200,
        "content_type": "text/plain",
        "body": "User-agent: *\nAllow: /\nSitemap: http://127.0.0.1:8080/clean/sitemap.xml"
    },
    "/clean/sitemap.xml": {
        "status": 200,
        "content_type": "application/xml",
        "body": """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url><loc>http://127.0.0.1:8080/clean/</loc></url>
           <url><loc>http://127.0.0.1:8080/clean/about</loc></url>
           <url><loc>http://127.0.0.1:8080/clean/contact</loc></url>
        </urlset>"""
    },
    
    # ---------------------------------------------------------
    # SINGLE ISSUES
    # ---------------------------------------------------------
    
    # Missing canonical
    "/issue-canonical/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head><title>No Canonical</title></head>
        <body>
            <h1>Missing Canonical</h1>
            <p>Content.</p>
            <a href="/issue-canonical/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </body>
        </html>
        """
    },
    
    # Missing structured data
    "/issue-structured/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>No Structured Data</title>
            <meta property="og:type" content="article">
            <link rel="canonical" href="http://127.0.0.1:8080/issue-structured/">
        </head>
        <body>
            <article>
                <h1>An Important Article</h1>
                <p>This is a long article that lacks structured data. {"Word " * 50}</p>
                <a href="/issue-structured/">Home</a>
                <p>Updated <time datetime="{get_current_date()}">recently</time></p>
            </article>
        </body>
        </html>
        """
    },
    
    # Stale Content
    "/issue-stale/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Stale Content</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-stale/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Stale Content</h1>
            <p>Content updated a long time ago: <time datetime="{get_stale_date()}">Old</time></p>
            <footer>&copy; 2022 Old Company</footer>
            <a href="/issue-stale/">Home</a>
        </body>
        </html>
        """
    },
    
    # Contact Conflict
    "/issue-contact-conflict/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Contact Conflict 1</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-contact-conflict/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Contact Conflict</h1>
            <address>Email: <a href="mailto:info@domain.com">info@domain.com</a></address>
            <a href="/issue-contact-conflict/page2">Page 2</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/issue-contact-conflict/page2": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Contact Conflict 2</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-contact-conflict/page2">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Contact Conflict 2</h1>
            <address>Email: <a href="mailto:other@domain.com">other@domain.com</a></address>
            <a href="/issue-contact-conflict/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    
    # Thin content (less than 15 words, no json ld)
    "/issue-thin/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Thin</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-thin/">
        </head>
        <body>
            <a href="/issue-thin/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    
    # Dead end (Must not be root)
    "/issue-deadend/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Dead End Root</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-deadend/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Home</h1>
            <a href="/issue-deadend/page2">Page 2</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
            <p>{"Word " * 20}</p>
        </body>
        </html>
        """
    },
    "/issue-deadend/page2": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Dead End Page</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-deadend/page2">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Dead End</h1>
            <p>There are no internal links here.</p>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
            <p>{"Word " * 20}</p>
        </body>
        </html>
        """
    },
    
    # Wall of text
    "/issue-walloftext/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Wall of Text</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-walloftext/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <p>{"Word " * 3005}</p>
            <a href="/issue-walloftext/">Home</a>
        </body>
        </html>
        """
    },
    
    # Render-locked content (JS generated)
    "/issue-renderlocked/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Render Locked</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-renderlocked/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Render Locked</h1>
            <div id="content"></div>
            <script>
                document.getElementById('content').innerHTML = '<p>Rendered paragraph.</p><a href="/issue-renderlocked/hidden">Hidden Link</a>';
            </script>
            <a href="/issue-renderlocked/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    
    # Redirect chain
    "/issue-redirect/": {
        "status": 301,
        "headers": {"Location": "/issue-redirect/1"},
        "body": ""
    },
    "/issue-redirect/1": {
        "status": 301,
        "headers": {"Location": "/issue-redirect/2"},
        "body": ""
    },
    "/issue-redirect/2": {
        "status": 301,
        "headers": {"Location": "/issue-redirect/3"},
        "body": ""
    },
    "/issue-redirect/3": {
        "status": 301,
        "headers": {"Location": "/issue-redirect/4"},
        "body": ""
    },
    "/issue-redirect/4": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Redirect Dest</title>
            <link rel="canonical" href="http://127.0.0.1:8080/issue-redirect/4">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Destination</h1>
            <a href="/issue-redirect/4">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    
    # ---------------------------------------------------------
    # MULTI-ISSUE SITE (Stale, Thin, Missing Canonical, Dead-End, Render Locked)
    # ---------------------------------------------------------
    "/multi/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head><title>Multi Issue Home</title></head>
        <body>
            <h1>Multi Issue Home</h1>
            <!-- Stale -->
            <p>Updated <time datetime="{get_stale_date()}">old</time></p>
            <a href="/multi/page2">Page 2</a>
            <a href="/multi/page3">Page 3</a>
        </body>
        </html>
        """
    },
    "/multi/page2": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Multi Issue Page 2</title>
            <link rel="canonical" href="http://127.0.0.1:8080/multi/page2">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <!-- Dead end -->
            <!-- Thin content -->
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/multi/page3": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Multi Issue Page 3</title>
            <link rel="canonical" href="http://127.0.0.1:8080/multi/page3">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <!-- Render Locked -->
            <div id="content"></div>
            <script>
                document.getElementById('content').innerHTML = '<p>Rendered paragraph.</p><a href="/multi/">Hidden Link</a>';
            </script>
            <a href="/multi/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    
    # ---------------------------------------------------------
    # EDGE CASES
    # ---------------------------------------------------------
    
    # Robots.txt testing
    "/robots-test/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Robots Test</title>
            <link rel="canonical" href="http://127.0.0.1:8080/robots-test/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <a href="/robots-test/allowed">Allowed</a>
            <a href="/robots-test/disallowed">Disallowed</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/robots-test/allowed": {
        "status": 200,
        "content_type": "text/html",
        "body": f"<html><head><title>Allowed</title><link rel='canonical' href='http://127.0.0.1:8080/robots-test/allowed'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><a href='/robots-test/'>Home</a><p>Updated <time datetime='{get_current_date()}'>recently</time></p></body></html>"
    },
    "/robots-test/disallowed": {
        "status": 200,
        "content_type": "text/html",
        "body": "<html><body>Secret!</body></html>"
    },
    "/robots-test/robots.txt": {
        "status": 200,
        "content_type": "text/plain",
        "body": "User-agent: *\nDisallow: /robots-test/disallowed"
    },
    
    # Malformed HTML
    "/malformed/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head><title>Malformed</title><link rel="canonical" href="http://127.0.0.1:8080/malformed/"><script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script></head>
        <body>
            <div id="unclosed">
            <span>Text
            <a href="/malformed/">Home</a
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        """
    },
    
    # Errors
    "/errors/": {
        "status": 200,
        "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Errors</title>
            <link rel="canonical" href="http://127.0.0.1:8080/errors/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <a href="/errors/404">404</a>
            <a href="/errors/500">500</a>
            <a href="/errors/">Home</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/errors/404": {
        "status": 404,
        "content_type": "text/html",
        "body": "Not found"
    },
    "/errors/500": {
        "status": 500,
        "content_type": "text/html",
        "body": "Server Error"
    }
}
