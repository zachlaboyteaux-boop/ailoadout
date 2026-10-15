#!/usr/bin/env python3
"""Generate SEO pages, sitemap, robots, llms.txt from tools.json. Run from repo root: python3 scripts/build.py"""
import json, os, html
BASE = "https://zachlaboyteaux-boop.github.io/ailoadout"
SLUG = {"Coding / Vibe Coding":"coding","AI Agents":"agents","Chat / Assistants":"chat","Image":"image","Video":"video",
        "Voice / Audio":"voice","Writing":"writing","Research / Search":"research","Game Dev":"game-dev","Productivity":"productivity",
        "Crypto / Finance AI":"crypto-finance","3D":"3d","Music":"music","Education":"education","Streamers / Creators":"creators",
        "Open-Source & Local Models":"local-models","AI in Games":"ai-in-games"}
D = json.load(open("tools.json")); UP = D["updated"]; YEAR = UP[:4]
e = html.escape
cats = {}
for t in D["tools"]: cats.setdefault(t["category"], []).append(t)
for c in cats: cats[c].sort(key=lambda t: (not t.get("featured", False), t["rank"]))
import re
def slugify(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
slugs = {}
for t in D["tools"]:
    s = slugify(t["name"])
    if s in slugs.values(): s = s + "-" + SLUG[t["category"]]
    slugs[id(t)] = s
def tslug(t): return slugs[id(t)]
for t in D["tools"]: t["slug"] = tslug(t)
json.dump(D, open("tools.json","w"), indent=1)  # write slugs back so the homepage can link to /tools/<slug>/
TIER_COL = {"S":"#ff5c5c","A":"#ffb347","B":"#7cff6b","C":"#5ac8ff"}
def feat(t): return ' <span style="display:inline-block;border-radius:6px;padding:0 6px;background:#ffd700;color:#000;font-weight:800;font-size:12px">★ Featured</span>' if t.get("featured") else ""
def badge(t): return f'<span style="display:inline-block;min-width:22px;text-align:center;font-weight:800;border-radius:6px;padding:0 6px;color:#000;background:{TIER_COL.get(t.get("tier","C"))}">{t.get("tier","")}</span>'
CSS = "body{margin:0;font:16px/1.6 system-ui,sans-serif;background:#0b0d12;color:#e7eaf2}a{color:#5ac8ff}.w{max-width:860px;margin:auto;padding:20px}h1{letter-spacing:-.5px}h1 span,h2{color:#7cff6b}ol li{margin:10px 0}.m{color:#8b93a7}nav a{margin-right:10px;font-size:14px}"
def ld(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>'
ORG = {"@context":"https://schema.org","@type":"Organization","name":"The AI Loadout","url":BASE+"/","logo":BASE+"/favicon.svg"}
KIT_FORM_ID = 10047964  # Kit form "Newsletter site"
GOATCOUNTER = '<script data-goatcounter="https://ailoadout.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'  # free analytics; site code from Zach's ailoadout.goatcounter.com
SIGNUP = f'<form action="https://app.kit.com/forms/{KIT_FORM_ID}/subscriptions" method="post" target="_blank" style="margin:30px 0;padding:18px;border:1px dashed #232a3a;border-radius:12px;text-align:center"><b>Get The AI Loadout Weekly</b><br><span class="m">The AI launches that matter + what to equip now. Free, weekly.</span><br><input type="email" name="email_address" required placeholder="you@example.com" aria-label="Email address" style="padding:12px;border-radius:10px;border:1px solid #232a3a;background:#141823;color:#e7eaf2;font-size:16px;max-width:300px;width:100%"> <button type="submit" style="padding:12px 16px;border-radius:10px;border:0;background:#7cff6b;color:#000;font-weight:700;margin-top:8px">Subscribe</button></form>'
def page(path, title, desc, body, extra=""):
    url = f"{BASE}/{path}"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<meta property="article:modified_time" content="{UP}">{ld(ORG)}{extra}<style>{CSS}</style></head><body><div class="w">
<nav><a href="{BASE}/">← The AI Loadout</a>{"".join(f'<a href="{BASE}/{s}/">{e(c)}</a>' for c,s in SLUG.items() if c in cats)}</nav>
{body}{SIGNUP}<p class="m"><a href="{BASE}/submit/">Submit a tool</a> · <a href="{BASE}/sponsor/">Sponsor / advertise</a></p><p class="m">Last updated {UP}. Rankings are editorial; pricing changes often, check each tool's site.</p></div>{GOATCOUNTER}</body></html>'''
urls = [BASE+"/"]
for c, ts in cats.items():
    s = SLUG.get(c, c.lower().replace(" ", "-").replace("/", ""))
    short = c.split(" /")[0]
    top = ts[0]
    faq = [(f"What is the best AI tool for {short.lower()} in {YEAR}?", f"The top-ranked pick is {top['name']}: {top['verdict'].lower()}. Runners-up: " + ", ".join(t['name'] for t in ts[1:3]) + "."),
           (f"Are there free AI tools for {short.lower()}?", "Free tiers or free options: " + (", ".join(t['name'] for t in ts if "free" in t['pricing'].lower() or "open source" in t['pricing'].lower()) or "none in this list") + "."),
           ("How is this list ranked?", f"Editorially by The AI Loadout, based on capability, ease of use and value, and updated as new tools ship. Last updated {UP}.")]
    lis = "".join(f'<li>{badge(t)} <b><a href="{BASE}/tools/{tslug(t)}/">{e(t["name"])}</a></b>{feat(t)} — {e(t["verdict"])}. <span class="m">{e(t["pricing"])} · <a href="{e(t["url"])}" rel="noopener">official site ↗</a></span></li>' for t in ts)
    body = f'<h1>Best AI tools for <span>{e(short)}</span> in {YEAR}</h1><p>The {e(c)} loadout: {len(ts)} AI tools ranked for this job, with a one-line verdict on what each is best for. Tiers: S = must-equip, A = strong pick, B = great for specific needs, C = situational. Top pick right now: <b>{e(top["name"])}</b> ({top.get("tier","")}-tier).</p><ol>{lis}</ol><h2>FAQ</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in faq)
    il = {"@context":"https://schema.org","@type":"ItemList","name":f"Best AI tools for {short} in {YEAR}","dateModified":UP,
          "itemListElement":[{"@type":"ListItem","position":t["rank"],"name":t["name"],"url":t["url"],"description":t["verdict"]} for t in ts]}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    os.makedirs(s, exist_ok=True)
    open(f"{s}/index.html","w").write(page(f"{s}/", f"Best AI tools for {short} in {YEAR} – The AI Loadout", f"The {len(ts)} best AI tools for {short.lower()} in {YEAR}, ranked. #1: {top['name']}.", body, ld(il)+ld(fq)))
    urls.append(f"{BASE}/{s}/")

# ---- per-tool pages ----
FULL_TOOLS = []
for t in D["tools"]:
    s = tslug(t); c = t["category"]; short = c.split(" /")[0]; peers = [x for x in cats[c] if x is not t]
    faq = [(f"What is {t['name']} best for?", f"{t['verdict']}. It ranks #{t['rank']} of {len(cats[c])} in our {c} loadout."),
           (f"Is {t['name']} free?", f"Pricing: {t['pricing']}. Pricing changes often; check {t['url']}."),
           (f"What are the best alternatives to {t['name']}?", "In the same loadout: " + "; ".join(f"{p['name']} (#{p['rank']}, {p['verdict'].lower()})" for p in peers[:4]) + ".")]
    alts = "".join(f'<li><a href="{BASE}/tools/{tslug(p)}/">{e(p["name"])}</a> (#{p["rank"]}) — {e(p["verdict"])}</li>' for p in peers)
    body = (f'<h1>{e(t["name"])} review: what it\'s best for ({YEAR})</h1>'
            f'<p><b>Verdict:</b> {e(t["verdict"])}.</p><p>{feat(t)}<b>Tier:</b> {badge(t)} &nbsp; <b>Rank:</b> #{t["rank"]} of {len(cats[c])} in the <a href="{BASE}/{SLUG[c]}/">{e(c)} loadout</a>.</p>'
            f'<p><b>Pricing:</b> {e(t["pricing"])}</p><p><a href="{e(t["url"])}" rel="noopener">Visit {e(t["name"])} →</a></p>'
            f'<h2>Alternatives in the {e(short)} loadout</h2><ul>{alts}</ul><h2>FAQ</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in faq))
    sa = {"@context":"https://schema.org","@type":"SoftwareApplication","name":t["name"],"url":t["url"],"applicationCategory":c,"operatingSystem":"Web",
          "description":t["verdict"],"dateModified":UP,"review":{"@type":"Review","author":{"@type":"Organization","name":"The AI Loadout"},"reviewBody":t["verdict"]}}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    os.makedirs(f"tools/{s}", exist_ok=True)
    open(f"tools/{s}/index.html","w").write(page(f"tools/{s}/", f"{t['name']} review: what it's best for ({YEAR}) – The AI Loadout", f"{t['name']}: {t['verdict']}. Ranked #{t['rank']} for {short.lower()}. Pricing, alternatives and FAQ.", body, ld(sa)+ld(fq)))
    urls.append(f"{BASE}/tools/{s}/")
    FULL_TOOLS.append(f"- {t['name']}: {BASE}/tools/{s}/\n")
# ---- comparison pages ----
def find_tool(spec):
    """spec is a name str, or (name, category) to pick a specific loadout entry."""
    if isinstance(spec, (list, tuple)) and len(spec) == 2:
        name, cat = spec
        m = [t for t in D["tools"] if t["name"] == name and t["category"] == cat]
        if m: return m[0]
        m = [t for t in D["tools"] if t["name"] == name]
        return m[0] if m else None
    m = [t for t in D["tools"] if t["name"] == spec]
    return m[0] if m else None
COMPARE = [("cursor-vs-claude-code",["Cursor","Claude Code"]),
           ("chatgpt-vs-claude-vs-gemini",["ChatGPT","Claude","Gemini"]),
           ("grok-vs-chatgpt-vs-claude",["Grok","ChatGPT","Claude"]),
           ("midjourney-vs-ideogram-vs-leonardo",["Midjourney","Ideogram","Leonardo.Ai"]),
           ("runway-vs-sora-vs-veo",["Runway","Sora","Veo (Google Flow)"]),
           ("lovable-vs-bolt-vs-v0",["Lovable","Bolt.new","v0"]),
           ("perplexity-vs-chatgpt-deep-research-vs-notebooklm",["Perplexity","ChatGPT Deep Research","NotebookLM"]),
           ("ollama-vs-lm-studio",[("Ollama","Open-Source & Local Models"),("LM Studio","Open-Source & Local Models")]),
           ("suno-vs-udio",[("Suno","Music"),("Udio","Music")]),
           ("opusclip-vs-eklipse",["OpusClip","Eklipse"]),
           ("meshy-vs-tripo-vs-rodin",[("Meshy","3D"),("Tripo","3D"),("Rodin (Hyper3D)","3D")])]
FULL_CMP = []
for s, names in COMPARE:
    ts = []
    for n in names:
        t = find_tool(n)
        if t: ts.append(t)
    if len(ts) < 2: continue
    title = " vs ".join(t["name"] for t in ts)
    same = len({t["category"] for t in ts}) == 1
    rows = "".join(f'<tr><td><a href="{BASE}/tools/{tslug(t)}/">{e(t["name"])}</a></td><td>{e(t["category"])}</td><td>#{t["rank"]}</td><td>{e(t["verdict"])}</td><td>{e(t["pricing"])}</td></tr>' for t in ts)
    picks = "".join(f'<li>Pick <b>{e(t["name"])}</b> if you want: {e(t["verdict"][0].lower()+t["verdict"][1:])}.</li>' for t in ts)
    top = min(ts, key=lambda t: t["rank"]) if same else None
    short_ans = (f"In our {ts[0]['category']} loadout, {top['name']} ranks highest (#{top['rank']}), but each wins at something different." if top else "They lead different loadouts, so the right pick depends on the job.")
    faq = [(f"Which is better: {title}?", short_ans + " " + " ".join(f"{t['name']}: {t['verdict'].lower()}." for t in ts)),
           ("Which one is free?", " ".join(f"{t['name']}: {t['pricing']}." for t in ts))]
    body = (f'<h1>{e(title)} ({YEAR})</h1><p><b>Short answer:</b> {e(short_ans)}</p>'
            f'<table style="width:100%;border-collapse:collapse" border="1" cellpadding="8"><tr><th>Tool</th><th>Loadout</th><th>Rank</th><th>Best for</th><th>Pricing</th></tr>{rows}</table>'
            f'<h2>Which should you pick?</h2><ul>{picks}</ul><h2>FAQ</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in faq) +
            '<p class="m">Comparison is based on The AI Loadout\'s own rankings and verdicts in tools.json.</p>')
    il = {"@context":"https://schema.org","@type":"ItemList","name":title,"dateModified":UP,"itemListElement":[{"@type":"ListItem","position":i+1,"name":t["name"],"url":t["url"]} for i,t in enumerate(ts)]}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    os.makedirs(f"compare/{s}", exist_ok=True)
    open(f"compare/{s}/index.html","w").write(page(f"compare/{s}/", f"{title} ({YEAR}): which AI tool should you use? – The AI Loadout", f"{title} compared: best-for verdicts, rankings and pricing. {short_ans}", body, ld(il)+ld(fq)))
    urls.append(f"{BASE}/compare/{s}/"); FULL_CMP.append(f"- {title}: {BASE}/compare/{s}/\n")

# ---- best-of SEO pages (curated from tools.json only; no invented claims) ----
def tools_by_specs(specs):
    out = []
    for spec in specs:
        t = find_tool(spec)
        if t: out.append(t)
    return out

BEST = [
  {
    "slug": "best-free-ai-coding-tools",
    "title": f"Best free AI coding tools in {YEAR}",
    "desc": f"The best free-tier AI coding tools in {YEAR}, ranked from our Coding loadout.",
    "intro": "These coding tools have a free tier or free plan in our data. Paid upgrades exist on most; check each site for current limits. Rankings stay editorial.",
    "specs": [("Cursor","Coding / Vibe Coding"),("GitHub Copilot","Coding / Vibe Coding"),("Lovable","Coding / Vibe Coding"),("Bolt.new","Coding / Vibe Coding"),("v0","Coding / Vibe Coding"),("Replit","Coding / Vibe Coding")],
    "faqs": [
      (f"What is the best free AI coding tool in {YEAR}?", "Among free-tier options in our Coding loadout, Cursor ranks #1 overall and has a free tier."),
      ("Do free tiers stay free forever?", "Pricing changes often. We list what tools.json says today; always confirm on the official site."),
    ],
  },
  {
    "slug": "best-ai-for-unity-devs",
    "title": f"Best AI for Unity developers in {YEAR}",
    "desc": f"AI tools Unity and game developers use for assets, NPCs, and prototyping in {YEAR}.",
    "intro": "We do not claim official Unity plugins. This page ranks tools from our Game Dev and 3D loadouts that game developers use for AI assets, NPCs, and prompt-to-playable prototypes.",
    "specs": [("Rosebud AI","Game Dev"),("Scenario","Game Dev"),("Meshy","Game Dev"),("Inworld AI","Game Dev"),("Tripo","Game Dev"),("Rodin (Hyper3D)","3D")],
    "faqs": [
      ("What AI should Unity developers start with?", "For prompt-to-playable browser games, Rosebud AI ranks #1 in our Game Dev loadout. For on-style assets, Scenario; for 3D meshes, Meshy."),
      ("Is this Unity-only?", "No. These tools are useful across game engines; we group them for developers shipping games, including Unity workflows."),
    ],
  },
  {
    "slug": "best-local-llm-tools",
    "title": f"Best local LLM tools in {YEAR}",
    "desc": f"Best tools to run open-source LLMs on your own machine in {YEAR}: Ollama, LM Studio, and more.",
    "intro": "Run models on your own hardware. We rank runners and UIs from our Open-Source & Local Models loadout. We do not invent VRAM requirements — check each project’s docs for your GPU or CPU.",
    "specs": [("Ollama","Open-Source & Local Models"),("LM Studio","Open-Source & Local Models"),("Hugging Face","Open-Source & Local Models"),("Open WebUI","Open-Source & Local Models"),("llama.cpp","Open-Source & Local Models"),("Jan","Open-Source & Local Models")],
    "faqs": [
      ("What is the best way to run a local LLM?", "Ollama ranks #1 in our local-models loadout for one-command local models. LM Studio is the top GUI desktop app."),
      ("Will this run on 8GB or 16GB VRAM?", "It depends on the model and quant. Our rankings do not claim specific VRAM sizes — use each tool’s model browser and docs."),
    ],
  },
  {
    "slug": "best-ai-for-twitch-streamers",
    "title": f"Best AI for Twitch streamers in {YEAR}",
    "desc": f"Best AI tools for Twitch streamers and creators in {YEAR}: clipping, captions, and edits.",
    "intro": "From our Streamers / Creators loadout: AI for highlights, vertical clips, captions, and edits. Built for people who ship content from long streams.",
    "specs": [("OpusClip","Streamers / Creators"),("Eklipse","Streamers / Creators"),("StreamLadder","Streamers / Creators"),("Captions","Streamers / Creators"),("Descript","Streamers / Creators"),("CapCut","Streamers / Creators")],
    "faqs": [
      ("What is the best AI clipper for Twitch?", "OpusClip ranks #1 for turning long videos into shorts. Eklipse ranks #2 and is tuned for Twitch gaming highlights."),
      ("Is CapCut good enough for free?", "CapCut is C-tier in this loadout as a free all-in-one social editor; stronger clippers sit above it for highlight workflows."),
    ],
  },
  {
    "slug": "best-ai-for-students",
    "title": f"Best AI for students in {YEAR}",
    "desc": f"Best AI study tools for students in {YEAR}, ranked from our Education loadout.",
    "intro": "Study gear from our Education loadout. Use AI to learn faster — not to skip learning. School policies differ; follow yours.",
    "specs": [("NotebookLM","Education"),("Khanmigo","Education"),("ChatGPT","Education"),("Duolingo","Education"),("Quizlet","Education")],
    "faqs": [
      ("What is the best AI for studying?", "NotebookLM ranks #1 for studying your own notes and sources. Khanmigo ranks #2 as a tutor that guides instead of dumping answers."),
      ("Is ChatGPT allowed for homework?", "Depends on your school. We rank it as an all-purpose explainer; always follow your academic integrity rules."),
    ],
  },
  {
    "slug": "best-ai-for-crypto-research",
    "title": f"Best AI for crypto research in {YEAR}",
    "desc": f"Best AI tools for crypto and market research in {YEAR}, from our Crypto / Finance loadout.",
    "intro": "Research and analytics gear from our Crypto / Finance AI loadout. Not financial advice — rankings are editorial opinions for finding information faster.",
    "specs": [("Perplexity Finance","Crypto / Finance AI"),("Grok","Crypto / Finance AI"),("Nansen","Crypto / Finance AI"),("Arkham Intelligence","Crypto / Finance AI"),("Kaito","Crypto / Finance AI"),("Messari","Crypto / Finance AI")],
    "faqs": [
      ("What is the best AI for crypto research?", "Perplexity Finance ranks #1 for quick, sourced answers on markets. Nansen leads on-chain wallet analytics; Messari for research reports."),
      ("Is this financial advice?", "No. The AI Loadout ranks tools for research workflows. Do your own diligence."),
    ],
  },
  {
    "slug": "best-ai-music-for-youtube",
    "title": f"Best AI music for YouTube in {YEAR}",
    "desc": f"Best AI music tools for YouTube creators in {YEAR}. Licensing still varies — check each tool.",
    "intro": "Music generators from our Music loadout. Licensing and copyright rules change and differ by plan. In our data, ElevenLabs Music is ranked for commercially cleared AI music; always confirm license terms before you monetize.",
    "specs": [("ElevenLabs Music","Music"),("Suno","Music"),("Udio","Music"),("Stable Audio","Music"),("Mubert","Music"),("AIVA","Music")],
    "faqs": [
      ("Can I use AI music on YouTube without a copyright claim?", "It depends on the tool and your plan. Our Music loadout ranks ElevenLabs Music for commercially cleared AI music; Mubert for royalty-free background music for streams. Verify current terms on each site before uploading."),
      ("Suno or Udio for YouTube?", "Suno ranks #1 for full songs with vocals; Udio #2 for finer control. Commercial rights depend on their plans — check both."),
    ],
  },
]
FULL_BEST = []
for b in BEST:
    ts = tools_by_specs(b["specs"])
    # de-dupe by name+category while preserving order
    seen=set(); uniq=[]
    for t in ts:
        k=(t["name"],t["category"])
        if k in seen: continue
        seen.add(k); uniq.append(t)
    ts = uniq
    if len(ts) < 2: continue
    lis = "".join(
        f'<li>{badge(t)} <b><a href="{BASE}/tools/{tslug(t)}/">{e(t["name"])}</a></b>{feat(t)} — {e(t["verdict"])}. '
        f'<span class="m">{e(t["pricing"])} · <a href="{BASE}/{SLUG.get(t["category"],"")}/">{e(t["category"])}</a> · '
        f'<a href="{e(t["url"])}" rel="noopener">official site ↗</a></span></li>'
        for t in ts
    )
    faq = b["faqs"]
    body = (f'<h1>{e(b["title"])}</h1><p>{e(b["intro"])}</p><ol>{lis}</ol><h2>FAQ</h2>'
            + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in faq)
            + f'<p class="m">Pulled from <a href="{BASE}/tools.json">tools.json</a> rankings. Related: <a href="{BASE}/">all loadouts</a>.</p>')
    il = {"@context":"https://schema.org","@type":"ItemList","name":b["title"],"dateModified":UP,
          "itemListElement":[{"@type":"ListItem","position":i+1,"name":t["name"],"url":f"{BASE}/tools/{tslug(t)}/","description":t["verdict"]} for i,t in enumerate(ts)]}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    os.makedirs(f"best/{b['slug']}", exist_ok=True)
    open(f"best/{b['slug']}/index.html","w").write(page(f"best/{b['slug']}/", f"{b['title']} – The AI Loadout", b["desc"], body, ld(il)+ld(fq)))
    urls.append(f"{BASE}/best/{b['slug']}/")
    FULL_BEST.append(f"- {b['title']}: {BASE}/best/{b['slug']}/\n")

# ---- submit page ----
PAY_LINK = "https://buy.stripe.com/aFa8wQ0wa5wL6Cy7bPgEg02"  # Stripe Payment Link: Featured Listing $49/mo
ISSUE = "https://github.com/zachlaboyteaux-boop/ailoadout/issues/new?title=Tool+submission%3A+&body=Tool+name%3A%0ATool+URL%3A%0ALoadout+%28category%29%3A%0AOne-line+pitch%3A%0A"
body = (f'<h1>Submit your AI tool</h1><p>Built an AI tool? Get it in front of people choosing their loadout. Two ways in:</p>'
  '<div id="thanks" style="display:none;padding:14px;border:1px solid #7cff6b;border-radius:12px;margin:12px 0"><b>Payment received — thank you!</b> Your Featured listing is being set up and usually goes live within 2 business days. We will reach you at your checkout email if we need anything.</div>'
  f'<h2>Free listing</h2><ul><li>Open a <a href="{ISSUE}" rel="noopener">submission on GitHub</a> with your tool name, URL, loadout and a one-line pitch.</li>'
  '<li>We review every submission. If it makes the cut, it gets ranked into a tier (S/A/B/C) on merit.</li><li>No guarantee of inclusion or placement; rankings stay editorial.</li></ul>'
  f'<h2>★ Featured listing — $49/month</h2><ul><li>Pinned at the top of your tool\'s loadout with a <b>★ Featured</b> badge.</li>'
  '<li>Included in <b>The AI Loadout Weekly</b> newsletter.</li><li>Your own tool page with FAQ and structured data for search and AI answers.</li>'
  '<li>Cancel anytime. Featured placement is clearly labeled and does not change your tier, which stays editorial.</li></ul>'
  f'<p><a href="{PAY_LINK}" rel="noopener" style="display:inline-block;padding:14px 22px;border-radius:10px;background:#7cff6b;color:#000;font-weight:800;text-decoration:none">Get Featured — $49/mo</a></p>'
  '<p class="m">Checkout is handled securely by Stripe and asks for your tool name and URL.</p>'
  '<script>if(location.search.indexOf("featured=thanks")>-1)document.getElementById("thanks").style.display="block"</script>')
os.makedirs("submit", exist_ok=True)
open("submit/index.html","w").write(page("submit/", "Submit your AI tool – The AI Loadout", "Submit your AI tool to The AI Loadout for free, or get a $49/month Featured listing pinned at the top of its loadout.", body))
urls.append(f"{BASE}/submit/")

# ---- sponsor / media kit page ----
SPONSOR_ISSUE = "https://github.com/zachlaboyteaux-boop/ailoadout/issues/new?title=Sponsor+inquiry&body=Company%3A%0AProduct%2FURL%3A%0APreferred+placement%3A%0ABudget+range+%28optional%29%3A%0AMessage%3A%0A"
sponsor_body = (
  '<h1>Sponsor / advertise</h1>'
  '<p>The AI Loadout ranks AI tools into loadouts with S/A/B/C tiers — coding, agents, image, video, game dev, crypto, local models, and more — plus a weekly newsletter of the launches that matter.</p>'
  '<h2>Who reads this</h2>'
  '<p>Builders, vibe coders, creators, gamers, and AI enthusiasts choosing what to equip next. Qualitative audience only; we do not invent demographics.</p>'
  '<h2>Early partners</h2>'
  '<p>The site is live and growing. The newsletter just launched — early partners get in before the list is crowded. Sponsored placements stay clearly labeled; rankings stay editorial.</p>'
  '<h2>Placements</h2>'
  '<ul>'
  f'<li><b>★ Featured tool listing — $49/mo</b>: pinned at the top of your tool\'s loadout with a Featured badge, included in the weekly newsletter, plus a dedicated tool page. <a href="{BASE}/submit/">Get Featured →</a></li>'
  '<li><b>Newsletter sponsorship slot</b>: a sponsor mention in The AI Loadout Weekly. Price TBD — ask us.</li>'
  '<li><b>Homepage / loadout mention or compare-page partner slot</b>: light gamer-flavored callouts where readers pick gear. Price TBD — ask us.</li>'
  '</ul>'
  '<h2>What we need from you</h2>'
  '<ul><li>Logo (SVG or PNG)</li><li>Product URL</li><li>One-liner (what it\'s best for)</li><li>Preferred loadout / placement</li></ul>'
  '<h2>Contact</h2>'
  f'<p><a href="{SPONSOR_ISSUE}" rel="noopener" style="display:inline-block;padding:14px 22px;border-radius:10px;background:#7cff6b;color:#000;font-weight:800;text-decoration:none">Open a sponsor inquiry</a></p>'
  '<p class="m">Opens a GitHub issue with a short form. No invented traffic stats — we will share real numbers once analytics is live.</p>'
)
os.makedirs("sponsor", exist_ok=True)
open("sponsor/index.html","w").write(page("sponsor/", "Sponsor / advertise – The AI Loadout", "Sponsor The AI Loadout: Featured listings, newsletter slots, and partner mentions for AI tools. Early partners welcome.", sponsor_body))
urls.append(f"{BASE}/sponsor/")
# home page JSON-LD + analytics + footer guide links
idx = open("index.html").read()
mark = "<!--LD-->"
block = mark + ld({"@context":"https://schema.org","@type":"WebSite","name":"The AI Loadout","url":BASE+"/","dateModified":UP}) + ld(ORG) +     ld({"@context":"https://schema.org","@type":"ItemList","name":"AI tool loadouts","itemListElement":[{"@type":"ListItem","position":i+1,"name":c,"url":f"{BASE}/{SLUG[c]}/"} for i,c in enumerate(cats)]}) + mark
if mark in idx: idx = idx.split(mark)[0] + block + idx.split(mark)[2]
else: idx = idx.replace("<style>", block + "<style>", 1)
if "ailoadout.goatcounter.com/count" not in idx:
    idx = idx.replace("</body>", GOATCOUNTER + "</body>", 1)
# Keep homepage footer compare + best links in sync with generated pages
cmp_links = " · ".join(f'<a href="compare/{s}/">{e(names[0] if isinstance(names[0], str) else names[0][0])}…</a>' for s, names in COMPARE)
# clearer static footer block
best_links = " · ".join(f'<a href="best/{b["slug"]}/">{e(b["title"].replace(f" in {YEAR}",""))}</a>' for b in BEST)
footer_guides = f'Compare: {cmp_links}<br>Best guides: {best_links}<br>'
import re as _re
idx2 = _re.sub(r"Compare:.*?<br>", footer_guides, idx, count=1, flags=_re.S)
if idx2 != idx: idx = idx2
elif "Best guides:" not in idx:
    idx = idx.replace("Compare:", footer_guides + "Compare:", 1)
open("index.html","w").write(idx)
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{u}</loc><lastmod>{UP}</lastmod><changefreq>daily</changefreq></url>\n" for u in urls+[BASE+"/llms.txt"]) + "</urlset>\n")
bots = ["Googlebot","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-User","Claude-SearchBot","PerplexityBot","Perplexity-User","Google-Extended"]
open("robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + "User-agent: *\nAllow: /\nDisallow: /dashboard/\n\n" + f"Sitemap: {BASE}/sitemap.xml\n")
L = [f"# The AI Loadout\n\n> A free directory of AI tools ranked by use case (\"loadouts\"), plus a feed of new AI releases. Last updated {UP}.\n\n## Loadouts\n"]
L += [f"- [Best AI tools for {c.split(' /')[0]}]({BASE}/{SLUG[c]}/): #1 {ts[0]['name']} — {ts[0]['verdict']}\n" for c,ts in cats.items()]
L += [f"\n## Data\n- [tools.json]({BASE}/tools.json): machine-readable list of all tools and releases\n- [llms-full.txt]({BASE}/llms-full.txt): full directory as text\n"]
open("llms.txt","w").write("".join(L))
F = [f"# The AI Loadout — full directory\n\nLast updated {UP}. Source: {BASE}/\n"]
for c, ts in cats.items():
    F.append(f"\n## {c} ({BASE}/{SLUG[c]}/)\n" + "".join(f"{t['rank']}. {t['name']} ({t['url']}) — {t['verdict']}. Pricing: {t['pricing']}\n" for t in ts))
F.append("\n## Tool pages\n" + "".join(FULL_TOOLS)); F.append("\n## Comparisons\n" + "".join(FULL_CMP)); F.append("\n## Best-of guides\n" + "".join(FULL_BEST))
F.append("\n## New releases\n" + "".join(f"- {r['date']}: {r['name']} — {r['what']} (source: {r['url']})\n" for r in D["releases"]))
open("llms-full.txt","w").write("".join(F))
print(f"built {len(cats)} loadout pages, {len(FULL_TOOLS)} tool pages, {len(FULL_CMP)} comparisons, {len(FULL_BEST)} best-of pages, {len(urls)} sitemap URLs")
