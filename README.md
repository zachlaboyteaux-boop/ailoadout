# The AI Loadout

AI tools ranked by use case ("loadouts") plus new releases. Static site on GitHub Pages, no build step needed to serve.
Live: https://zachlaboyteaux-boop.github.io/ailoadout/

## Files
- `tools.json` — the single source of truth (tools, releases, `updated` date).
- `index.html` — homepage (reads tools.json in the browser).
- `scripts/build.py` — generates the loadout pages (`/coding/`, `/agents/`, ...), JSON-LD, `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`.
- `dashboard/` — noindex stats page (tool/release counts, commit history; analytics/Kit/Stripe panels not connected yet).
- `newsletter/`, `marketing/` — weekly issue drafts and X post drafts.

## 12-hourly update routine
1. Research new launches/tool changes; edit `tools.json` (add to `releases`, update `tools`, set `updated` to today's date YYYY-MM-DD).
2. Commit `tools.json` to `main`. That's it: the **Build site** GitHub Action (`.github/workflows/decode-binaries.yml`) runs `scripts/build.py`, regenerates every loadout page, `/tools/<slug>/` page, `/compare/<slug>/` page, sitemap, robots and llms files, and commits them. Pages redeploys automatically.
3. Optional local check: `python3 scripts/build.py` (Python 3 stdlib only).

Binary assets: the GitHub connector can only push text, so commit binaries as `<file>.b64`; the Action decodes them (e.g. `og.png.b64` → `og.png`).
New categories: add a slug to `SLUG` in build.py. New comparisons: add to `COMPARE` in build.py.
