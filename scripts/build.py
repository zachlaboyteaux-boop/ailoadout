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
SIGNUP = f'<form action="https://app.kit.com/forms/{KIT_FORM_ID}/subscriptions" method="post" target="_blank" style="margin:30px 0;padding:18px;border:1px dashed #232a3a;border-radius:12px;text-align:center"><b>Get The AI Loadout Weekly</b><br><span class="m">The AI launches that matter + what to equip now. Free, weekly.</span><br><input type="email" name="email_address" required placeholder="you@example.com" aria-label="Email address" style="padding:12px;border-radius:10px;border:1px solid #232a3a;background:#141823;color:#e7eaf2;font-size:16px;max-width:300px;width:100%"> <button type="submit" style="padding:12px 16px;border-radius:10px;border:0;background:#7cff6b;color:#000;font-weight:700;margin-top:8px">Subscribe</button></form>'
def page(path, title, desc, body, extra=""):
    url = f"{BASE}/{path}"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/og.png"><meta name="twitter:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<meta property="article:modified_time" content="{UP}">{ld(ORG)}{extra}<style>{CSS}</style></head><body><div class="w">
<nav><a href="{BASE}/">← The AI Loadout</a>{"".join(f'<a href="{BASE}/{s}/">{e(c)}</a>' for c,s in SLUG.items() if c in cats)}</nav>
{body}{SIGNUP}<p class="m"><a href="{BASE}/submit/">Submit a tool</a> · <a href="{BASE}/sponsor/">Sponsor / advertise</a></p><p class="m">Last updated {UP}. Rankings are editorial; pricing changes often, check each tool's site.</p></div></body></html>'''
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
COMPARE = [("cursor-vs-claude-code",["Cursor","Claude Code"]),
           ("chatgpt-vs-claude-vs-gemini",["ChatGPT","Claude","Gemini"]),
           ("midjourney-vs-ideogram-vs-leonardo",["Midjourney","Ideogram","Leonardo.Ai"]),
           ("runway-vs-sora-vs-veo",["Runway","Sora","Veo (Google Flow)"]),
           ("lovable-vs-bolt-vs-v0",["Lovable","Bolt.new","v0"]),
           ("perplexity-vs-chatgpt-deep-research-vs-notebooklm",["Perplexity","ChatGPT Deep Research","NotebookLM"])]
FULL_CMP = []
for s, names in COMPARE:
    ts = []
    for n in names:
        m = [t for t in D["tools"] if t["name"] == n]
        if m: ts.append(m[0])
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
# home page JSON-LD
idx = open("index.html").read()
mark = "<!--LD-->"
block = mark + ld({"@context":"https://schema.org","@type":"WebSite","name":"The AI Loadout","url":BASE+"/","dateModified":UP}) + ld(ORG) + \
    ld({"@context":"https://schema.org","@type":"ItemList","name":"AI tool loadouts","itemListElement":[{"@type":"ListItem","position":i+1,"name":c,"url":f"{BASE}/{SLUG[c]}/"} for i,c in enumerate(cats)]}) + mark
if mark in idx: idx = idx.split(mark)[0] + block + idx.split(mark)[2]
else: idx = idx.replace("<style>", block + "<style>", 1)
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
F.append("\n## Tool pages\n" + "".join(FULL_TOOLS)); F.append("\n## Comparisons\n" + "".join(FULL_CMP))
F.append("\n## New releases\n" + "".join(f"- {r['date']}: {r['name']} — {r['what']} (source: {r['url']})\n" for r in D["releases"]))
open("llms-full.txt","w").write("".join(F))
print(f"built {len(cats)} loadout pages, {len(FULL_TOOLS)} tool pages, {len(FULL_CMP)} comparisons, {len(urls)} sitemap URLs")
