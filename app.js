let D,cat="All";const $=s=>document.querySelector(s),e=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
fetch("tools.json").then(r=>r.json()).then(d=>{D=d;$("#up").textContent=d.updated;
$("#rel").innerHTML=d.releases.map(r=>`<div class="card rel"><div class="date">${e(r.date)}</div><a class="n" href="${e(r.url)}" target="_blank" rel="noopener">${e(r.name)}</a><p>${e(r.what)}</p><span class="tag">via ${e(r.source)}</span></div>`).join("");
const cats=["All",...new Set(d.tools.map(t=>t.category))];
$("#chips").innerHTML=cats.map(c=>`<button class="chip${c==cat?' on':''}">${e(c)}</button>`).join("");
$("#chips").onclick=ev=>{if(ev.target.tagName!="BUTTON")return;cat=ev.target.textContent;[...$("#chips").children].forEach(b=>b.classList.toggle("on",b.textContent==cat));draw()};
$("#q").oninput=draw;draw()});
function draw(){const q=$("#q").value.toLowerCase();const g={};
D.tools.filter(t=>(cat=="All"||t.category==cat)&&(!q||Object.values(t).join(" ").toLowerCase().includes(q))).forEach(t=>(g[t.category]=g[t.category]||[]).push(t));
$("#list").innerHTML=Object.keys(g).map(c=>`<h3>${e(c)} loadout</h3><div class="grid">${g[c].sort((a,b)=>(!!b.featured-!!a.featured)||a.rank-b.rank).map(t=>`<div class="card"><span class="r"><span class="tier t${e(t.tier)}">${e(t.tier)}</span> #${t.rank}</span><a class="n" href="tools/${e(t.slug)}/">${e(t.name)}</a>${t.featured?' <span class="tier" style="background:#ffd700">★ Featured</span>':''}<p>${e(t.verdict)}</p><span class="tag">${e(t.pricing)} · <a href="${e(t.url)}" target="_blank" rel="noopener">official ↗</a></span></div>`).join("")}</div>`).join("")||"<p>No tools match.</p>"}
