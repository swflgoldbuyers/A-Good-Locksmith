#!/usr/bin/env python3
"""Generate location, service, and resource pages for A Good Locksmith."""

from __future__ import annotations

import json
import re
from pathlib import Path

from content_articles import ARTICLE_BY_SLUG, ARTICLES, FEATURED_ARTICLE_SLUGS
from content_cities import ALL_CITY_SLUGS, CITIES
from content_services import ALL_SERVICE_SLUGS, SERVICE_BY_SLUG, SERVICES

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://agoodlocksmith.com"
PHONE_DISPLAY = "(239) 278-5397"
PHONE_TEL = "2392785397"
PHONE_E164 = "+1-239-278-5397"
TODAY = "2026-08-05"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def json_ld(data: dict | list) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def asset(path: str) -> str:
    return f"/{path.lstrip('/')}"


CITY_BY_SLUG = {c["slug"]: c for c in CITIES}


def nav_html(active: str = "") -> str:
    links = [
        ("/", "Home", "home"),
        ("/#services", "Services", "services"),
        ("/resources/", "Resources", "resources"),
        ("/#about", "About", "about"),
        ("/#contact", "Contact", "contact"),
    ]
    items = []
    for href, label, key in links:
        cls = ' class="active-link"' if key == active else ""
        items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    return "\n                ".join(items)


def header_html(active: str = "") -> str:
    return f"""<header class="site-header scrolled">
    <div class="container nav">
        <a href="/" class="brand" aria-label="A Good Locksmith home">
            <img src="{asset('logo-header.png')}" alt="A Good Locksmith" class="brand-logo brand-logo-rect" width="220" height="92">
        </a>
        <nav aria-label="Main navigation">
            <ul class="nav-links">
                {nav_html(active)}
            </ul>
        </nav>
        <a href="tel:{PHONE_TEL}" class="call-button">Call Now</a>
        <button type="button" class="menu-toggle" aria-label="Toggle navigation menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>
</header>"""


def footer_html() -> str:
    service_links = "\n".join(
        f'                    <li><a href="/services/{s["slug"]}/">{esc(s["nav_label"])}</a></li>'
        for s in SERVICES[:8]
    )
    area_links = "\n".join(
        f'                    <li><a href="/locations/{c["slug"]}/">{esc(c["name"])}</a></li>'
        for c in CITIES
    )
    return f"""<footer id="contact">
    <div class="container">
        <div class="footer-grid">
            <div>
                <h3>A GOOD LOCKSMITH</h3>
                <p>
                    Serving Southwest Florida since 1988 with trusted residential,
                    commercial and automotive locksmith services.
                </p>
                <br>
                <p>
                    <strong>Phone</strong><br>
                    <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
                </p>
                <p class="footer-social">
                    <a href="https://www.facebook.com/AGoodLocksmith" class="footer-facebook" target="_blank" rel="noopener noreferrer" aria-label="Visit A Good Locksmith on Facebook">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    </a>
                </p>
            </div>
            <div>
                <h4>Services</h4>
                <ul>
{service_links}
                    <li><a href="/services/">View All Services</a></li>
                </ul>
            </div>
            <div>
                <h4>Service Areas</h4>
                <ul>
{area_links}
                </ul>
            </div>
            <div>
                <h4>Resources</h4>
                <ul>
                    <li><a href="/resources/">Resource Center</a></li>
                    <li><a href="/resources/how-often-should-you-rekey-your-home/">When to Rekey</a></li>
                    <li><a href="/resources/locked-out-of-your-car/">Car Lockout Tips</a></li>
                    <li><a href="/resources/5-signs-its-time-to-replace-your-locks/">Replace Locks</a></li>
                    <li><a href="/#about">About Us</a></li>
                    <li>Serving Since 1988</li>
                    <li>24/7 Emergency Service</li>
                </ul>
            </div>
        </div>
        <div class="footer-trust">
            <span class="footer-trust-item">Serving Southwest Florida Since 1988</span>
            <span class="footer-trust-divider" aria-hidden="true"></span>
            <span class="footer-trust-item">Residential • Commercial • Automotive</span>
            <span class="footer-trust-divider" aria-hidden="true"></span>
            <span class="footer-trust-item">232+ Google Reviews</span>
            <span class="footer-trust-divider" aria-hidden="true"></span>
            <span class="footer-trust-item">24/7 Emergency Service</span>
        </div>
        <div class="footer-bottom">
            © 2026 A Good Locksmith • All Rights Reserved
        </div>
    </div>
</footer>
<a href="tel:{PHONE_TEL}" class="floating-call">
    Need a Locksmith?<br>
    <span>{PHONE_DISPLAY}</span>
</a>
<script src="{asset('script.js')}"></script>"""


def breadcrumbs_html(crumbs: list[tuple[str, str | None]]) -> str:
    parts = ['<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>']
    for i, (label, href) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        if last or not href:
            parts.append(f'<li aria-current="page"><span>{esc(label)}</span></li>')
        else:
            parts.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    parts.append("</ol></nav>")
    return "\n".join(parts)


def breadcrumb_schema(crumbs: list[tuple[str, str | None]]) -> dict:
    elements = []
    for i, (label, href) in enumerate(crumbs, start=1):
        item: dict = {
            "@type": "ListItem",
            "position": i,
            "name": label,
        }
        if href:
            item["item"] = SITE + href if href.startswith("/") else href
        elements.append(item)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }


def faq_schema(faqs: list[dict]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in faqs
        ],
    }


def local_business_schema(city: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Locksmith",
        "name": "A Good Locksmith",
        "url": f"{SITE}/locations/{city['slug']}/",
        "logo": f"{SITE}/LOGO.png",
        "image": f"{SITE}/HERO.webp",
        "telephone": PHONE_E164,
        "description": city["meta_description"],
        "foundingDate": "1988",
        "priceRange": "$$",
        "areaServed": {
            "@type": "City",
            "name": city["name"],
            "containedInPlace": {
                "@type": "AdministrativeArea",
                "name": f"{city['county']} County, Florida",
            },
        },
        "serviceType": [
            "Residential Locksmith",
            "Commercial Locksmith",
            "Automotive Locksmith",
            "Emergency Locksmith",
            "Lock Rekeying",
            "Smart Lock Installation",
        ],
        "sameAs": ["https://www.facebook.com/AGoodLocksmith"],
    }


def service_schema(service: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service["name"],
        "serviceType": service["name"],
        "description": service["meta_description"],
        "url": f"{SITE}/services/{service['slug']}/",
        "provider": {
            "@type": "Locksmith",
            "name": "A Good Locksmith",
            "telephone": PHONE_E164,
            "url": f"{SITE}/",
            "areaServed": [c["name"] for c in CITIES] + ["Southwest Florida"],
        },
        "areaServed": [c["name"] for c in CITIES] + ["Southwest Florida"],
    }


def article_schema(article: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta_description"],
        "image": f"{SITE}/{article['image']}",
        "datePublished": article["date_published"],
        "dateModified": article["date_modified"],
        "author": {"@type": "Organization", "name": "A Good Locksmith"},
        "publisher": {
            "@type": "Organization",
            "name": "A Good Locksmith",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE}/LOGO.png",
            },
        },
        "mainEntityOfPage": f"{SITE}/resources/{article['slug']}/",
    }


def head_html(
    *,
    title: str,
    description: str,
    canonical: str,
    og_title: str,
    og_type: str = "website",
    og_image: str = f"{SITE}/HERO.webp",
    schemas: list[dict] | None = None,
) -> str:
    schema_blocks = ""
    for schema in schemas or []:
        schema_blocks += f'\n<script type="application/ld+json">\n{json_ld(schema)}\n</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="A Good Locksmith">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#B22222">
<meta name="format-detection" content="telephone=yes">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(og_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="A Good Locksmith">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(og_title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('style.css')}">{schema_blocks}
</head>
<body class="inner-page">"""


def page_hero(eyebrow: str, headline: str, sub: str) -> str:
    return f"""<section class="page-hero">
    <div class="overlay"></div>
    <div class="container page-hero-content">
        <span class="page-eyebrow">{esc(eyebrow)}</span>
        <h1>{esc(headline)}</h1>
        <p>{esc(sub)}</p>
        <div class="hero-buttons">
            <a href="tel:{PHONE_TEL}" class="btn-red">Call {PHONE_DISPLAY}</a>
            <a href="/#contact" class="btn-outline">Request Service</a>
        </div>
    </div>
</section>"""


def faq_html(faqs: list[dict]) -> str:
    items = []
    for faq in faqs:
        items.append(
            f"""            <div class="faq-item">
                <button class="faq-question" type="button">
                    <span>{esc(faq["q"])}</span>
                    <span class="faq-icon">+</span>
                </button>
                <div class="faq-answer">
                    <p>{esc(faq["a"])}</p>
                </div>
            </div>"""
        )
    return f"""<section class="faq-section inner-faq">
    <div class="container">
        <div class="section-heading">
            <span>FAQ</span>
            <h2>Frequently Asked Questions</h2>
        </div>
        <div class="faq-list">
{chr(10).join(items)}
        </div>
    </div>
</section>"""


def cta_band(headline: str, text: str) -> str:
    return f"""<section class="cta-band">
    <div class="container cta-band-inner">
        <div>
            <h2>{esc(headline)}</h2>
            <p>{esc(text)}</p>
        </div>
        <a href="tel:{PHONE_TEL}" class="btn-red">Call {PHONE_DISPLAY}</a>
    </div>
</section>"""


def sidebar_services(current: str | None = None) -> str:
    links = []
    for s in SERVICES:
        cls = ' class="is-active"' if s["slug"] == current else ""
        links.append(
            f'<li><a href="/services/{s["slug"]}/"{cls}>{esc(s["nav_label"])}</a></li>'
        )
    return f"""<aside class="page-sidebar">
    <div class="sidebar-card">
        <h3>Our Services</h3>
        <ul class="sidebar-links">
            {chr(10).join(links)}
        </ul>
    </div>
    <div class="sidebar-card sidebar-cta">
        <h3>Need Help Now?</h3>
        <p>Call for fast residential, commercial or automotive locksmith service across Southwest Florida.</p>
        <a href="tel:{PHONE_TEL}" class="btn-red">Call {PHONE_DISPLAY}</a>
    </div>
</aside>"""


def sidebar_locations(current: str | None = None) -> str:
    links = []
    for c in CITIES:
        cls = ' class="is-active"' if c["slug"] == current else ""
        links.append(
            f'<li><a href="/locations/{c["slug"]}/"{cls}>{esc(c["name"])}</a></li>'
        )
    return f"""<div class="sidebar-card">
        <h3>Service Areas</h3>
        <ul class="sidebar-links">
            {chr(10).join(links)}
        </ul>
    </div>"""


def render_sections(sections: list[dict]) -> str:
    blocks = []
    for section in sections:
        blocks.append(
            f"""<section class="content-block">
                <h2>{esc(section["heading"])}</h2>
                {section["html"]}
            </section>"""
        )
    return "\n".join(blocks)


def write_page(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def build_city_page(city: dict) -> None:
    crumbs = [
        ("Home", "/"),
        ("Service Areas", "/locations/"),
        (city["name"], None),
    ]
    canonical = f"{SITE}/locations/{city['slug']}/"
    schemas = [
        local_business_schema(city),
        breadcrumb_schema(crumbs),
        faq_schema(city["faqs"]),
    ]

    neighborhoods = "".join(f"<li>{esc(n)}</li>" for n in city["neighborhoods"])
    landmarks = "".join(f"<li>{esc(n)}</li>" for n in city["landmarks"])
    other_cities = [c for c in CITIES if c["slug"] != city["slug"]]
    nearby = "".join(
        f'<li><a href="/locations/{c["slug"]}/">{esc(c["name"])}</a></li>'
        for c in other_cities[:5]
    )
    service_pills = "".join(
        f'<a class="chip-link" href="/services/{s["slug"]}/">{esc(s["nav_label"])}</a>'
        for s in SERVICES[:8]
    )

    body = f"""{header_html("services")}
{page_hero("LOCKSMITH IN " + city["name"].upper(), city["hero_headline"], city["hero_sub"])}
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="page-layout">
    <div class="container page-layout-grid">
        <div class="page-main">
            <div class="content-block intro-block">
                {city["intro_html"]}
            </div>
            {render_sections(city["sections"])}
            <section class="content-block">
                <h2>Neighborhoods We Serve in {esc(city["name"])}</h2>
                <p>{esc(city["services_blurb"])}</p>
                <ul class="two-col-list">{neighborhoods}</ul>
            </section>
            <section class="content-block">
                <h2>Local Landmarks &amp; Familiar Areas</h2>
                <p>Our technicians regularly serve homes and businesses near the places {esc(city["name"])} residents know best.</p>
                <ul class="two-col-list">{landmarks}</ul>
            </section>
            <section class="content-block">
                <h2>Popular Locksmith Services in {esc(city["name"])}</h2>
                <div class="chip-row">{service_pills}</div>
                <p>Explore <a href="/services/residential-locksmith/">residential</a>, <a href="/services/commercial-locksmith/">commercial</a>, <a href="/services/automotive-locksmith/">automotive</a> and <a href="/services/emergency-locksmith/">emergency locksmith</a> options — or browse our <a href="/resources/">resource center</a> for helpful security guidance.</p>
            </section>
            <section class="content-block">
                <h2>Nearby Communities</h2>
                <ul class="two-col-list">{nearby}</ul>
            </section>
        </div>
        {sidebar_services()}
    </div>
</section>
{faq_html(city["faqs"])}
{cta_band(city["cta_headline"], city["cta_text"])}
{footer_html()}
</body>
</html>"""

    html = (
        head_html(
            title=city["meta_title"],
            description=city["meta_description"],
            canonical=canonical,
            og_title=city["og_title"],
            schemas=schemas,
        )
        + body
    )
    write_page(ROOT / "locations" / city["slug"] / "index.html", html)


def build_service_page(service: dict) -> None:
    crumbs = [
        ("Home", "/"),
        ("Services", "/services/"),
        (service["name"], None),
    ]
    canonical = f"{SITE}/services/{service['slug']}/"
    schemas = [
        service_schema(service),
        breadcrumb_schema(crumbs),
        faq_schema(service["faqs"]),
    ]

    benefits = "".join(f"<li>{esc(b)}</li>" for b in service["benefits"])
    steps = "".join(
        f"""<div class="process-step">
            <span class="process-num">{i:02d}</span>
            <div>
                <h3>{esc(step["title"])}</h3>
                <p>{esc(step["text"])}</p>
            </div>
        </div>"""
        for i, step in enumerate(service["process_steps"], start=1)
    )
    related_svc = "".join(
        f'<a class="chip-link" href="/services/{slug}/">{esc(SERVICE_BY_SLUG[slug]["nav_label"])}</a>'
        for slug in service["related_services"]
        if slug in SERVICE_BY_SLUG
    )
    related_art_cards = []
    for slug in service["related_articles"]:
        if slug not in ARTICLE_BY_SLUG:
            continue
        a = ARTICLE_BY_SLUG[slug]
        related_art_cards.append(
            f'<a class="related-card" href="/resources/{slug}/"><span class="article-category">{esc(a["category"])}</span><strong>{esc(a["title"])}</strong></a>'
        )
    related_art = "".join(related_art_cards)
    city_links = "".join(
        f'<a class="chip-link" href="/locations/{c["slug"]}/">{esc(c["name"])}</a>'
        for c in CITIES
    )
    service_nav = []
    for s in SERVICES:
        active = ' class="is-active"' if s["slug"] == service["slug"] else ""
        service_nav.append(
            f'<li><a href="/services/{s["slug"]}/"{active}>{esc(s["nav_label"])}</a></li>'
        )

    body = f"""{header_html("services")}
{page_hero(service["category"].upper() + " SERVICE", service["hero_headline"], service["hero_sub"])}
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="page-layout">
    <div class="container page-layout-grid">
        <div class="page-main">
            <div class="content-block intro-block">
                {service["intro_html"]}
            </div>
            {render_sections(service["sections"])}
            <section class="content-block">
                <h2>Why Choose A Good Locksmith</h2>
                <ul>{benefits}</ul>
            </section>
            <section class="content-block">
                <h2>How the Process Works</h2>
                <div class="process-list">{steps}</div>
            </section>
            <section class="content-block">
                <h2>Serving Communities Across Southwest Florida</h2>
                <p>We provide {esc(service["name"].lower())} throughout Lee and Collier County, including:</p>
                <div class="chip-row">{city_links}</div>
            </section>
            <section class="content-block">
                <h2>Related Services</h2>
                <div class="chip-row">{related_svc}</div>
            </section>
            <section class="content-block">
                <h2>Helpful Resources</h2>
                <div class="related-grid">{related_art}</div>
            </section>
        </div>
        <aside class="page-sidebar">
            <div class="sidebar-card">
                <h3>Our Services</h3>
                <ul class="sidebar-links">
                    {"".join(service_nav)}
                </ul>
            </div>
            {sidebar_locations()}
            <div class="sidebar-card sidebar-cta">
                <h3>Need {esc(service["name"])}?</h3>
                <p>Call now for fast help across Southwest Florida.</p>
                <a href="tel:{PHONE_TEL}" class="btn-red">Call {PHONE_DISPLAY}</a>
            </div>
        </aside>
    </div>
</section>
{faq_html(service["faqs"])}
{cta_band(service["cta_headline"], service["cta_text"])}
{footer_html()}
</body>
</html>"""

    html = (
        head_html(
            title=service["meta_title"],
            description=service["meta_description"],
            canonical=canonical,
            og_title=service["og_title"],
            schemas=schemas,
        )
        + body
    )
    write_page(ROOT / "services" / service["slug"] / "index.html", html)


def build_article_page(article: dict) -> None:
    crumbs = [
        ("Home", "/"),
        ("Resources", "/resources/"),
        (article["title"], None),
    ]
    canonical = f"{SITE}/resources/{article['slug']}/"
    schemas = [article_schema(article), breadcrumb_schema(crumbs)]
    if article.get("faqs"):
        schemas.append(faq_schema(article["faqs"]))

    related_svc = "".join(
        f'<a class="chip-link" href="/services/{slug}/">{esc(SERVICE_BY_SLUG[slug]["nav_label"])}</a>'
        for slug in article["related_services"]
        if slug in SERVICE_BY_SLUG
    )
    related_art = "".join(
        f'<a class="related-card" href="/resources/{slug}/"><span class="article-category">{esc(ARTICLE_BY_SLUG[slug]["category"])}</span><strong>{esc(ARTICLE_BY_SLUG[slug]["title"])}</strong><span>{esc(ARTICLE_BY_SLUG[slug]["excerpt"])}</span></a>'
        for slug in article["related_articles"]
        if slug in ARTICLE_BY_SLUG and slug != article["slug"]
    )[:3]  # keep string short - actually this slices chars not items. Fix below.

    # rebuild related articles properly
    related_cards = []
    for slug in article["related_articles"]:
        if slug not in ARTICLE_BY_SLUG or slug == article["slug"]:
            continue
        a = ARTICLE_BY_SLUG[slug]
        related_cards.append(
            f'<a class="related-card" href="/resources/{slug}/"><span class="article-category">{esc(a["category"])}</span><strong>{esc(a["title"])}</strong><span>{esc(a["excerpt"])}</span></a>'
        )
        if len(related_cards) >= 3:
            break
    related_art = "".join(related_cards)

    faq_block = faq_html(article["faqs"]) if article.get("faqs") else ""

    body = f"""{header_html("resources")}
<section class="page-hero article-hero">
    <div class="overlay"></div>
    <div class="container page-hero-content">
        <span class="page-eyebrow">{esc(article["category"].upper())}</span>
        <h1>{esc(article["title"])}</h1>
        <p class="article-meta">{esc(article["read_time"])} · Updated {esc(article["date_modified"])}</p>
    </div>
</section>
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="page-layout">
    <div class="container page-layout-grid">
        <article class="page-main article-main">
            <div class="article-feature-image">
                <img src="{asset(article["image"])}" alt="{esc(article["image_alt"])}" loading="lazy" width="1200" height="675">
            </div>
            <div class="content-block intro-block">
                {article["intro_html"]}
            </div>
            {render_sections(article["sections"])}
            <section class="content-block">
                <h2>Related Locksmith Services</h2>
                <div class="chip-row">{related_svc}</div>
            </section>
            <section class="content-block">
                <h2>Keep Reading</h2>
                <div class="related-grid">{related_art}</div>
            </section>
        </article>
        <aside class="page-sidebar">
            <div class="sidebar-card sidebar-cta">
                <h3>Talk to a Locksmith</h3>
                <p>Questions about locks, keys or security upgrades? Call A Good Locksmith.</p>
                <a href="tel:{PHONE_TEL}" class="btn-red">Call {PHONE_DISPLAY}</a>
            </div>
            {sidebar_locations()}
            <div class="sidebar-card">
                <h3>Popular Services</h3>
                <ul class="sidebar-links">
                    {"".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["nav_label"])}</a></li>' for s in SERVICES[:8])}
                </ul>
            </div>
        </aside>
    </div>
</section>
{faq_block}
{cta_band("Need Professional Locksmith Help?", "A Good Locksmith has served Southwest Florida since 1988. Call for residential, commercial or automotive service.")}
{footer_html()}
</body>
</html>"""

    html = (
        head_html(
            title=article["meta_title"],
            description=article["meta_description"],
            canonical=canonical,
            og_title=article["og_title"],
            og_type="article",
            og_image=f"{SITE}/{article['image']}",
            schemas=schemas,
        )
        + body
    )
    write_page(ROOT / "resources" / article["slug"] / "index.html", html)


def build_locations_index() -> None:
    crumbs = [("Home", "/"), ("Service Areas", None)]
    cards = "".join(
        f"""<a class="directory-card" href="/locations/{c["slug"]}/">
            <span class="directory-kicker">{esc(c["county"])} County</span>
            <h2>{esc(c["name"])}</h2>
            <p>{esc(c["hero_sub"])}</p>
            <span class="directory-link">View {esc(c["name"])} locksmith services →</span>
        </a>"""
        for c in CITIES
    )
    canonical = f"{SITE}/locations/"
    schemas = [
        breadcrumb_schema(crumbs),
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Locksmith Service Areas in Southwest Florida",
            "url": canonical,
            "description": "A Good Locksmith serves Bonita Springs, Estero, Naples, Fort Myers, North Fort Myers, Cape Coral, Lehigh Acres and San Carlos Park.",
        },
    ]
    body = f"""{header_html("services")}
{page_hero("SERVICE AREAS", "Locksmith Services Across Southwest Florida", "Fast, dependable locksmith service throughout Lee and Collier County since 1988.")}
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="directory-section">
    <div class="container">
        <div class="directory-grid">{cards}</div>
    </div>
</section>
{cta_band("Need a Locksmith Near You?", "Call A Good Locksmith for residential, commercial and automotive service across Southwest Florida.")}
{footer_html()}
</body>
</html>"""
    html = head_html(
        title="Locksmith Service Areas | Southwest Florida | A Good Locksmith",
        description="Find local locksmith services in Bonita Springs, Estero, Naples, Fort Myers, North Fort Myers, Cape Coral, Lehigh Acres and San Carlos Park.",
        canonical=canonical,
        og_title="Locksmith Service Areas | A Good Locksmith",
        schemas=schemas,
    ) + body
    write_page(ROOT / "locations" / "index.html", html)


def build_services_index() -> None:
    crumbs = [("Home", "/"), ("Services", None)]
    cards = "".join(
        f"""<a class="directory-card" href="/services/{s["slug"]}/">
            <span class="directory-kicker">{esc(s["category"])}</span>
            <h2>{esc(s["name"])}</h2>
            <p>{esc(s["hero_sub"])}</p>
            <span class="directory-link">Learn more →</span>
        </a>"""
        for s in SERVICES
    )
    canonical = f"{SITE}/services/"
    schemas = [
        breadcrumb_schema(crumbs),
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Locksmith Services",
            "url": canonical,
        },
    ]
    body = f"""{header_html("services")}
{page_hero("OUR SERVICES", "Professional Locksmith Services", "Residential, commercial, automotive and emergency locksmith solutions for Southwest Florida.")}
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="directory-section">
    <div class="container">
        <div class="directory-grid">{cards}</div>
    </div>
</section>
{cta_band("Ready to Get Started?", f"Call {PHONE_DISPLAY} for honest pricing and dependable locksmith service.")}
{footer_html()}
</body>
</html>"""
    html = head_html(
        title="Locksmith Services | Residential, Commercial & Automotive | A Good Locksmith",
        description="Explore residential, commercial, automotive and emergency locksmith services from A Good Locksmith — serving Southwest Florida since 1988.",
        canonical=canonical,
        og_title="Locksmith Services | A Good Locksmith",
        schemas=schemas,
    ) + body
    write_page(ROOT / "services" / "index.html", html)


def build_resources_index() -> None:
    crumbs = [("Home", "/"), ("Resources", None)]
    cards = "".join(
        f"""<article class="article-card">
            <div class="article-image">
                <img src="{asset(a["image"])}" alt="{esc(a["image_alt"])}" loading="lazy" width="640" height="400">
            </div>
            <div class="article-body">
                <span class="article-category">{esc(a["category"])}</span>
                <h3><a href="/resources/{a["slug"]}/">{esc(a["title"])}</a></h3>
                <p>{esc(a["excerpt"])}</p>
                <a href="/resources/{a["slug"]}/" class="btn-red article-read-more">Read More</a>
            </div>
        </article>"""
        for a in ARTICLES
    )
    canonical = f"{SITE}/resources/"
    item_list = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Locksmith Resource Center",
        "url": canonical,
        "description": "Helpful locksmith tips, security advice and guides from A Good Locksmith.",
        "hasPart": [
            {
                "@type": "BlogPosting",
                "headline": a["title"],
                "url": f"{SITE}/resources/{a['slug']}/",
                "description": a["meta_description"],
            }
            for a in ARTICLES
        ],
    }
    body = f"""{header_html("resources")}
{page_hero("RESOURCE CENTER", "Locksmith Tips & Security Guidance", "Practical advice from Southwest Florida locksmith experts — trusted local guidance since 1988.")}
<div class="container breadcrumb-wrap">
{breadcrumbs_html(crumbs)}
</div>
<section class="resource-center-section directory-resources">
    <div class="container">
        <div class="article-grid resources-grid">{cards}</div>
    </div>
</section>
{cta_band("Need Hands-On Help?", f"Call {PHONE_DISPLAY} for lockouts, rekeying, installations and more.")}
{footer_html()}
</body>
</html>"""
    html = head_html(
        title="Locksmith Resource Center | Security Tips & Guides | A Good Locksmith",
        description="Browse locksmith tips, home security guides and automotive advice from A Good Locksmith, serving Southwest Florida since 1988.",
        canonical=canonical,
        og_title="Locksmith Resource Center | A Good Locksmith",
        schemas=[breadcrumb_schema(crumbs), item_list],
    ) + body
    write_page(ROOT / "resources" / "index.html", html)


def build_sitemap() -> None:
    urls = [
        ("/", "1.0", "weekly"),
        ("/locations/", "0.9", "weekly"),
        ("/services/", "0.9", "weekly"),
        ("/resources/", "0.9", "weekly"),
    ]
    for c in CITIES:
        urls.append((f"/locations/{c['slug']}/", "0.8", "monthly"))
    for s in SERVICES:
        urls.append((f"/services/{s['slug']}/", "0.8", "monthly"))
    for a in ARTICLES:
        urls.append((f"/resources/{a['slug']}/", "0.7", "monthly"))

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq in urls:
        parts.append(
            f"""  <url>
    <loc>{SITE}{path}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8")
    print("Wrote sitemap.xml")


def build_llms() -> None:
    service_lines = "\n".join(f"- {s['name']}: {SITE}/services/{s['slug']}/" for s in SERVICES)
    city_lines = "\n".join(f"- {c['name']}: {SITE}/locations/{c['slug']}/" for c in CITIES)
    article_lines = "\n".join(f"- {a['title']}: {SITE}/resources/{a['slug']}/" for a in ARTICLES)
    text = f"""# A Good Locksmith

Website:
{SITE}/

Business:
A Good Locksmith

Description:
Residential, commercial, and automotive locksmith serving Southwest Florida since 1988.

Phone:
{PHONE_DISPLAY}

Founded:
1988

Primary Service Area:
Bonita Springs
Estero
Naples
San Carlos Park
Fort Myers
North Fort Myers
Lehigh Acres
Cape Coral
Southwest Florida

Services:
{service_lines}

City Pages:
{city_lines}

Resource Center:
{SITE}/resources/

Articles:
{article_lines}

Website Purpose:
Provide trustworthy locksmith information and connect customers with professional locksmith services throughout Southwest Florida.
"""
    (ROOT / "llms.txt").write_text(text, encoding="utf-8")
    print("Wrote llms.txt")


def main() -> None:
    for city in CITIES:
        build_city_page(city)
    for service in SERVICES:
        build_service_page(service)
    for article in ARTICLES:
        build_article_page(article)
    build_locations_index()
    build_services_index()
    build_resources_index()
    build_sitemap()
    build_llms()
    print(
        f"Done. Generated {len(CITIES)} cities, {len(SERVICES)} services, {len(ARTICLES)} articles."
    )


if __name__ == "__main__":
    main()
