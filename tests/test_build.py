"""Tests for the FFXIV Ocean Fishing Guide build.

Run with:
    python3 -m unittest discover tests -v
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import build as build_module  # noqa: E402


class RenderInlineTests(unittest.TestCase):
    def test_bold(self):
        self.assertEqual(build_module.render_inline("bronze **and** calm"),
                         "bronze <strong>and</strong> calm")

    def test_italic(self):
        self.assertEqual(build_module.render_inline("stay *patient*"),
                         "stay <em>patient</em>")

    def test_inline_code(self):
        self.assertEqual(build_module.render_inline("read `fish-finder`"),
                         "read <code>fish-finder</code>")

    def test_link(self):
        html = build_module.render_inline("see [Glossary](glossary.md) next")
        self.assertEqual(html, 'see <a href="glossary.md">Glossary</a> next')

    def test_html_is_escaped(self):
        html = build_module.render_inline("<script>&</script>")
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_code_block_not_bolded(self):
        html = build_module.render_inline("`**not bold**`")
        self.assertEqual(html, "<code>**not bold**</code>")


class BlockTests(unittest.TestCase):
    def test_headings(self):
        html = build_module.render_markdown("## About\n\n### Deep")
        self.assertIn("<h2>About</h2>", html)
        self.assertIn("<h3>Deep</h3>", html)
        self.assertNotIn("<h1>", html)

    def test_paragraphs_merge_consecutive_lines(self):
        html = build_module.render_markdown("one two\nthree four")
        self.assertEqual(html, "<p>one two three four</p>")

    def test_unordered_list(self):
        html = build_module.render_markdown("- alpha\n- beta")
        self.assertIn("<ul>", html)
        self.assertIn("<li>alpha</li>", html)
        self.assertIn("<li>beta</li>", html)
        self.assertIn("</ul>", html)

    def test_ordered_list(self):
        html = build_module.render_markdown("1. Cast\n2. Hook")
        self.assertIn("<ol>", html)
        self.assertIn("<li>Cast</li>", html)
        self.assertIn("</ol>", html)

    def test_checklist_boxes(self):
        html = build_module.render_markdown("- [ ] unchecked\n- [x] done")
        self.assertIn('type="checkbox"', html)
        self.assertIn("checked", html)
        self.assertIn("unchecked", html)
        self.assertIn("</li>", html)

    def test_table_structure(self):
        md = ("| A | B |\n"
              "| --- | --- |\n"
              "| 1 | 2 |")
        html = build_module.render_markdown(md)
        self.assertIn("<table>", html)
        self.assertIn("<th>A</th>", html)
        self.assertIn("<td>2</td>", html)

    def test_table_with_inline_markdown(self):
        md = ("| Name | Link |\n"
              "| --- | --- |\n"
              "| Guide | [docs](boats.md) |")
        html = build_module.render_markdown(md)
        self.assertIn('<a href="boats.md">docs</a>', html)

    def test_blockquote(self):
        html = build_module.render_markdown("> kind words")
        self.assertIn("<blockquote>kind words</blockquote>", html)

    def test_horizontal_rule(self):
        html = build_module.render_markdown("---\n\nafter")
        self.assertIn("<hr>", html)
        self.assertIn("<p>after</p>", html)

    def test_verify_date_detected(self):
        text = "Lead-in.\n\nLast hand-checked: **2026-10-31**\n"
        self.assertEqual(build_module.render_verify_banner(text), "2026-10-31")

    def test_missing_verify_date(self):
        self.assertIsNone(build_module.render_verify_banner("No stamp here."))

    def test_table_body_vs_separator(self):
        md = "| Day | Sea |\n| --- | --- |\n| Mon | calm |"
        html = build_module.render_markdown(md)
        # Separator row must not leak into the body.
        self.assertNotIn("<td>---</td>", html)
        self.assertNotIn("<td> </td>", html)


class PageTemplateTests(unittest.TestCase):
    def test_page_includes_skin_and_footer(self):
        page = build_module._page_html("T", "<p>body</p>", "2026-10-31", "<nav></nav>")
        self.assertIn('<link rel="stylesheet" href="style.css">', page)
        self.assertIn("Hand-maintained page", page)
        self.assertIn("2026-10-31", page)
        self.assertIn("Asdale Dynamics, LLC", page)

    def test_no_verify_date_means_no_banner(self):
        page = build_module._page_html("T", "<p>body</p>", None, "<nav></nav>")
        self.assertNotIn("verify-badge", page)

    def test_title_escaped(self):
        page = build_module._page_html('T & <b>x</b>', "", None, "")
        self.assertIn("T &amp; &lt;b&gt;x&lt;/b&gt;", page)


class FilesystemTests(unittest.TestCase):
    def test_build_site_from_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "static").mkdir()
            (root / "docs" / "a.md").write_text(
                "# Guide A\n\nLast hand-checked: **2026-10-31**\n\n| W |\n| --- |\n| x |\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "# Guide Home\n\nBody.\n", encoding="utf-8"
            )
            (root / "static" / "style.css").write_text("body {}\n", encoding="utf-8")

            written = build_module.build_site(root)
            names = {p.name for p in written}
            self.assertIn("index.html", names)
            self.assertIn("a.html", names)
            self.assertIn("style.css", names)
            self.assertEqual(len(written), 3)

            doc_page = (root / "site" / "a.html").read_text(encoding="utf-8")
            home_page = (root / "site" / "index.html").read_text(encoding="utf-8")
            for page in (doc_page, home_page):
                self.assertIn('<a href="index.html">Home</a>', page)
                self.assertIn('<a href="a.html">Guide A</a>', page)

    def test_missing_docs_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# X\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                build_module.build_site(root)


class RepoSmokeTests(unittest.TestCase):
    """Smoke checks against the real repository content."""

    def setUp(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        self.readme_html = build_module.render_markdown(readme)
        docs = sorted((PROJECT_ROOT / "docs").glob("*.md"))
        self.docs = docs
        self.doc_texts = {p: p.read_text(encoding="utf-8") for p in docs}

    def test_all_docs_render(self):
        for path, text in self.doc_texts.items():
            with self.subTest(doc=path.name):
                html = build_module.render_markdown(text)
                self.assertIn("<h1>", html)
                self.assertIn("<h2>", html)

    def test_every_doc_carries_verify_date(self):
        for path, text in self.doc_texts.items():
            with self.subTest(doc=path.name):
                self.assertIsNotNone(
                    build_module.render_verify_banner(text),
                    f"{path.name} is missing a 'Last hand-checked: **date**' stamp",
                )

    def test_verify_date_format(self):
        date_re = re.compile(r"Last hand-checked:\s*\*\*(\d{4}-\d{2}-\d{2})\*\*")
        for path, text in self.doc_texts.items():
            found = date_re.findall(text)
            self.assertTrue(
                found,
                f"{path.name} verify stamp must be YYYY-MM-DD",
            )

    def test_docs_reference_each_other(self):
        text = "\n".join(self.doc_texts.values())
        for needed in ("01-voyage-windows.md", "02-hourly-boils.md",
                       "03-weather-and-expectations.md",
                       "04-bait-rotation-cards.md",
                       "05-achievement-hunts.md",
                       "06-patience-tips.md",
                       "voyage-checklist.md",
                       "glossary.md"):
            self.assertIn(needed, text)

    def test_readme_mentions_ethos(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        for needle in ("Asdale Dynamics, LLC", "verify date",
                       "no scraping", "no account data"):
            self.assertIn(needle.lower(), readme.lower())
        html = self.readme_html
        self.assertIn("MIT", html)

    def test_no_flags_of_automation(self):
        for path in list(self.docs) + [PROJECT_ROOT / "README.md",
                                       PROJECT_ROOT / "build.py"]:
            text = path.read_text(encoding="utf-8").lower()
            with self.subTest(file=path.name):
                self.assertNotIn("requests.get", text)
                self.assertNotIn("urllib.request.urlopen", text)
                self.assertNotIn("selenium", text)

    def test_license_copyright_line_exact(self):
        license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)
        self.assertIn("MIT License", license_text)

    def test_readme_credits_llc(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", readme)


if __name__ == "__main__":
    unittest.main()
