def make_html(title, body, meta="", headers="", thin=False):
    filler = "" if thin else "<p>" + "word "*20 + "</p>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {meta}
</head>
<body>
    <header>{headers}</header>
    <main>
        {body}
        {filler}
    </main>
</body>
</html>"""

GENERALIZATION_FIXTURES = {
    # Archetype 1: Corporate (clean)
    "/corporate/clean/": {
        "body": make_html("Corporate Home", 'Welcome to our company. <a href="/corporate/clean/about">About Us</a> <a href="/corporate/clean/contact">Contact</a>', meta='<link rel="canonical" href="/corporate/clean/"><script type="application/ld+json">{"@context": "https://schema.org", "@type": "Organization", "name": "Corp"}</script>'),
        "content_type": "text/html"
    },
    "/corporate/clean/about": {
        "body": make_html("About Us", "We are a great company." + "<p>More content here.</p>"*20, meta='<link rel="canonical" href="/corporate/clean/about">'),
        "content_type": "text/html"
    },
    "/corporate/clean/contact": {
        "body": make_html("Contact Us", '<address>123 Fake St, NY</address><a href="mailto:info@example.com">info@example.com</a><a href="tel:555-1234">555-1234</a>', meta='<link rel="canonical" href="/corporate/clean/contact">'), # Should NOT be thin content
        "content_type": "text/html"
    },
    # Archetype 1: Corporate (defective) - Missing canonical, Thin content on about, Contact contradiction
    "/corporate/defective/": {
        "body": make_html("Corporate Home", 'Welcome. <a href="/corporate/defective/about">About</a> <a href="/corporate/defective/contact">Contact</a>', meta='<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Organization", "name": "Corp"}</script>'),
        "content_type": "text/html"
    },
    "/corporate/defective/about": {
        "body": make_html("About Us", "We are a great company.", meta="", thin=True), # Missing canonical, Thin content
        "content_type": "text/html"
    },
    "/corporate/defective/contact": {
        "body": make_html("Contact Us", '<address>123 Fake St, NY</address><script type="application/ld+json">{"@context": "https://schema.org", "@type": "Organization", "contactPoint": {"telephone": "999-9999"}}</script><a href="tel:555-1234">555-1234</a>', meta=""), # Missing canonical, Contact contradiction
        "content_type": "text/html"
    },
    
    # Archetype 2: Ecommerce (clean)
    "/ecommerce/clean/": {
        "body": make_html("Shop Home", 'Buy things! <a href="/ecommerce/clean/product/1">Product 1</a>', meta='<link rel="canonical" href="/ecommerce/clean/">'),
        "content_type": "text/html"
    },
    "/ecommerce/clean/product/1": {
        "body": make_html("Product 1", '<h1>Product 1</h1><p>Buy this great product!</p>' + '<p>Description</p>'*10 + '<a href="/ecommerce/clean/cart">Add to Cart</a>', meta='<link rel="canonical" href="/ecommerce/clean/product/1"><script type="application/ld+json">{"@context": "https://schema.org", "@type": "Product", "name": "Prod 1"}</script>'),
        "content_type": "text/html"
    },
    "/ecommerce/clean/cart": {
        "body": make_html("Cart", "Your cart is empty. Please browse our catalog and add some great items to your cart before proceeding to checkout! <a href='/ecommerce/clean/'>Back</a>", meta='<link rel="canonical" href="/ecommerce/clean/cart">'), # Short page, shouldn't be thin content
        "content_type": "text/html"
    },
    # Archetype 2: Ecommerce (defective) - Missing Product Structured Data, dead end on product
    "/ecommerce/defective/": {
        "body": make_html("Shop Home", 'Buy things! <a href="/ecommerce/defective/product/1">Product 1</a>', meta='<link rel="canonical" href="/ecommerce/defective/">'),
        "content_type": "text/html"
    },
    "/ecommerce/defective/product/1": {
        "body": make_html("Product 1", '<h1>Product 1</h1><p>Buy this great product!</p>' + '<p>Description</p>'*10, meta='<link rel="canonical" href="/ecommerce/defective/product/1">'), # Dead end, missing structured data
        "content_type": "text/html"
    },

    # Archetype 3: Blog (clean)
    "/blog/clean/": {
        "body": make_html("Blog Home", 'Read articles! <a href="/blog/clean/article/1">Article 1</a>', meta='<link rel="canonical" href="/blog/clean/">'),
        "content_type": "text/html"
    },
    "/blog/clean/article/1": {
        "body": make_html("Article 1", '<h1>Article 1</h1><p>Great read.</p>' + '<p>Content</p>'*20 + '<a href="/blog/clean/">Back</a>', meta='<link rel="canonical" href="/blog/clean/article/1"><script type="application/ld+json">{"@context": "https://schema.org", "@type": "Article", "datePublished": "2025-01-01"}</script>'),
        "content_type": "text/html"
    },
    # Archetype 3: Blog (defective) - Stale content
    "/blog/defective/": {
        "body": make_html("Blog Home", 'Read articles! <a href="/blog/defective/article/1">Article 1</a>', meta='<link rel="canonical" href="/blog/defective/">'),
        "content_type": "text/html"
    },
    "/blog/defective/article/1": {
        "body": make_html("Article 1", '<h1>Article 1</h1><p>Great read.</p>' + '<p>Content</p>'*20 + '<p>Copyright 2015</p><a href="/blog/defective/">Back</a>', meta='<link rel="canonical" href="/blog/defective/article/1"><script type="application/ld+json">{"@context": "https://schema.org", "@type": "Article", "datePublished": "2015-01-01"}</script>'), # Stale
        "content_type": "text/html"
    },
    
    # Archetype 4: Docs (clean)
    "/docs/clean/": {
        "body": make_html("Docs", '<h1>Docs</h1><p>Read docs.</p><a href="/docs/clean/guide">Guide</a>', meta='<link rel="canonical" href="/docs/clean/">'),
        "content_type": "text/html"
    },
    "/docs/clean/guide": {
        "body": make_html("Guide", '<h1>Guide</h1><h2>Section 1</h2><p>text</p><h2>Section 2</h2><p>text</p>'*30 + '<a href="/docs/clean/">Back</a>', meta='<link rel="canonical" href="/docs/clean/guide">'), # Long page, but has headings, so not Wall of Text
        "content_type": "text/html"
    },
    # Archetype 4: Docs (defective) - Wall of Text
    "/docs/defective/": {
        "body": make_html("Docs", '<h1>Docs</h1><p>Read docs.</p><a href="/docs/defective/guide">Guide</a>', meta='<link rel="canonical" href="/docs/defective/">'),
        "content_type": "text/html"
    },
    "/docs/defective/guide": {
        "body": make_html("Guide", '<p>' + 'word '*3500 + '</p><a href="/docs/defective/">Back</a>', meta='<link rel="canonical" href="/docs/defective/guide">'), # Wall of text
        "content_type": "text/html"
    },

    # Archetype 5: Portfolio (clean)
    "/portfolio/clean/": {
        "body": make_html("Portfolio", '<h1>My Work</h1><a href="/portfolio/clean/project">Project</a>', meta='<link rel="canonical" href="/portfolio/clean/">'),
        "content_type": "text/html"
    },
    "/portfolio/clean/project": {
        "body": make_html("Project", '<h1>Project</h1><p>Did this project for a wonderful client. It was highly successful and we learned a lot along the way!</p><a href="/portfolio/clean/">Back</a>', meta='<link rel="canonical" href="/portfolio/clean/project">'),
        "content_type": "text/html"
    },
    
    # Archetype 6: SaaS (clean)
    "/saas/clean/": {
        "body": make_html("SaaS", '<h1>SaaS</h1><a href="/saas/clean/login">Login</a>', meta='<link rel="canonical" href="/saas/clean/">'),
        "content_type": "text/html"
    },
    "/saas/clean/login": {
        "body": make_html("Login", '<p>Welcome back! Please enter your username and password below to securely access your personalized SaaS dashboard.</p><form><input type="text"><input type="password"></form>', meta='<link rel="canonical" href="/saas/clean/login">'), # Short utility page, shouldn't be thin content
        "content_type": "text/html"
    },

    # Archetype 7: Media (clean)
    "/media/clean/": {
        "body": make_html("Media", '<h1>Videos</h1><a href="/media/clean/video">Video</a>', meta='<link rel="canonical" href="/media/clean/">'),
        "content_type": "text/html"
    },
    "/media/clean/video": {
        "body": make_html("Video", '<h1>Cool Video</h1><video src="test.mp4"></video><p>Here is a detailed description of this amazing video that contains enough words to not be considered thin.</p><a href="/media/clean/">Back</a>', meta='<link rel="canonical" href="/media/clean/video">'), # Media rich, short text, not thin content
        "content_type": "text/html"
    },

    # Archetype 8: Multilingual
    "/multi/clean/": {
        "body": make_html("Bonjour", '<h1>Bonjour le monde!</h1><p>Ceci est un test.</p>'*10, meta='<link rel="canonical" href="/multi/clean/">'),
        "content_type": "text/html"
    },

    # Archetype 9: JS
    "/js/clean/": {
        "body": make_html("JS", '<h1>JS</h1><a href="/js/clean/page">Page</a>', meta='<link rel="canonical" href="/js/clean/">'),
        "content_type": "text/html"
    },
    "/js/clean/page": {
        "body": make_html("JS Page", '<h1>JS Page</h1><div id="content"></div><script>document.getElementById("content").innerHTML = "<p>Loaded content. This is a JavaScript driven page with enough meaningful text to satisfy the word count requirement.</p>"</script><a href="/js/clean/">Back</a>', meta='<link rel="canonical" href="/js/clean/page">'),
        "content_type": "text/html"
    },

    # Archetype 10: Minimal
    "/minimal/clean/": {
        "body": make_html("Min", 'Hi <a href="/minimal/clean/contact">Contact</a>', meta='<link rel="canonical" href="/minimal/clean/">'),
        "content_type": "text/html"
    },
    "/minimal/clean/contact": {
        "body": make_html("Contact", 'Call 555-5555', meta='<link rel="canonical" href="/minimal/clean/contact">'),
        "content_type": "text/html"
    },

    # Archetype 11: Large
    "/large/clean/": {
        "body": make_html("Large", "<h1>Large</h1>" + "".join([f'<a href="/large/clean/page{i}">Page {i}</a>' for i in range(50)]), meta='<link rel="canonical" href="/large/clean/">'),
        "content_type": "text/html"
    },

    # Archetype 12: Redirects
    "/redirects/clean/": {
        "body": make_html("Redirects", '<a href="/redirects/clean/target">Link</a> <a href="/redirects/clean/redir">Redir Link</a>', meta='<link rel="canonical" href="/redirects/clean/">'),
        "content_type": "text/html"
    },
    "/redirects/clean/redir": {
        "status": 301,
        "location": "/redirects/clean/target" # 1 hop redirect (False positive E)
    },
    "/redirects/clean/target": {
        "body": make_html("Target", '<p>Target</p><a href="/redirects/clean/">Back</a>', meta='<link rel="canonical" href="/redirects/clean/target">'),
        "content_type": "text/html"
    },
    
    "/redirects/defective/": {
        "body": make_html("Redirects", '<a href="/redirects/defective/target">Link</a> <a href="/redirects/defective/chain1">Redir Link</a>', meta='<link rel="canonical" href="/redirects/defective/">'),
        "content_type": "text/html"
    },
    "/redirects/defective/chain1": {
        "status": 301,
        "location": "/redirects/defective/chain2"
    },
    "/redirects/defective/chain2": {
        "status": 301,
        "location": "/redirects/defective/chain3"
    },
    "/redirects/defective/chain3": {
        "status": 301,
        "location": "/redirects/defective/chain4"
    },
    "/redirects/defective/chain4": {
        "status": 301,
        "location": "/redirects/defective/chain5"
    },
    "/redirects/defective/chain5": {
        "status": 301,
        "location": "/redirects/defective/chain6"
    },
    "/redirects/defective/chain6": {
        "status": 301,
        "location": "/redirects/defective/target"
    },
    "/redirects/defective/target": {
        "body": make_html("Target", '<p>Target</p><a href="/redirects/defective/">Back</a>', meta='<link rel="canonical" href="/redirects/defective/target">'),
        "content_type": "text/html"
    },
    
    # Adding Robots and Sitemaps
    "/robots.txt": {
        "body": "User-agent: *\nAllow: /\n",
        "content_type": "text/plain"
    },
}

for i in range(50):
    GENERALIZATION_FIXTURES[f"/large/clean/page{i}"] = {
        "body": make_html(f"Page {i}", f"<h1>Page {i}</h1><p>Content</p><a href=\"/large/clean/\">Back</a>", meta=f'<link rel="canonical" href="/large/clean/page{i}">'),
        "content_type": "text/html"
    }
