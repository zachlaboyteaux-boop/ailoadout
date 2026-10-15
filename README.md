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
2. Run `python3 scripts/build.py` from the repo root (Python 3 stdlib only).
3. Commit **all** changed files (tools.json, index.html, every `*/index.html`, sitemap.xml, robots.txt, llms*.txt) to `main`. Pages redeploys automatically.
New categories: add a slug to `SLUG` in build.py.
