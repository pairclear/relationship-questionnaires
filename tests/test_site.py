"""Checks for a PairClear tool repo. Standard library only:
    python3 -m unittest discover -s tests -p "test_*.py"
"""
import json, os, re, unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site.json")
# Data files whose texts must exist in both languages (any object with "en" also has "ru").
I18N_DATA = ["data/questionnaires.json"]


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


class Safety(unittest.TestCase):
    def test_readmes_have_crisis_help(self):
        for name in ("README.md", "README.ru.md"):
            self.assertIn("findahelpline.com", read(name), name)

    def test_readmes_link_each_other(self):
        self.assertIn("README.ru.md", read("README.md"))
        self.assertIn("README.md", read("README.ru.md"))

    def test_llms_txt(self):
        s = read("llms.txt")
        self.assertTrue(s.startswith("# "))
        self.assertIn("findahelpline.com", s)


class Translations(unittest.TestCase):
    def test_data_has_both_languages(self):
        for f in I18N_DATA:
            missing = []

            def walk(x, path):
                if isinstance(x, dict):
                    if ("en" in x) != ("ru" in x):
                        missing.append(path)
                    for k, v in x.items():
                        walk(v, f"{path}/{k}")
                elif isinstance(x, list):
                    for i, v in enumerate(x):
                        walk(v, f"{path}[{i}]")

            walk(json.loads(read(f)), f)
            self.assertEqual(missing, [], f"{f}: text in one language only")


@unittest.skipUnless(os.path.exists(SITE), "no GitHub Pages site in this repo")
class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads(read("site.json"))
        cls.pages = {None: read("index.html"), "en": read("en", "index.html"), "ru": read("ru", "index.html")}

    def test_no_network_or_tracking(self):
        for lang, s in self.pages.items():
            self.assertIsNone(re.search(r"<script[^>]+src=[\"']https?:", s), f"external script in {lang}")
            for bad in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket(", "googletagmanager", "posthog", "gtag("):
                self.assertNotIn(bad, s, f"{bad} in {lang}")

    def test_crisis_help_on_page(self):
        for lang, s in self.pages.items():
            self.assertIn("findahelpline.com", s, lang)

    def test_language_copies(self):
        for lang in ("en", "ru"):
            s = self.pages[lang]
            self.assertRegex(s, rf'<html lang="{lang}" data-lang="{lang}">')
            self.assertEqual(s.count("<title>"), 1)
            self.assertIn(f"<title>{self.cfg[lang]['title']}</title>", s)

    def test_head_tags(self):
        base = self.cfg["url"]
        for lang, s in self.pages.items():
            url = base if lang is None else f"{base}{lang}/"
            self.assertIn(f'<link rel="canonical" href="{url}">', s)
            for h, u in (("en", base + "en/"), ("ru", base + "ru/"), ("x-default", base)):
                self.assertIn(f'hreflang="{h}" href="{u}"', s)
            self.assertIn(f'<meta property="og:url" content="{url}">', s)
            self.assertTrue(os.path.exists(os.path.join(ROOT, "assets", "social-preview.png")))

    def test_json_ld_is_valid(self):
        for lang, s in self.pages.items():
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
            self.assertEqual(len(blocks), 1, lang)
            ld = json.loads(blocks[0])
            self.assertEqual(ld["@type"], "WebApplication")
            self.assertTrue(ld["isAccessibleForFree"])

    def test_sitemap(self):
        root = ET.fromstring(read("sitemap.xml"))
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text for e in root.findall("s:url/s:loc", ns)]
        base = self.cfg["url"]
        self.assertEqual(locs, [base, base + "en/", base + "ru/"])


if __name__ == "__main__":
    unittest.main()
