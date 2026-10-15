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
def page(path, title, desc, body, extra=""):
    url = f"{BASE}/{path}"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/og.svg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<meta property="article:modified_time" content="{UP}">{ld(ORG)}{extra}<style>{CSS}</style></head><body><div class="w">
<nav><a href="{BASE}/">← The AI Loadout</a>{"".join(f'<a href="{BASE}/{s}/">{e(c)}</a>' for c,s in SLUG.items() if c in cats)}</nav>
{body}<p class="m">Last updated {UP}. Rankings are editorial; pricing changes often, check each tool's site.</p></div></body></html>'''
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
F.append("\n## New releases\n" + "".join(f"- {r['date']}: {r['name']} — {r['what']} (source: {r['url']})\n" for r in D["releases"]))
open("llms-full.txt","w").write("".join(F))
print(f"built {len(cats)} category pages, {len(urls)} sitemap URLs")
