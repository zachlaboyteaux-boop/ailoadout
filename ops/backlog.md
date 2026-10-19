# The AI Loadout — Backlog (prioritized)

Voice: neutral "we rank", light gamer flavor. Budget: $0 unless Zach approves spend.

## P0 — Revenue groundwork (blocked on Zach's OK)
1. ~~Submit-your-tool page + Stripe link~~ DONE 2026-10-14 (live: $49/mo Featured, payment link plink_1UQelYL3anCVpwrE5rEStGg5). Follow-ups: fulfillment checklist (on each new subscription: set `featured: true` in tools.json, add to next newsletter); handle cancellations (remove flag); consider Stripe webhook → GitHub automation; set a public business name/support email in Stripe for this brand.
2. ~~Sponsor / media-kit page~~ DONE 2026-10-15 (`/sponsor/` live): audience (qualitative), placements (Featured $49/mo + newsletter/homepage/compare slots ask-us), GitHub issue contact. No invented traffic/sub numbers. GoatCounter script live; confirm dashboard counts separately.
3. ~~**Analytics**: GoatCounter~~ DONE 2026-10-15 (script on all pages → ailoadout.goatcounter.com). Still need: confirm counts in dashboard; wire `/dashboard/` Visitors panel to real GoatCounter numbers (no invented stats).
4. **Kit**: verify sending address, switch to free plan before Oct 29 trial ends, publish welcome email.

## P1 — SEO / AI-search growth
5. ~~More "best X for Y" pages~~ DONE 2026-10-15 (`/best/`): free coding, Unity/game-dev, local LLMs (no invented VRAM claims), Twitch streamers, students, crypto research, AI music for YouTube (license caveats). Follow-up: more long-tail pages as search demand shows. 2026-10-15 09:00: +5 guides (free chatbots, free image, game assets, NPCs, agent builders) + /best/ hub.
6. ~~More comparisons~~ DONE 2026-10-15 (those five live under `/compare/`). Follow-up: more as new tools land. 2026-10-15 09:00: +5 (n8n/Zapier, Granola/Otter, Nansen/Arkham, Inworld/Convai, Veo/Kling) + /compare/ hub.
7. ~~Homepage cards and loadout pages link to tool pages; breadcrumbs + "updated" stamps~~ DONE 2026-10-15 (build.py: crumbs + stamp + BreadcrumbList on loadout/tool/compare/best pages).
8. Move to custom domain (ailoadout.ai, ~$80/yr) once revenue covers it, so root robots.txt is honored.

## P2 — Marketing drafts (drafts only; nothing posts without Zach's OK)
9. X: daily drop posts + weekly tier-list image (have `marketing/x-launch-posts.md`). Still drafts only.
10. ~~Reddit drafts~~ DONE 2026-10-15 (`marketing/reddit-drafts.md`) — not posted; Zach OK + sub rules required.
11. ~~Hacker News Show HN draft~~ DONE 2026-10-15 (`marketing/hn-show-hn.md`) — not posted.
12. ~~Product Hunt launch kit draft~~ DONE 2026-10-15 (`marketing/product-hunt-kit.md`) — gallery images + Zach OK still needed before launch.
13. ~~TikTok / Shorts scripts~~ DONE 2026-10-15 (`marketing/tiktok-shorts-scripts.md`) — not posted.

## P1b — Next SEO ideas
- ~~Tool pages: "Appears in" links to related compare/best pages~~ DONE 2026-10-15 12:00 ("Compared and ranked in" section on 70+ tool pages).
- Wire `/dashboard/` Visitors panel to GoatCounter (needs API token from Zach, or public counter enabled).
- ~~Stripe fulfillment checklist doc in ops/~~ DONE 2026-10-15 12:00 (`ops/featured-fulfillment.md`).
- More comparisons as tools land (2026-10-15 12:00: +6, 22 total).
- ~~Long-tail best-of ideas from existing data~~ DONE (teachers 2026-10-15; meeting notes, voice generators, open-source, YouTube Shorts, 3D model generators, academic research, music production 2026-10-18). Next long-tail ideas: best AI for architects/archviz, best AI for podcasters, best offline AI apps for iPhone/Mac, best AI for game prototyping.

## P3 — Product
14. User voting / "suggest a tier change" (needs a backend; consider free tier of a form service).
15. Repo-checker idea (saved): paste-your-repo security checker for vibe coders.
16. Founder outreach: ~40 small-team tools, list in ops/outreach-targets.md (46 candidates; pitch = their tier badge from /badge/). Drafts need Zach's approval before sending.
