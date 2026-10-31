# FFXIV Ocean Fishing Guide — A Fan-Made Manual Without the Spreadsheets

*A gentle, hand-maintained manual for enjoying Final Fantasy XIV's Ocean Fishing: voyage windows
and hourly boil signs in plain tables, weather explained kindly, simple bait-rotation cheat
cards, achievement hunts for relaxed collectors, and patience tips so slow seas stay fun.*

Built and maintained by **Asdale Dynamics, LLC** as part of a growing set of warm, tested,
beginner-friendly guides. Find more plain-English manuals at
[dylanasdale.github.io](https://dylanasdale.github.io).

---

## Why this exists

Ocean fishing has wonderful community spreadsheets — and spreadsheet dread for the rest of us.
This project is the counter-proposal:

- **Plain tables, no math.** Departure windows, boil signs, weather, and bait choices explained
  the way a friend would explain them.
- **Kind expectations.** A bronze voyage is a finished voyage. Nothing here will make you feel
  late, behind, or inefficient.
- **Hand-maintained only.** Every table carries a **verify date** — the last day a human checked
  it against the live game. If a patch changes the sea, we update the table and move the stamp,
  by hand.
- **Nothing automated. No sniffing. No scraping. No account data.** The build script is a small,
  local, offline program. It reads our own Markdown, writes HTML, and never touches the network,
  your game files, or your account.

## What's inside

| File | What it covers |
| --- | --- |
| [`docs/01-voyage-windows.md`](docs/01-voyage-windows.md) | When The Endeavor sails; booking via Duty Finder; what a voyage feels like |
| [`docs/02-hourly-boils.md`](docs/02-hourly-boils.md) | What boils are, a splash-reading cheatsheet, and a personal boil log to maintain |
| [`docs/03-weather-and-expectations.md`](docs/03-weather-and-expectations.md) | Skies explained kindly; expectation-setting so slow voyages stay pleasant |
| [`docs/04-bait-rotation-cards.md`](docs/04-bait-rotation-cards.md) | Four cheat cards: default rotation, bait-vs-bite, actions, and a first-voyage script |
| [`docs/05-achievement-hunts.md`](docs/05-achievement-hunts.md) | Relaxed-collector goals and the gentle order to chase them in |
| [`docs/06-patience-tips.md`](docs/06-patience-tips.md) | Keeping slow seas fun — in game and in general |
| [`docs/voyage-checklist.md`](docs/voyage-checklist.md) | One-page before/during/after trip card |
| [`docs/glossary.md`](docs/glossary.md) | The hobby's secret language, translated warmly |

Docs are Markdown; a build script (`build.py`) turns them into a reviewable HTML site in `site/`
with a shared template and stylesheet — no frameworks, no dependencies, no network calls.

### Repository layout

```
README.md            you are here; becomes the site homepage
docs/                the manual (Markdown, hand-maintained, verify-dated)
static/style.css     one small stylesheet, no fonts fetched, no CDNs
build.py             offline Python build: docs/ + README.md -> site/
tests/               unit + repo-smoke tests for the build
site/                build output (gitignored; regenerate locally)
STATUS.md            what's built, how verified, known gaps
LICENSE              MIT
```

## Building the site (fully offline)

You need Python 3.8 or newer. From the project folder:

```sh
./build.py            # builds the HTML site into site/ and prints a summary
python3 build.py      # same thing, if your shell lacks executable bits
```

The build is pure standard-library Python: it converts the Markdown in `docs/` (plus the README)
into simple, accessible HTML pages in `site/`, sharing one stylesheet and a small navigation
header. Every page shows each table's **verify date** so readers always know how fresh the
hand-maintained data is.

## Running the tests

```sh
python3 -m unittest discover tests -v
```

The tests cover the Markdown→HTML converter (headings, tables, lists, emphasis, links, escapes)
and a smoke-build of the real docs, including checks that every hand-maintained table carries a
verify-date stamp.

## Maintaining the tables (the project's whole point)

1. Sail a voyage. Notice something true.
2. Open the relevant `docs/*.md` table and update your row — by hand.
3. Move that table's **Last hand-checked** stamp to today's date.
4. Rebuild and re-run tests. Commit with a short message.

Nothing is automated on purpose: the verify dates are only honest if a person is behind them.

## Privacy and safety posture

- No network calls at build time or runtime. No scraping, no sniffing, no crawlers.
- No logins, no account data, no personal data in this repository.
- No Square Enix assets or data redistribution; the manual is original prose and is a fan work.
  Final Fantasy XIV is a trademark of Square Enix (see the disclaimer below).

## Contributing

PRs that update a table's *content* + verify date are welcome. Keep the tone warm, keep tables
plain, and never propose automation of the data collection — that would break the project's
promise. If in doubt, match the voice of the existing docs: kind, unhurried, unhyped.

## License

[MIT](LICENSE) — Copyright (c) 2026 Asdale Dynamics, LLC.

© 2026 Asdale Dynamics, LLC. Fan-made guide; not affiliated with or endorsed by Square Enix.
"Final Fantasy XIV" is a registered trademark of Square Enix Holdings Co., Ltd. All game
references are descriptive only.
