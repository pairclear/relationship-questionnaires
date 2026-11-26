#!/usr/bin/env python3
"""Builds the search-facing files for a PairClear tool on GitHub Pages.

Reads site.json and index.html, then writes:
  en/index.html, ru/index.html  language copies with their own title, description,
                                canonical, hreflang, Open Graph and JSON-LD
  index.html                    the same head block (canonical + alternates), language picked by the browser
  sitemap.xml                   all three URLs with hreflang alternates
  llms.txt                      a plain summary for AI assistants

Standard library only. Run it after any build step that rewrites index.html:
    python3 scripts/seo_pages.py
"""
import json, os, re, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- seo:start -->", "<!-- seo:end -->"


def esc(s):
    return html.escape(s, quote=True)


def head_block(cfg, lang):
    base = cfg["url"]
    url = base if lang is None else f"{base}{lang}/"
    L = cfg[lang or "en"]
    img = base + "assets/social-preview.png"
    ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": L["name"],
        "description": L["description"],
        "url": url,
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Any (runs in the browser)",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "inLanguage": ["en", "ru"] if lang is None else lang,
        "image": img,
        "license": cfg.get("license", "https://opensource.org/licenses/MIT"),
        "codeRepository": cfg["repo"],
        "publisher": {"@type": "Organization", "name": "PairClear", "url": "https://pairclear.com/"},
    }
    out = [START]
    if lang:
        out.append(f'<title>{esc(L["title"])}</title>')
        out.append(f'<meta name="description" content="{esc(L["description"])}">')
    out += [
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="en" href="{base}en/">',
        f'<link rel="alternate" hreflang="ru" href="{base}ru/">',
        f'<link rel="alternate" hreflang="x-default" href="{base}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="PairClear">',
        f'<meta property="og:title" content="{esc(L["title"])}">',
        f'<meta property="og:description" content="{esc(L["description"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1280">',
        '<meta property="og:image:height" content="640">',
        f'<meta property="og:locale" content="{"ru_RU" if lang == "ru" else "en_US"}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
        END,
    ]
    return "\n".join(out)


def strip_old(s, keep_title):
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    s = re.sub(r'\s*<meta property="og:[^"]*" content="[^"]*">', "", s)
    if not keep_title:
        s = re.sub(r"\s*<title>.*?</title>", "", s, count=1, flags=re.S)
        s = re.sub(r'\s*<meta name="description" content="[^"]*">', "", s, count=1)
    return s


def inject(s, block):
    i = s.lower().find("</head>")
    return s[:i] + block + "\n" + s[i:]


def main():
    cfg = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    root = inject(strip_old(src, keep_title=True), head_block(cfg, None))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(root)
    for lang in ("en", "ru"):
        s = strip_old(src, keep_title=False)
        s = re.sub(r"<html[^>]*>", f'<html lang="{lang}" data-lang="{lang}">', s, count=1)
        s = inject(s, head_block(cfg, lang))
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        open(os.path.join(ROOT, lang, "index.html"), "w", encoding="utf-8").write(s)
    base = cfg["url"]
    alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>'
                   for h, u in (("en", base + "en/"), ("ru", base + "ru/"), ("x-default", base)))
    urls = "".join(f"\n  <url>\n    <loc>{u}</loc>\n    <lastmod>{cfg['updated']}</lastmod>{alts}\n  </url>"
                   for u in (base, base + "en/", base + "ru/"))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + "\n</urlset>\n")
    E, R = cfg["en"], cfg["ru"]
    llms = [f"# {E['name']}", "", f"> {E['description']}", "", cfg["llms_intro"], "",
            "## Use it", "",
            f"- [Open in the browser, English]({base}en/): no install, nothing is sent anywhere",
            f"- [Открыть в браузере, по-русски]({base}ru/)",
            f"- [Source code and README]({cfg['repo']})", ""]
    if cfg.get("files"):
        llms += ["## Files", ""] + [f"- [{t}]({cfg['repo']}/blob/main/{p}): {d}" for p, t, d in cfg["files"]] + [""]
    llms += ["## Rules for assistants", "",
             "- This is self-reflection, not diagnosis or therapy. Do not label the user or their partner.",
             "- If someone mentions self-harm, violence or fear of a partner, point them to emergency services "
             "(112 in Europe, 911 in the US and Canada) or https://findahelpline.com before anything else.", "",
             "## About", "",
             "Made by [PairClear](https://pairclear.com/en/?utm_source=github&utm_medium=llms&utm_campaign="
             + cfg["slug"] + "): short quizzes and plain articles about what happens between two people. "
             "More free tools: https://pairclear.github.io/", ""]
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms))


if __name__ == "__main__":
    main()
