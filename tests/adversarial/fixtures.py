from datetime import datetime, timezone
import json

def get_current_date():
    return datetime.now(timezone.utc).isoformat()

ADVERSARIAL_FIXTURES = {
    # ---------------------------------------------------------
    # ADVERSARIAL HTML & URLS
    # ---------------------------------------------------------
    "/malformed-html/": {
        "status": 200,
        "content_type": "text/html",
        "body": """
        <html><head>
        <title>""" + ("A" * 5000) + """</title>
        <meta name="description" content=\"""" + ("B" * 5000) + """\">
        <link rel="canonical" href="http://127.0.0.1:8081/malformed-html/">
        <link rel="canonical" href="http://127.0.0.1:8081/malformed-html/duplicate">
        <script type="application/ld+json">[{ "@context": "https://schema.org", "@type": "WebPage" }, { "@context": "https://schema.org", "@type": "Organization", "name": "Duplicate Brand" }]</script>
        </head>
        <body>
        """ + ("<div>" * 100) + "Deeply nested content" + ("</div>" * 100) + """
        <a href="/malformed-html/?a=1&a=1&b=2%203">Query string</a>
        <a href="javascript:alert(1)">JS link</a>
        <a href="mailto:test@example.com">Mailto</a>
        <a href="data:text/html,<html></html>">Data</a>
        <a href="http://external.com/">External</a>
        <h1>Duplicate H1</h1><h1>Duplicate H1</h1>
        <p>""" + ("word " * 100) + """</p>
        <p>Updated <time datetime=\"""" + get_current_date() + """\">recently</time></p>
        <!-- Unclosed tags -->
        <span><div><p>
        </body></html>
        """
    },
    "/unicode-emoji/": {
        "status": 200,
        "content_type": "text/html; charset=utf-8",
        "body": f"""
        <html>
        <head>
            <title>🚀 Emoji Title 🌟</title>
            <link rel="canonical" href="http://127.0.0.1:8081/unicode-emoji/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <h1>Üñîçøðé 漢字 😊</h1>
            <a href="/unicode-emoji/">Hômè</a>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
            <p>{"Word 😊 " * 100}</p>
        </body>
        </html>
        """
    },
    
    # ---------------------------------------------------------
    # CRAWLER BOUNDARIES & REDIRECTS
    # ---------------------------------------------------------
    "/cyclic/1": {
        "status": 200, "content_type": "text/html",
        "body": f"<html><head><title>C1</title><link rel='canonical' href='http://127.0.0.1:8081/cyclic/1'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><a href='/cyclic/2'>Next</a><p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },
    "/cyclic/2": {
        "status": 200, "content_type": "text/html",
        "body": f"<html><head><title>C2</title><link rel='canonical' href='http://127.0.0.1:8081/cyclic/2'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><a href='/cyclic/1'>Back</a><p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },
    
    "/redirect-loop/1": {
        "status": 301,
        "headers": {"Location": "/redirect-loop/2"}
    },
    "/redirect-loop/2": {
        "status": 302,
        "headers": {"Location": "/redirect-loop/1"}
    },
    
    "/redirect-chain/1": {"status": 301, "headers": {"Location": "/redirect-chain/2"}},
    "/redirect-chain/2": {"status": 301, "headers": {"Location": "/redirect-chain/3"}},
    "/redirect-chain/3": {"status": 301, "headers": {"Location": "/redirect-chain/4"}},
    "/redirect-chain/4": {"status": 301, "headers": {"Location": "/redirect-chain/5"}},
    "/redirect-chain/5": {"status": 301, "headers": {"Location": "/redirect-chain/6"}},
    "/redirect-chain/6": {
        "status": 200, "content_type": "text/html",
        "body": f"<html><head><title>End</title><link rel='canonical' href='http://127.0.0.1:8081/redirect-chain/6'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },
    
    # ---------------------------------------------------------
    # NETWORK FAILURES & HANGS
    # ---------------------------------------------------------
    "/hang/": {
        "status": 200,
        "delay": 2.0, # Will trigger some timeouts if timeout is 1s
        "content_type": "text/html",
        "body": "<html><body>Hanged!</body></html>"
    },
    "/drop/": {
        "drop_connection": True
    },
    "/incomplete/": {
        "status": 200,
        "incomplete_response": True,
        "content_type": "text/html",
        "body": "<html><body>This response will be cut off before it finishes." * 100
    },
    "/error-500/": {
        "status": 500,
        "content_type": "text/plain",
        "body": "Internal Server Error"
    },
    
    # ---------------------------------------------------------
    # ROBOTS.TXT & SITEMAP
    # ---------------------------------------------------------
    "/robots-conflicts/robots.txt": {
        "status": 200, "content_type": "text/plain",
        "body": "User-agent: *\nDisallow: /robots-conflicts/secret\nAllow: /robots-conflicts/secret/public"
    },
    "/robots-conflicts/": {
        "status": 200, "content_type": "text/html",
        "body": f"<html><head><title>R</title><link rel='canonical' href='http://127.0.0.1:8081/robots-conflicts/'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><a href='/robots-conflicts/secret'>Secret</a> <a href='/robots-conflicts/secret/public'>Public</a><p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },
    "/robots-conflicts/secret": {
        "status": 200, "content_type": "text/html", "body": "<html><body>Blocked</body></html>"
    },
    "/robots-conflicts/secret/public": {
        "status": 200, "content_type": "text/html", "body": f"<html><head><title>Pub</title><link rel='canonical' href='http://127.0.0.1:8081/robots-conflicts/secret/public'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body>Allowed<p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },
    
    "/malformed-sitemap/sitemap.xml": {
        "status": 200, "content_type": "application/xml",
        "body": '<?xml version="1.0" encoding="UTF-8"?><urlset><url><loc>http://127.0.0.1:8081/malformed-sitemap/</loc></url><url><loc>http://external.com/</loc></url>' # Unclosed urlset
    },
    "/malformed-sitemap/": {
        "status": 200, "content_type": "text/html",
        "body": f"<html><head><title>Sitemap</title><link rel='canonical' href='http://127.0.0.1:8081/malformed-sitemap/'><script type='application/ld+json'>{{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\" }}</script></head><body><p>{'word '*100}</p><time datetime='{get_current_date()}'>t</time></body></html>"
    },

    # ---------------------------------------------------------
    # ANALYSIS BYPASS (False Positives)
    # ---------------------------------------------------------
    "/legit-short/": {
        "status": 200, "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Contact Us</title>
            <link rel="canonical" href="http://127.0.0.1:8081/legit-short/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "ContactPage" }}</script>
        </head>
        <body>
            <nav><a href="/">Home</a></nav>
            <h1>Contact</h1>
            <p>Email us at test@example.com</p>
            <p>Updated <time datetime="{get_current_date()}">recently</time></p>
        </body>
        </html>
        """
    },
    "/future-date/": {
        "status": 200, "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Future Date</title>
            <link rel="canonical" href="http://127.0.0.1:8081/future-date/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <a href="/">Home</a>
            <p>Updated <time datetime="2050-01-01T00:00:00Z">2050</time></p>
            <p>{"Word " * 100}</p>
        </body>
        </html>
        """
    },
    
    # ---------------------------------------------------------
    # DETERMINISM & REPORTING
    # ---------------------------------------------------------
    "/determinism/": {
        "status": 200, "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Determinism</title>
            <link rel="canonical" href="http://127.0.0.1:8081/determinism/">
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <a href="/determinism/2">Page 2</a>
            <a href="/determinism/3">Page 3</a>
            <p>Updated <time datetime="2020-01-01T00:00:00Z">old</time></p>
            <p>{"Word " * 10}</p> <!-- Thin content -->
        </body>
        </html>
        """
    },
    "/determinism/2": {
        "status": 200, "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Determinism 2</title>
            <script type="application/ld+json">{{ "@context": "https://schema.org", "@type": "WebPage" }}</script>
        </head>
        <body>
            <a href="/determinism/">Home</a>
            <p>Updated <time datetime="2020-01-01T00:00:00Z">old</time></p>
            <p>{"Word " * 10}</p> <!-- Thin content -->
        </body>
        </html>
        """
    },
    "/determinism/3": {
        "status": 200, "content_type": "text/html",
        "body": f"""
        <html>
        <head>
            <title>Determinism 3</title>
            <!-- Missing everything -->
        </head>
        <body>
            <a href="/determinism/">Home</a>
            <p>{"Word " * 10}</p> <!-- Thin content -->
        </body>
        </html>
        """
    }
}
