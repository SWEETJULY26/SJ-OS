import sys, os, io, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_rows import ROWS, POSITIONS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser("~/Documents/AC-Brands-RACI.html")

def b64(name):
    return io.open(os.path.join(HERE, name + ".b64")).read().strip()

FONT_REG = b64("Adrianna-Regular.ttf")
FONT_DEMI = b64("Adrianna-Demibold.ttf")

INI = [p[0] for p in POSITIONS]
FUNCS = []
for r in ROWS:
    if r[0] not in FUNCS:
        FUNCS.append(r[0])

# ---- counts ----
def counts(ini):
    a = sum(1 for r in ROWS if r[2] == ini)
    rr = sum(1 for r in ROWS if r[3] == ini)
    ar = sum(1 for r in ROWS if r[2] == ini and r[3] == ini)
    inc = sum(1 for r in ROWS if r[6] == ini)          # rows arriving on hire
    out = sum(1 for r in ROWS if r[3] == ini and r[6])  # rows leaving on hire
    return dict(a=a, r=rr, ar=ar, inc=inc, out=out)

CNT = {i: counts(i) for i in INI}

# ---- payload for client-side filtering ----
payload = {
    "positions": [{"id": p[0], "name": p[1], "title": p[2], "status": p[3], **CNT[p[0]]} for p in POSITIONS],
    "functions": FUNCS,
    "rows": [
        {"f": r[0], "a": r[1], "A": r[2], "R": r[3], "C": r[4], "I": r[5],
         "t": r[6], "src": r[7], "n": r[8]}
        for r in ROWS
    ],
}

STATUS_LABEL = {"filled": "", "recruiting": "Open · recruiting now",
                "phased": "Open · phased in after Ops", "contractor": "Contractor",
                "partner": "External partner"}

CHANGES = [
    ("Erin is the technical authority on packaging",
     "Packaging development, artwork execution and the label artwork archive answer to Erin. "
     "Jan executes under her. Perrine consults where formula contact matters."),
    ("Danielle owns brand and campaign direction",
     "Brand guidelines and campaign direction are hers, and she is consulted across Creative and "
     "Marketing rather than only receiving finished work. Ayesha is consulted wherever the brand "
     "carries her name."),
    ("Quality gets a gate",
     "Nicole holds the final quality check on product and documentation across every function. "
     "Each function still owns its own work — the gate sits on top of it, not instead of it."),
    ("Every row now has an owner",
     "Marketing, wholesale and Shopify revenue were the last gaps. They were never ownerless — "
     "they were missing from the sources. Soraya owns Marketing, Nicole owns all channels, "
     "Danielle owns web."),
    ("Our partners are on the matrix",
     "Pedrero on regulatory, Ironclad on finance, Calm HR on people, WITHIN on digital marketing, "
     "Teknologics on web and Coastal Interactive on managed IT. They hold the work; accountability "
     "stays in-house."),
    ("Perrine advises on the technical calls",
     "R&D, Quality, Production and Regulatory requirements for product. She stays accountable for "
     "formula and testing decisions, and consults on everything process-shaped."),
    ("Two seats, in order",
     "Operations Specialist first, recruiting now. Product Development Specialist phased in after. "
     "Both report to Nicole. 32 rows below move to one of them on hire."),
]

def cell(row, ini):
    if row[2] == ini and row[3] == ini:
        return ("ar", "A/R")
    if row[2] == ini:
        return ("a", "A")
    if row[3] == ini:
        return ("r", "R")
    if ini in row[4]:
        return ("c", "C")
    if ini in row[5]:
        return ("i", "I")
    if row[6] == ini:
        return ("t", "→")
    return ("", "")

e = html.escape

# ---------------------------------------------------------------- build
parts = []
parts.append(f"""<style>
@font-face{{font-family:'Adrianna';src:url(data:font/ttf;base64,{FONT_REG}) format('truetype');font-weight:400;font-display:block}}
@font-face{{font-family:'Adrianna';src:url(data:font/ttf;base64,{FONT_DEMI}) format('truetype');font-weight:600;font-display:block}}
:root{{
  --bone:#f4f0e8; --good-youth:#795d50; --pava-brown:#8a665a; --irie:#b08a6c;
  --soursop:#bcab83; --pava:#cab29d; --coffee-fix:#a2b2c8; --lychee:#d7d2cb;
  --pineapple:#f3d54e; --guava:#a9c47f; --rum:#9b5f3a;
  --ground:#f4f0e8; --raised:#fbf9f4; --ink:#2e2521; --ink-soft:#6b5a51;
  --ink-faint:#9a8b81; --rule:#e0d8ca; --rule-strong:#bcab83;
  --a-bg:#8a665a; --a-ink:#fbf9f4; --r-bg:#dfe6ef; --r-ink:#43536b;
  --c-ink:#7d6d63; --i-ink:#a4968c; --chip-open:#f3d54e; --chip-open-ink:#4a3c14;
  --focus:#8a665a;
  --step--1:.78rem; --step-0:.94rem; --step-1:1.18rem; --step-2:1.6rem; --step-3:2.3rem;
}}
@media (prefers-color-scheme:dark){{:root{{
  --ground:#241d19; --raised:#2e2621; --ink:#f0e9df; --ink-soft:#bdaca0;
  --ink-faint:#8b7a6e; --rule:#3d332c; --rule-strong:#5c4a3d;
  --a-bg:#b08a6c; --a-ink:#241d19; --r-bg:#33414f; --r-ink:#bcd0e4;
  --c-ink:#b0a096; --i-ink:#7d6d63; --chip-open:#d8bb3d; --chip-open-ink:#241d19;
  --focus:#cab29d;
}}}}
:root[data-theme="dark"]{{
  --ground:#241d19; --raised:#2e2621; --ink:#f0e9df; --ink-soft:#bdaca0;
  --ink-faint:#8b7a6e; --rule:#3d332c; --rule-strong:#5c4a3d;
  --a-bg:#b08a6c; --a-ink:#241d19; --r-bg:#33414f; --r-ink:#bcd0e4;
  --c-ink:#b0a096; --i-ink:#7d6d63; --chip-open:#d8bb3d; --chip-open-ink:#241d19;
  --focus:#cab29d;
}}
:root[data-theme="light"]{{
  --ground:#f4f0e8; --raised:#fbf9f4; --ink:#2e2521; --ink-soft:#6b5a51;
  --ink-faint:#9a8b81; --rule:#e0d8ca; --rule-strong:#bcab83;
  --a-bg:#8a665a; --a-ink:#fbf9f4; --r-bg:#dfe6ef; --r-ink:#43536b;
  --c-ink:#7d6d63; --i-ink:#a4968c; --chip-open:#f3d54e; --chip-open-ink:#4a3c14;
  --focus:#8a665a;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:'Adrianna',ui-sans-serif,system-ui,sans-serif;font-size:var(--step-0);
  line-height:1.5;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1180px;margin:0 auto;padding:clamp(1.5rem,4vw,3.5rem) clamp(1rem,3vw,2rem) 5rem}}
h1,h2,h3{{font-weight:600;margin:0;text-wrap:balance;color:var(--ink)}}
h1{{font-size:var(--step-3);line-height:1.08;letter-spacing:-.015em}}
h2{{font-size:var(--step-2);line-height:1.15}}
h3{{font-size:var(--step-1)}}
p{{margin:0}}
.eyebrow{{font-size:var(--step--1);text-transform:uppercase;letter-spacing:.14em;
  color:var(--ink-faint);font-weight:600}}
.stack{{display:flex;flex-direction:column}}
header.page{{display:flex;flex-direction:column;gap:.65rem;
  padding-bottom:1.75rem;border-bottom:2px solid var(--rule-strong)}}
header.page .lede{{max-width:62ch;color:var(--ink-soft);font-size:var(--step-1);line-height:1.45}}
.meta{{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:var(--step--1);
  color:var(--ink-faint);margin-top:.5rem}}
section.block{{margin-top:3rem;display:flex;flex-direction:column;gap:1.1rem}}
/* what changed */
.changes{{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr))}}
.change{{background:var(--raised);padding:1.1rem 1.15rem;display:flex;
  flex-direction:column;gap:.4rem}}
.change h3{{font-size:var(--step-0);letter-spacing:.005em}}
.change p{{font-size:var(--step--1);color:var(--ink-soft);line-height:1.55}}
/* position strip */
.pos-strip{{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  grid-template-columns:repeat(auto-fit,minmax(178px,1fr))}}
.pos{{background:var(--raised);border:0;text-align:left;font:inherit;color:inherit;
  padding:.85rem .9rem;display:flex;flex-direction:column;gap:.45rem;cursor:pointer;
  position:relative;transition:background .13s ease}}
.pos:hover{{background:var(--ground)}}
.pos[aria-pressed="true"]{{background:var(--a-bg);color:var(--a-ink)}}
.pos[aria-pressed="true"] .pos-title,.pos[aria-pressed="true"] .tally,
.pos[aria-pressed="true"] .pos-name{{color:var(--a-ink)}}
.pos:focus-visible{{outline:2px solid var(--focus);outline-offset:2px;z-index:2}}
.pos-name{{font-weight:600;font-size:var(--step-0);line-height:1.2}}
.pos-title{{font-size:var(--step--1);color:var(--ink-soft);line-height:1.3}}
.tally{{display:flex;gap:.7rem;font-size:var(--step--1);color:var(--ink-faint);
  font-variant-numeric:tabular-nums;margin-top:auto;padding-top:.3rem}}
.tally b{{font-weight:600;color:var(--ink)}}
.pos[aria-pressed="true"] .tally b{{color:var(--a-ink)}}
.chip{{display:inline-block;font-size:.68rem;text-transform:uppercase;
  letter-spacing:.1em;font-weight:600;padding:.16rem .45rem;border-radius:2px;
  background:var(--chip-open);color:var(--chip-open-ink);width:fit-content}}
.chip.sub{{background:transparent;color:var(--ink-faint);
  border:1px solid var(--rule-strong);padding:.14rem .42rem}}
.chip.partner{{background:transparent;color:var(--r-ink);
  border:1px solid var(--r-ink);padding:.14rem .42rem}}
/* legend */
.legend{{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;font-size:var(--step--1);
  color:var(--ink-soft);align-items:center}}
.legend span{{display:inline-flex;align-items:center;gap:.45rem}}
.mk{{display:inline-grid;place-items:center;width:1.5rem;height:1.35rem;
  font-size:.72rem;font-weight:600;letter-spacing:.03em}}
.mk.a{{background:var(--a-bg);color:var(--a-ink)}}
.mk.r{{background:var(--r-bg);color:var(--r-ink)}}
.mk.ar{{background:var(--a-bg);color:var(--a-ink);font-size:.62rem}}
.mk.c{{color:var(--c-ink)}}
.mk.i{{color:var(--i-ink)}}
.mk.t{{color:var(--ink-faint)}}
/* toolbar */
.toolbar{{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;
  justify-content:space-between}}
.btn{{font:inherit;font-size:var(--step--1);font-weight:600;background:transparent;
  color:var(--ink-soft);border:1px solid var(--rule-strong);padding:.4rem .8rem;
  border-radius:2px;cursor:pointer}}
.btn:hover{{color:var(--ink);border-color:var(--ink-soft)}}
.btn:focus-visible{{outline:2px solid var(--focus);outline-offset:2px}}
.filter-note{{font-size:var(--step--1);color:var(--ink-faint)}}
/* matrix */
details.fn{{border-top:1px solid var(--rule)}}
details.fn:last-of-type{{border-bottom:1px solid var(--rule)}}
details.fn > summary{{cursor:pointer;padding:.85rem .2rem;display:flex;
  align-items:baseline;gap:.75rem;list-style:none}}
details.fn > summary::-webkit-details-marker{{display:none}}
details.fn > summary::before{{content:"+";font-weight:600;color:var(--ink-faint);
  width:1ch;display:inline-block}}
details.fn[open] > summary::before{{content:"–"}}
details.fn > summary:focus-visible{{outline:2px solid var(--focus);outline-offset:-2px}}
.fn-name{{font-weight:600;font-size:var(--step-1)}}
.fn-count{{font-size:var(--step--1);color:var(--ink-faint);
  font-variant-numeric:tabular-nums;margin-left:auto}}
.scroller{{overflow-x:auto;padding-bottom:.4rem}}
table{{border-collapse:collapse;width:100%;min-width:1080px;font-size:var(--step--1)}}
thead th{{position:sticky;top:0;background:var(--ground);text-align:center;
  font-weight:600;font-size:.68rem;letter-spacing:.04em;padding:.4rem .05rem .5rem;
  border-bottom:1px solid var(--rule-strong);color:var(--ink-soft);white-space:nowrap}}
thead th.act{{text-align:left;min-width:230px;width:34%;letter-spacing:.1em;
  text-transform:uppercase;padding-left:0;position:sticky;left:0;
  background:var(--ground);z-index:3}}
tbody td{{border-bottom:1px solid var(--rule);padding:.5rem .05rem;text-align:center;
  vertical-align:middle}}
tbody td.act{{text-align:left;padding:.55rem 1rem .55rem 0;line-height:1.4;
  color:var(--ink);position:sticky;left:0;background:var(--ground);z-index:2}}
tbody tr:hover td{{background:var(--raised)}}
tbody tr:hover td.act{{background:var(--raised)}}
.mk{{min-width:1.35rem}}
tbody tr.dim td.act{{color:var(--ink-faint)}}
td .mk{{margin:0 auto}}
td.col-dim .mk{{opacity:.26}}
.srcbtn{{background:none;border:0;padding:0;font:inherit;font-size:.68rem;
  color:var(--ink-faint);cursor:pointer;text-decoration:underline;
  text-decoration-style:dotted;text-underline-offset:2px;opacity:0;
  transition:opacity .12s ease}}
tbody tr:hover .srcbtn,tbody tr:focus-within .srcbtn,
.srcbtn[aria-expanded="true"]{{opacity:1}}
@media (hover:none){{.srcbtn{{opacity:1}}}}
.srcbtn:hover{{color:var(--ink-soft)}}
.srcbtn:focus-visible{{outline:2px solid var(--focus);outline-offset:2px}}
tr.srcrow td{{padding:0 1rem .7rem 0;text-align:left;
  border-bottom:1px solid var(--rule);position:sticky;left:0;
  background:var(--ground)}}
tr.srcrow .srcwrap{{font-size:var(--step--1);color:var(--ink-soft);
  line-height:1.5;max-width:78ch;display:flex;flex-direction:column;gap:.3rem}}
tr.srcrow code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:.72rem;color:var(--ink-faint);word-break:break-word}}
tr[hidden]{{display:none}}
/* mobile cards */
.cards{{display:none}}
@media (max-width:700px){{
  .scroller{{display:none}}
  .cards{{display:flex;flex-direction:column;gap:1px;background:var(--rule);
    border-block:1px solid var(--rule)}}
  .card{{background:var(--raised);padding:.8rem .85rem;display:flex;
    flex-direction:column;gap:.45rem}}
  .card .who{{display:flex;flex-wrap:wrap;gap:.35rem .9rem;font-size:var(--step--1)}}
  .card .who span{{display:inline-flex;gap:.4rem;align-items:center}}
  .card .lbl{{color:var(--ink-faint);font-size:.68rem;text-transform:uppercase;
    letter-spacing:.08em}}
  h1{{font-size:1.75rem}}
}}
footer.page{{margin-top:3.5rem;padding-top:1.25rem;border-top:1px solid var(--rule);
  font-size:var(--step--1);color:var(--ink-faint);display:flex;
  flex-direction:column;gap:.4rem;max-width:78ch}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>""")

parts.append('<div class="wrap">')

# ---- header
parts.append(f"""<header class="page">
<p class="eyebrow">AC Brands · Operations &amp; Product Development</p>
<h1>Who owns what</h1>
<p class="lede">Accountability across every function, by position. One person answers for each
activity and one person does the work — everyone else is consulted or kept informed.</p>
<div class="meta"><span>{len(ROWS)} activities · {len(FUNCS)} functions</span>
<span>As of 31 July 2026</span>
<span>Reflects the 30 July leadership review and the 31 July role corrections</span></div>
</header>""")

# ---- what changed
parts.append('<section class="block"><h2>What changed</h2><div class="changes">')
for t, b in CHANGES:
    parts.append(f'<article class="change"><h3>{e(t)}</h3><p>{e(b)}</p></article>')
parts.append('</div></section>')

# ---- positions
parts.append("""<section class="block">
<h2>Positions</h2>
<p class="filter-note">Select a position to see only the activities it touches. Select again to clear.</p>
<div class="pos-strip" id="posStrip">""")
for pid, name, title, status in POSITIONS:
    c = CNT[pid]
    chip = ""
    if status in ("recruiting", "phased"):
        chip = f'<span class="chip">{e(STATUS_LABEL[status])}</span>'
    elif status in ("contractor", "partner"):
        cls = "chip sub" if status == "contractor" else "chip partner"
        chip = f'<span class="{cls}">{e(STATUS_LABEL[status])}</span>'
    if status in ("recruiting", "phased"):
        tally = f'<span>Absorbs <b>{c["inc"]}</b></span>'
    else:
        tally = f'<span>A <b>{c["a"]}</b></span><span>R <b>{c["r"]}</b></span>'
        if c["out"]:
            tally += f'<span>Hands off <b>{c["out"]}</b></span>'
    parts.append(f"""<button class="pos" type="button" data-pos="{pid}" aria-pressed="false">
<span class="pos-name">{e(name)}</span><span class="pos-title">{e(title)}</span>
{chip}<span class="tally">{tally}</span></button>""")
parts.append('</div></section>')

# ---- legend
parts.append("""<section class="block"><h2>The matrix</h2>
<div class="legend">
<span><i class="mk a">A</i> Answers for the outcome</span>
<span><i class="mk r">R</i> Does the work</span>
<span><i class="mk ar">A/R</i> Both, so no second pair of eyes</span>
<span><i class="mk c">C</i> Consulted</span>
<span><i class="mk i">I</i> Informed</span>
<span><i class="mk t">→</i> Moves here on hire</span>
</div>
<div class="toolbar">
<div><button class="btn" type="button" id="expandAll">Expand all</button>
<button class="btn" type="button" id="collapseAll">Collapse all</button></div>
<span class="filter-note" id="filterState">Showing all positions</span>
</div>""")

# ---- function tables
head_cells = "".join(
    f'<th data-col="{p[0]}" title="{e(p[1])} — {e(p[2])}">{p[0]}</th>' for p in POSITIONS)
ri = 0
for fi, fn in enumerate(FUNCS):
    frows = [r for r in ROWS if r[0] == fn]
    op = " open" if fi < 2 else ""
    parts.append(f'<details class="fn" data-fn="{e(fn)}"{op}><summary>'
                 f'<span class="fn-name">{e(fn)}</span>'
                 f'<span class="fn-count">{len(frows)} activities</span></summary>')
    # desktop table
    parts.append(f'<div class="scroller"><table><thead><tr>'
                 f'<th class="act">Activity</th>{head_cells}</tr></thead><tbody>')
    for r in frows:
        ri += 1
        tds = []
        for pid in INI:
            cls, txt = cell(r, pid)
            inner = f'<i class="mk {cls}">{txt}</i>' if txt else ""
            tds.append(f'<td data-col="{pid}">{inner}</td>')
        parts.append(
            f'<tr data-row="{ri}"><td class="act">{e(r[1])}<br>'
            f'<button class="srcbtn" type="button" data-src="{ri}" '
            f'aria-expanded="false" aria-controls="src{ri}">source</button></td>'
            + "".join(tds) + '</tr>')
        parts.append(
            f'<tr class="srcrow" id="src{ri}" hidden><td colspan="{len(INI)+1}">'
            f'<div class="srcwrap"><span>{e(r[8])}</span><code>{e(r[7])}</code></div></td></tr>')
    parts.append('</tbody></table></div>')
    # mobile cards
    parts.append('<div class="cards">')
    for r in frows:
        def nm(i):
            for p in POSITIONS:
                if p[0] == i:
                    return p[1] if p[3] == "filled" or p[3] == "contractor" else p[2]
            return i
        xfer = (f'<span><span class="lbl">moves to</span>'
                f'{e(nm(r[6]))}</span>') if r[6] else ""
        parts.append(f"""<div class="card"><strong>{e(r[1])}</strong>
<div class="who"><span><i class="mk a">A</i>{e(nm(r[2]))}</span>
<span><i class="mk r">R</i>{e(nm(r[3]))}</span>{xfer}</div></div>""")
    parts.append('</div></details>')

parts.append('</section>')

# ---- footer
parts.append(f"""<footer class="page">
<p><strong>How this was built.</strong> Every row traces to a source — the operating procedures and
role definitions in the SJ-OS repository, the two specialist job descriptions, or the 30 July
leadership review. Open any row's source link to see which.</p>
<p>One row has no documented owner and shows the VP of Operations by default because the work falls
there in practice: Shopify revenue and channel position. It is marked as inferred rather than
sourced. Accounts payable and HR onboarding used to sit here too, and are now owned by Ironclad
Finance and Calm HR.</p>
<p><strong>Partner organisations</strong> hold the work but never the accountability — that stays with
an employee. Pedrero Regulatory is consulted rather than responsible because our procedures make
them consult-only, with no access to our systems.</p>
<p>Coverage is Sweet July Skin plus company-wide work. Sweet July, the lifestyle brand, is not
represented — nothing in our operating documentation defines who owns it.</p>
<p>Questions or a row that looks wrong: Alvin.</p>
</footer>""")

parts.append('</div>')

# ---- script
parts.append("""<script>
(function(){
  var strip=document.getElementById('posStrip'), state=document.getElementById('filterState');
  var active=null;
  function apply(){
    document.querySelectorAll('[data-col]').forEach(function(el){
      el.classList.toggle('col-dim', !!active && el.getAttribute('data-col')!==active);
    });
    document.querySelectorAll('tbody tr[data-row]').forEach(function(tr){
      var show=true;
      if(active){
        var td=tr.querySelector('td[data-col="'+active+'"]');
        show = !!(td && td.querySelector('.mk'));
      }
      tr.hidden=!show;
      var s=document.getElementById('src'+tr.getAttribute('data-row'));
      if(s && !show) s.hidden=true;
    });
    document.querySelectorAll('details.fn').forEach(function(d){
      var vis=d.querySelectorAll('tbody tr[data-row]:not([hidden])').length;
      d.hidden = !!active && vis===0;
      if(active && vis>0) d.open=true;
      var c=d.querySelector('.fn-count');
      var total=d.querySelectorAll('tbody tr[data-row]').length;
      c.textContent = active ? vis+' of '+total+' activities' : total+' activities';
    });
    if(active){
      var b=strip.querySelector('[data-pos="'+active+'"]');
      state.textContent='Showing '+b.querySelector('.pos-name').textContent.trim()+
        ' — '+b.querySelector('.pos-title').textContent.trim();
    } else { state.textContent='Showing all positions'; }
  }
  strip.addEventListener('click',function(ev){
    var b=ev.target.closest('.pos'); if(!b) return;
    var id=b.getAttribute('data-pos');
    active = (active===id) ? null : id;
    strip.querySelectorAll('.pos').forEach(function(x){
      x.setAttribute('aria-pressed', x.getAttribute('data-pos')===active ? 'true':'false');
    });
    apply();
  });
  document.addEventListener('click',function(ev){
    var s=ev.target.closest('.srcbtn'); if(!s) return;
    var row=document.getElementById('src'+s.getAttribute('data-src'));
    if(row){ row.hidden=!row.hidden;
      s.setAttribute('aria-expanded', row.hidden ? 'false':'true'); }
  });
  document.getElementById('expandAll').addEventListener('click',function(){
    document.querySelectorAll('details.fn').forEach(function(d){d.open=true;});
  });
  document.getElementById('collapseAll').addEventListener('click',function(){
    document.querySelectorAll('details.fn').forEach(function(d){d.open=false;});
  });
  apply();
})();
</script>""")

io.open(OUT, "w", encoding="utf-8").write(
    "<title>AC Brands — Who owns what</title>\n" + "\n".join(parts))
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
