#!/usr/bin/env python3
"""Generate SEO pages, sitemap, robots, llms.txt from tools.json. Run from repo root: python3 scripts/build.py"""
import json, os, html
BASE = "https://zachlaboyteaux-boop.github.io/ailoadout"
SLUG = {"Coding / Vibe Coding":"coding","AI Agents":"agents","Chat / Assistants":"chat","Image":"image","Video":"video",
        "Voice / Audio":"voice","Writing":"writing","Research / Search":"research","Game Dev":"game-dev","Productivity":"productivity"}
D = json.load(open("tools.json")); UP = D["updated"]; YEAR = UP[:4]
e = html.escape
cats = {}
for t in D["tools"]: cats.setdefault(t["category"], []).append(t)
for c in cats: cats[c].sort(key=lambda t: t["rank"])
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
{body}{SIGNUP}<p class="m">Last updated {UP}. Rankings are editorial; pricing changes often, check each tool's site.</p></div></body></html>'''
urls = [BASE+"/"]
for c, ts in cats.items():
    s = SLUG.get(c, c.lower().replace(" ", "-").replace("/", ""))
    short = c.split(" /")[0]
    top = ts[0]
    faq = [(f"What is the best AI tool for {short.lower()} in {YEAR}?", f"Our #1 pick is {top['name']}: {top['verdict'].lower()}. Runners-up: " + ", ".join(t['name'] for t in ts[1:3]) + "."),
           (f"Are there free AI tools for {short.lower()}?", "Free tiers or free options: " + (", ".join(t['name'] for t in ts if "free" in t['pricing'].lower() or "open source" in t['pricing'].lower()) or "none in this list") + "."),
           ("How is this list ranked?", f"Editorially by The AI Loadout, based on capability, ease of use and value, and updated as new tools ship. Last updated {UP}.")]
    lis = "".join(f'<li><b><a href="{e(t["url"])}" rel="noopener">{e(t["name"])}</a></b> — {e(t["verdict"])}. <span class="m">{e(t["pricing"])}</span></li>' for t in ts)
    body = f'<h1>Best AI tools for <span>{e(short)}</span> in {YEAR}</h1><p>The {e(c)} loadout: {len(ts)} AI tools ranked for this job, with a one-line verdict on what each is best for. Our top pick right now is <b>{e(top["name"])}</b>.</p><ol>{lis}</ol><h2>FAQ</h2>' + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in faq)
    il = {"@context":"https://schema.org","@type":"ItemList","name":f"Best AI tools for {short} in {YEAR}","dateModified":UP,
          "itemListElement":[{"@type":"ListItem","position":t["rank"],"name":t["name"],"url":t["url"],"description":t["verdict"]} for t in ts]}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    os.makedirs(s, exist_ok=True)
    open(f"{s}/index.html","w").write(page(f"{s}/", f"Best AI tools for {short} in {YEAR} – The AI Loadout", f"The {len(ts)} best AI tools for {short.lower()} in {YEAR}, ranked. #1: {top['name']}.", body, ld(il)+ld(fq)))
    urls.append(f"{BASE}/{s}/")

# ---- per-tool pages ----
import re
def slugify(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
slugs = {}
for t in D["tools"]:
    s = slugify(t["name"])
    if s in slugs.values(): s = s + "-" + SLUG[t["category"]]
    slugs[id(t)] = s
def tslug(t): return slugs[id(t)]
FULL_TOOLS = []
for t in D["tools"]:
    s = tslug(t); c = t["category"]; short = c.split(" /")[0]; peers = [x for x in cats[c] if x is not t]
    faq = [(f"What is {t['name']} best for?", f"{t['verdict']}. It ranks #{t['rank']} of {len(cats[c])} in our {c} loadout."),
           (f"Is {t['name']} free?", f"Pricing: {t['pricing']}. Pricing changes often; check {t['url']}."),
           (f"What are the best alternatives to {t['name']}?", "In the same loadout: " + "; ".join(f"{p['name']} (#{p['rank']}, {p['verdict'].lower()})" for p in peers[:4]) + ".")]
    alts = "".join(f'<li><a href="{BASE}/tools/{tslug(p)}/">{e(p["name"])}</a> (#{p["rank"]}) — {e(p["verdict"])}</li>' for p in peers)
    body = (f'<h1>{e(t["name"])} review: what it\'s best for ({YEAR})</h1>'
            f'<p><b>Verdict:</b> {e(t["verdict"])}.</p><p><b>Rank:</b> #{t["rank"]} of {len(cats[c])} in the <a href="{BASE}/{SLUG[c]}/">{e(c)} loadout</a>.</p>'
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
