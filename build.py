#!/usr/bin/env python3
"""Build script for the FFXIV Ocean Fishing Guide.

Converts the hand-maintained Markdown under ``docs/`` (plus README.md, which
becomes the homepage) into a small, plain, fully-offline static HTML site
under ``site/``.

Ethos enforced by design: no network calls, no third-party dependencies, no
game-data scraping, no account data. The site is a review copy of the manual.

Usage:
    ./build.py
    python3 build.py
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DOCS_DIR = PROJECT_ROOT / "docs"
SITE_DIR = PROJECT_ROOT / "site"

PROJECT_NAME = "FFXIV Ocean Fishing Guide"
PROJECT_TAGLINE = "A fan-made manual without the spreadsheets"
FOOTER = (
    "&#169; 2026 Asdale Dynamics, LLC &middot; "
    "Fan-made guide, not affiliated with or endorsed by Square Enix &middot; "
    "All tables hand-maintained with verify dates &middot; "
    "No automation, no scraping, no account data."
)

VERIFY_DATE_RE = re.compile(r"Last hand-checked:\s*\*\*([^*]+)\*\*")


# ---------------------------------------------------------------------------
# Inline markdown -> HTML
# ---------------------------------------------------------------------------

def render_inline(text: str) -> str:
    """Convert inline Markdown (code, bold, italic, links) to HTML.

    The raw text is HTML-escaped first, so document authors can safely write
    characters like < and & without breaking page structure.
    """
    escaped = html.escape(text, quote=False)

    # Inline code first: stored as placeholders so nothing else rewrites it.
    code_spans: list[str] = []

    def _stash_code(match: re.Match) -> str:
        code_spans.append("<code>%s</code>" % match.group(1))
        return "\x00%d\x00" % (len(code_spans) - 1)

    escaped = re.sub(r"`([^`]+)`", _stash_code, escaped)
    # Images: ![alt](src) -> alt text only (site stays offline, no assets to track).
    escaped = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r"\1", escaped)
    # Links [text](target)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)),
        escaped,
    )
    # Bold then italic.
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", escaped)

    # Restore code spans.
    for index, span in enumerate(code_spans):
        escaped = escaped.replace("\x00%d\x00" % index, span)
    return escaped


def render_verify_banner(text: str) -> str | None:
    """Return the first verify date found in the document, if any."""
    dates = VERIFY_DATE_RE.findall(text)
    return dates[0] if dates else None


# ---------------------------------------------------------------------------
# Block-level markdown -> HTML
# ---------------------------------------------------------------------------

def _table_html(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header, body = rows[0], rows[2:]
    parts: list[str] = ["<table>"]
    parts.append("<thead><tr>")
    parts.extend("<th>%s</th>" % render_inline(cell) for cell in header)
    parts.append("</tr></thead>")
    if body:
        parts.append("<tbody>")
        for row in body:
            cells = row + [""] * (len(header) - len(row))
            parts.append("<tr>")
            parts.extend("<td>%s</td>" % render_inline(cell) for cell in cells[: len(header)])
            parts.append("</tr>")
        parts.append("</tbody>")
    parts.append("</table>")
    return "".join(parts)


def _is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_table_separator(line: str) -> bool:
    if not _is_table_row(line):
        return False
    cells = _split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def _checkbox_html(content: str) -> str | None:
    match = re.match(r"^\[([ xX])\]\s+(.*)$", content)
    if not match:
        return None
    state, label = match.group(1), match.group(2)
    checked = " checked" if state in ("x", "X") else ""
    box = f'<input type="checkbox" disabled{checked}>'
    return f'<li class="checklist-item">{box} {render_inline(label)}</li>'


def render_markdown(text: str) -> str:
    """Convert a constrained subset of Markdown to clean HTML.

    Supported: ATX headings (# .. ######), paragraphs, unordered/ordered
    lists, task-list checkboxes, pipe tables, blockquotes, horizontal rules,
    and the inline constructs in :func:`render_inline`.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []

    paragraph: list[str] = []
    open_list: str | None = None  # "ul" / "ol" while a list is open
    quote: list[str] = []
    table_rows: list[list[str]] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>%s</p>" % render_inline(" ".join(paragraph).strip()))
            paragraph.clear()

    def flush_list() -> None:
        nonlocal open_list
        if open_list:
            out.append(f"</{open_list}>")
            open_list = None

    def flush_quote() -> None:
        if quote:
            out.append("<blockquote>%s</blockquote>" % render_inline(" ".join(quote).strip()))
            quote.clear()

    def flush_table() -> None:
        if table_rows:
            out.append(_table_html(table_rows))
            table_rows.clear()

    def flush_all() -> None:
        flush_paragraph()
        flush_list()
        flush_quote()
        flush_table()

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        # Table rows.
        if _is_table_row(stripped):
            flush_paragraph()
            flush_list()
            flush_quote()
            table_rows.append(_split_table_row(stripped))
            continue
        flush_table()

        # Blank line closes open blocks.
        if not stripped:
            flush_all()
            continue

        # Headings.
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_all()
            level = len(heading.group(1))
            out.append("<h%d>%s</h%d>" % (level, render_inline(heading.group(2)), level))
            continue

        # Horizontal rules.
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            flush_all()
            out.append("<hr>")
            continue

        # Blockquotes.
        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            quote.append(stripped.lstrip("> ").strip())
            continue

        # Lists.
        unordered = re.match(r"^[-*]\s+(.*)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.*)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            flush_quote()
            flush_table()
            content = (unordered or ordered).group(1)
            tag = "ul" if unordered else "ol"
            if open_list and open_list != tag:
                flush_list()
            if not open_list:
                out.append(f"<{tag}>")
                open_list = tag
            checkbox = _checkbox_html(content)
            if checkbox:
                out.append(checkbox)
            else:
                out.append("<li>%s</li>" % render_inline(content))
            continue

        # Paragraph text.
        paragraph.append(stripped)

    flush_all()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Site assembly
# ---------------------------------------------------------------------------

def _first_heading(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return re.sub(r"^#{1,6}\s*", "", line).strip()
    return "Untitled page"


def _page_html(title: str, body: str, verify_date: str | None, nav: str) -> str:
    banner = ""
    if verify_date:
        banner = (
            '<p class="verify-badge">Hand-maintained page, last checked by a human on '
            "<strong>%s</strong></p>" % html.escape(verify_date)
        )
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)} — {PROJECT_NAME}</title>\n"
        '<link rel="stylesheet" href="style.css">\n'
        "</head>\n"
        "<body>\n"
        '<header class="site-header">\n'
        f'<h1><a href="index.html">{PROJECT_NAME}</a></h1>\n'
        f'<p class="tagline">{PROJECT_TAGLINE}</p>\n'
        f"<nav>{nav}</nav>\n"
        "</header>\n"
        "<main>\n"
        f"{banner}\n"
        f"{body}\n"
        "</main>\n"
        f"<footer><p>{FOOTER}</p></footer>\n"
        "</body>\n"
        "</html>\n"
    )


def _nav_label(title: str, dest: Path) -> str:
    if dest.name == "index.html":
        return "Home"
    # Strip "1. " style doc numbering for nav brevity.
    return title.split(". ", 1)[-1]


def build_site(root: Path = PROJECT_ROOT) -> list[Path]:
    """Build site/ from docs/ + README.md. Returns list of written files."""
    docs_dir = root / "docs"
    site_dir = root / "site"
    readme = root / "README.md"

    if not docs_dir.is_dir():
        raise SystemExit(f"docs/ not found in {root}; nothing to build")
    if not readme.is_file():
        raise SystemExit(f"README.md not found in {root}")

    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)

    sources = [(readme, "index.html")]
    sources.extend((doc, doc.stem + ".html") for doc in sorted(docs_dir.glob("*.md")))

    # Render every source once.
    rendered: dict[str, tuple[str, str, str | None]] = {}
    for src, dest_name in sources:
        text = src.read_text(encoding="utf-8")
        title = _first_heading(text)
        body = render_markdown(text)
        verify = render_verify_banner(text)
        rendered[dest_name] = (title, body, verify)

    nav_parts = [
        f'<a href="{dest}">{html.escape(_nav_label(title, Path(dest)))}</a>'
        for dest, (title, _body, _verify) in rendered.items()
    ]
    nav = "<br>".join(nav_parts)

    written: list[Path] = []
    for dest_name, (title, body, verify) in rendered.items():
        dest = site_dir / dest_name
        dest.write_text(_page_html(title, body, verify, nav), encoding="utf-8")
        written.append(dest)

    css_src = root / "static" / "style.css"
    css_dest = site_dir / "style.css"
    if css_src.is_file():
        css_dest.write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(css_dest)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the static guide site.")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args(argv)

    if args.dry_run:
        files = sorted(p.name for p in DOCS_DIR.glob("*.md"))
        print(f"Would build {len(files) + 1} pages from: {', '.join(files)} + README.md")
        return 0

    written = build_site()
    print(f"Built {len(written)} files in site/:")
    for path in written:
        print(f"  {path.name}")

    doc_files = sorted(DOCS_DIR.glob("*.md"))
    stamped = [f for f in doc_files if render_verify_banner(f.read_text(encoding="utf-8"))]
    print(f"Hand-maintained docs with verify dates: {len(stamped)}/{len(doc_files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
