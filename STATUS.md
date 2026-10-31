# STATUS

Project: **FFXIV Ocean Fishing Guide** — fan-made manual, hand-maintained, warm-toned.
Owner: Asdale Dynamics, LLC. Last updated: **2026-10-31**

## What was built

- **Manual, 8 hand-maintained Markdown documents** in `docs/`, all with warm tone and stamped
  with a hand-check (**verify date**) stamp of `2026-10-31`:
  1. `01-voyage-windows.md` — booking the voyage, plain departure-window table, what a trip feels like
  2. `02-hourly-boils.md` — boils explained plainly, splash-reading cheatsheet, personal boil log
  3. `03-weather-and-expectations.md` — skies in plain words, kindly expectation-setting
  4. `04-bait-rotation-cards.md` — four cheat cards: default rotation, bait-vs-bite, actions, first-voyage script
  5. `05-achievement-hunts.md` — relaxed-collector hunt order and gentle pacing
  6. `06-patience-tips.md` — slow seas staying fun, in game and in general
  7. `voyage-checklist.md` — before/during/after one-page card with checkboxes
  8. `glossary.md` — plain-words hobby dictionary
- **Static site generator** (`build.py`, Python 3.8+, standard library only): converts
  `README.md` (homepage) + `docs/*.md` into `site/*.html` with a shared stylesheet
  (`static/style.css`), site navigation, and per-page verify-date badges.
  Constraint honored by design: **no network calls, no scraping, no sniffing, no account data.**
- **Test suite** (`tests/test_build.py`, 31 tests, `unittest`): inline/bold/italic/code/link
  rendering, escaping, HTML injection safety, tables/lists/checklists/blockquotes/rules,
  verify-date detection, page templating, site build from a fixture, and repository smoke tests
  (every doc stamped with a `YYYY-MM-DD` verify date, docs cross-linked, no automation flags).
- **README.md** — full project intro, table contents, build/test/maintenance instructions,
  privacy posture, contributing rules, license + LLC credit, trademark disclaimer.
- **LICENSE** — MIT with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
- **`.gitignore`** — ignores regenerated `site/`, caches, editor litter.

## How to run it

```sh
python3 build.py                      # build the site into site/
python3 -m unittest discover tests -v # run the test suite
```

Open `site/index.html` in a browser to read the site. Nothing needs a server; pages are plain
file URLs. `python3 build.py --dry-run` lists what *would* be built without writing.

## Verification results (2026-10-31)

- `python3 -m unittest discover tests`: **31 tests, all OK** (0 failures).
- `python3 build.py`: **built 10 files** (9 HTML pages + stylesheet) and reported
  **8/8 hand-maintained docs carry verify dates**.
- Spot-checked generated HTML: valid tags, table + verify badge present, LLC footer on every page.
- Confirmations against the project brief:
  - voyage windows & hourly boil signs: plain tables present (verified stamps in docs 01, 02)
  - weather kindly explained, expectations set: doc 03
  - bait-rotation cheat cards: doc 04 (four cards)
  - achievement hunts for relaxed collectors: doc 05
  - patience tips: doc 06
  - voyage checklist: `voyage-checklist.md` (checkboxes render in HTML)
  - glossary: `glossary.md`
  - warm tone, tested build, no scraping: throughout + enforced by tests
  - LICENSE exact string and README LLC credit: verified by `test_license_copyright_line_exact`
    and `test_readme_credits_llc`
- Git initialized in this folder with a single plain commit (no Co-authored-by trailers, no push,
  no remote, no publishing).

## Known gaps (honest list)

- **Table values are intentionally general.** The departure-window table has fill-in rows and
  the boil table is a watch-pattern of shapes, not exact in-game strings. This is by design —
  the brief demands hand-maintained, verify-dated tables; exact numbers across 8 documents were
  not verified against a live game in this session. The **verify date is the contract**:
  anyone (including future us) who plays a voyage updates their table, moves the stamp, commits.
- **Exact bait names, achievement names, quest names, departure interval** are described
  functionally (e.g., "the heavy bait") rather than hard-coded, to avoid drifting after patches
  and localizations. The docs say so on the page.
- The maintenance loop is a human loop: if sorted-by-date tracking of many editors is ever
  needed, a small `docs/METADATA.md` index could be added next to the tables. Not built yet.
- The site is plain HTML with no search or dark mode; navigation is a simple list, by design.
- No CI. Tests are one command; a future workflow could run them on push — but this project
  stays local-first, so it was deliberately not wired up.
