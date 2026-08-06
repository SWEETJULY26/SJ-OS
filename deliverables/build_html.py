import sys, os, io, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_rows import ROWS, POSITIONS
from activity_notes import INFO

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser("~/Documents/AC-Brands-RACI.html")

def b64(name):
    return io.open(os.path.join(HERE, name + ".b64")).read().strip()

FONT_REG = b64("Adrianna-Regular.ttf")
FONT_DEMI = b64("Adrianna-Demibold.ttf")

FUNCS = []
for r in ROWS:
    if r[0] not in FUNCS:
        FUNCS.append(r[0])

# The published baseline. Everything on the page renders from this, and an
# edited copy lives in the viewer's browser until they revert.
PUB = {
    "version": "v7",
    "asOf": "31 July 2026",
    "positions": [{"id": p[0], "name": p[1], "title": p[2], "status": p[3]}
                  for p in POSITIONS],
    "functions": FUNCS,
    "rows": [{"f": r[0], "act": r[1], "A": ([r[2]] if r[2] else []), "R": r[3],
              "C": list(r[4]), "I": list(r[5]),
              "t": r[6] or "", "src": r[7], "n": r[8],
              "what": INFO.get(r[1], {}).get("what", ""),
              "eg": INFO.get(r[1], {}).get("example", "")}
             for r in ROWS],
}

e = html.escape

CSS = """
:root{
  --bone:#f4f0e8; --good-youth:#795d50; --pava-brown:#8a665a; --irie:#b08a6c;
  --soursop:#bcab83; --pava:#cab29d; --coffee-fix:#a2b2c8; --lychee:#d7d2cb;
  --pineapple:#f3d54e; --guava:#a9c47f; --rum:#9b5f3a;
  --ground:#f4f0e8; --raised:#fbf9f4; --ink:#2e2521; --ink-soft:#6b5a51;
  --ink-faint:#9a8b81; --rule:#e0d8ca; --rule-strong:#bcab83;
  --a-bg:#8a665a; --a-ink:#fbf9f4; --r-bg:#dfe6ef; --r-ink:#43536b;
  --c-ink:#7d6d63; --i-ink:#a4968c; --chip-open:#f3d54e; --chip-open-ink:#4a3c14;
  --focus:#8a665a; --warn:#9b5f3a; --edit:#a9c47f; --edit-ink:#2f4318;
  --step--1:.78rem; --step-0:.94rem; --step-1:1.18rem; --step-2:1.6rem; --step-3:2.3rem;
}
@media (prefers-color-scheme:dark){:root{
  --ground:#241d19; --raised:#2e2621; --ink:#f0e9df; --ink-soft:#bdaca0;
  --ink-faint:#8b7a6e; --rule:#3d332c; --rule-strong:#5c4a3d;
  --a-bg:#b08a6c; --a-ink:#241d19; --r-bg:#33414f; --r-ink:#bcd0e4;
  --c-ink:#b0a096; --i-ink:#7d6d63; --chip-open:#d8bb3d; --chip-open-ink:#241d19;
  --focus:#cab29d; --warn:#d9a077; --edit:#5d7a3c; --edit-ink:#eef5e4;
}}
:root[data-theme="dark"]{
  --ground:#241d19; --raised:#2e2621; --ink:#f0e9df; --ink-soft:#bdaca0;
  --ink-faint:#8b7a6e; --rule:#3d332c; --rule-strong:#5c4a3d;
  --a-bg:#b08a6c; --a-ink:#241d19; --r-bg:#33414f; --r-ink:#bcd0e4;
  --c-ink:#b0a096; --i-ink:#7d6d63; --chip-open:#d8bb3d; --chip-open-ink:#241d19;
  --focus:#cab29d; --warn:#d9a077; --edit:#5d7a3c; --edit-ink:#eef5e4;
}
:root[data-theme="light"]{
  --ground:#f4f0e8; --raised:#fbf9f4; --ink:#2e2521; --ink-soft:#6b5a51;
  --ink-faint:#9a8b81; --rule:#e0d8ca; --rule-strong:#bcab83;
  --a-bg:#8a665a; --a-ink:#fbf9f4; --r-bg:#dfe6ef; --r-ink:#43536b;
  --c-ink:#7d6d63; --i-ink:#a4968c; --chip-open:#f3d54e; --chip-open-ink:#4a3c14;
  --focus:#8a665a; --warn:#9b5f3a; --edit:#a9c47f; --edit-ink:#2f4318;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:'Adrianna',ui-sans-serif,system-ui,sans-serif;font-size:var(--step-0);
  line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:clamp(1.5rem,4vw,3.5rem) clamp(1rem,3vw,2rem) 6rem}
h1,h2,h3{font-weight:600;margin:0;text-wrap:balance;color:var(--ink)}
h1{font-size:var(--step-3);line-height:1.08;letter-spacing:-.015em}
h2{font-size:var(--step-2);line-height:1.15}
h3{font-size:var(--step-1)}
p{margin:0}
.eyebrow{font-size:var(--step--1);text-transform:uppercase;letter-spacing:.14em;
  color:var(--ink-faint);font-weight:600}
header.page{display:flex;flex-direction:column;gap:.65rem;
  padding-bottom:1.75rem;border-bottom:2px solid var(--rule-strong)}
header.page .lede{max-width:62ch;color:var(--ink-soft);font-size:var(--step-1);line-height:1.45}
.meta{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:var(--step--1);
  color:var(--ink-faint);margin-top:.5rem}
section.block{margin-top:3rem;display:flex;flex-direction:column;gap:1.1rem}
/* position strip */
.pos-strip{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  grid-template-columns:repeat(auto-fit,minmax(178px,1fr))}
.pos{background:var(--raised);border:0;text-align:left;font:inherit;color:inherit;
  padding:.85rem .9rem;display:flex;flex-direction:column;gap:.45rem;cursor:pointer;
  position:relative;transition:background .13s ease}
.pos:hover{background:var(--ground)}
.pos[aria-pressed="true"]{background:var(--a-bg);color:var(--a-ink)}
.pos[aria-pressed="true"] .pos-title,.pos[aria-pressed="true"] .tally,
.pos[aria-pressed="true"] .pos-name{color:var(--a-ink)}
.pos:focus-visible{outline:2px solid var(--focus);outline-offset:2px;z-index:2}
.pos-name{font-weight:600;font-size:var(--step-0);line-height:1.2}
.pos-title{font-size:var(--step--1);color:var(--ink-soft);line-height:1.3}
.tally{display:flex;gap:.7rem;font-size:var(--step--1);color:var(--ink-faint);
  font-variant-numeric:tabular-nums;margin-top:auto;padding-top:.3rem}
.tally b{font-weight:600;color:var(--ink)}
.pos[aria-pressed="true"] .tally b{color:var(--a-ink)}
.chip{display:inline-block;font-size:.68rem;text-transform:uppercase;
  letter-spacing:.1em;font-weight:600;padding:.16rem .45rem;border-radius:2px;
  background:var(--chip-open);color:var(--chip-open-ink);width:fit-content}
.chip.sub{background:transparent;color:var(--ink-faint);
  border:1px solid var(--rule-strong);padding:.14rem .42rem}
.chip.partner{background:transparent;color:var(--r-ink);
  border:1px solid var(--r-ink);padding:.14rem .42rem}
/* legend */
.legend{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;font-size:var(--step--1);
  color:var(--ink-soft);align-items:center}
.legend span{display:inline-flex;align-items:center;gap:.45rem}
.mk{display:inline-grid;place-items:center;width:1.5rem;height:1.35rem;
  font-size:.72rem;font-weight:600;letter-spacing:.03em;min-width:1.35rem}
.mk.a{background:var(--a-bg);color:var(--a-ink)}
.mk.r{background:var(--r-bg);color:var(--r-ink)}
.mk.ar{background:var(--a-bg);color:var(--a-ink);font-size:.62rem}
.mk.c{color:var(--c-ink)}
.mk.i{color:var(--i-ink)}
.mk.t{color:var(--ink-faint)}
/* toolbar */
.toolbar{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;
  justify-content:space-between}
.btnrow{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.btn{font:inherit;font-size:var(--step--1);font-weight:600;background:transparent;
  color:var(--ink-soft);border:1px solid var(--rule-strong);padding:.4rem .8rem;
  border-radius:2px;cursor:pointer}
.btn:hover{color:var(--ink);border-color:var(--ink-soft)}
.btn:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.btn[aria-pressed="true"]{background:var(--edit);color:var(--edit-ink);
  border-color:var(--edit)}
.btn.quiet{border-color:transparent;color:var(--ink-faint)}
.btn.quiet:hover{border-color:var(--rule)}
.filter-note{font-size:var(--step--1);color:var(--ink-faint)}
/* edit banner */
.banner{display:none;gap:.75rem 1.1rem;align-items:baseline;flex-wrap:wrap;
  border:1px solid var(--rule-strong);border-left:3px solid var(--edit);
  background:var(--raised);padding:.7rem .9rem;font-size:var(--step--1);
  color:var(--ink-soft)}
.banner.on{display:flex}
.banner b{color:var(--ink)}
.banner .warn{color:var(--warn);font-weight:600}
/* matrix */
details.fn{border-top:1px solid var(--rule)}
details.fn:last-of-type{border-bottom:1px solid var(--rule)}
details.fn > summary{cursor:pointer;padding:.85rem .2rem;display:flex;
  align-items:baseline;gap:.75rem;list-style:none}
details.fn > summary::-webkit-details-marker{display:none}
details.fn > summary::before{content:"+";font-weight:600;color:var(--ink-faint);
  width:1ch;display:inline-block}
details.fn[open] > summary::before{content:"\\2212"}
details.fn > summary:focus-visible{outline:2px solid var(--focus);outline-offset:-2px}
.fn-name{font-weight:600;font-size:var(--step-1)}
.fn-count{font-size:var(--step--1);color:var(--ink-faint);
  font-variant-numeric:tabular-nums;margin-left:auto}
.fn-name[contenteditable="true"]{outline:1px dashed var(--rule-strong);
  outline-offset:3px;min-width:6ch}
.scroller{overflow-x:auto;padding-bottom:.4rem}
table{border-collapse:collapse;width:100%;min-width:1000px;font-size:var(--step--1)}
thead th{position:sticky;top:0;background:var(--ground);text-align:center;
  font-weight:600;font-size:.68rem;letter-spacing:.04em;padding:.4rem .05rem .5rem;
  border-bottom:1px solid var(--rule-strong);color:var(--ink-soft);white-space:nowrap}
thead th.act{text-align:left;min-width:230px;width:32%;letter-spacing:.1em;
  text-transform:uppercase;padding-left:0;position:sticky;left:0;
  background:var(--ground);z-index:3}
thead th.tools{width:1%}
tbody td{border-bottom:1px solid var(--rule);padding:.5rem .05rem;text-align:center;
  vertical-align:middle}
tbody td.act{text-align:left;padding:.55rem 1rem .55rem 0;line-height:1.4;
  color:var(--ink);position:sticky;left:0;background:var(--ground);z-index:2}
tbody tr:hover td{background:var(--raised)}
tbody tr:hover td.act{background:var(--raised)}
tbody tr.flag td.act{box-shadow:inset 3px 0 0 var(--warn)}
tbody tr.flag td.act{padding-left:.55rem}
td.col-dim .mk{opacity:.26}
.acttext{display:block}
.acttext[contenteditable="true"]{outline:1px dashed var(--rule-strong);
  outline-offset:3px;min-height:1.4em}
.rowmsg{display:block;font-size:.68rem;color:var(--warn);margin-top:.2rem}
tr[hidden]{display:none}
/* the activity opens a breakdown */
.actbtn{background:none;border:0;padding:0;margin:0;font:inherit;text-align:left;
  color:var(--ink);cursor:pointer;width:100%;line-height:1.4;
  text-decoration:underline;text-decoration-color:transparent;
  text-decoration-thickness:1px;text-underline-offset:3px;
  transition:text-decoration-color .12s ease}
.actbtn:hover{text-decoration-color:var(--rule-strong)}
.actbtn:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.cardbtn{background:none;border:0;padding:0;font:inherit;font-weight:600;
  text-align:left;color:var(--ink);cursor:pointer}
.cardbtn:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
/* drawer */
.scrim{position:fixed;inset:0;background:rgba(20,15,12,.42);z-index:30;
  opacity:0;transition:opacity .18s ease}
.scrim.on{opacity:1}
body.drawer-open{overflow:hidden}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(30rem,100vw);
  background:var(--raised);border-left:1px solid var(--rule-strong);z-index:31;
  display:flex;flex-direction:column;transform:translateX(100%);
  transition:transform .18s ease;box-shadow:-12px 0 32px rgba(20,15,12,.14)}
.drawer.on{transform:translateX(0)}
.drawer-close{align-self:flex-end;margin:.85rem .95rem 0;font:inherit;
  font-size:var(--step--1);font-weight:600;background:transparent;
  color:var(--ink-soft);border:1px solid var(--rule-strong);border-radius:2px;
  padding:.3rem .7rem;cursor:pointer;flex:none}
.drawer-close:hover{color:var(--ink);border-color:var(--ink-soft)}
.drawer-close:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.drawer-body{overflow-y:auto;padding:.4rem clamp(1.1rem,3vw,1.6rem) 2.5rem;
  display:flex;flex-direction:column;gap:1.2rem}
.drawer-body h3{font-size:var(--step-1);line-height:1.25}
.drawer-body .eyebrow{margin-bottom:-.75rem}
.d-sec{display:flex;flex-direction:column;gap:.4rem}
.d-sec h4{font-size:.68rem;text-transform:uppercase;letter-spacing:.11em;
  font-weight:600;color:var(--ink-faint);margin:0}
.d-sec p{font-size:var(--step--1);line-height:1.6;color:var(--ink-soft);max-width:46ch}
.d-sec p.eg{border-left:2px solid var(--soursop);padding-left:.7rem;color:var(--ink)}
.d-sec p.muted{color:var(--ink-faint)}
.d-sec p.warn-line{color:var(--warn);font-weight:600}
.d-sec code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:.7rem;color:var(--ink-faint);word-break:break-word;line-height:1.5}
.who-wrap{display:flex;flex-direction:column;gap:.5rem}
.who-row{display:grid;grid-template-columns:6.5rem 1fr;gap:.5rem;
  font-size:var(--step--1);align-items:baseline}
.who-lbl{color:var(--ink-faint);font-size:.68rem;text-transform:uppercase;
  letter-spacing:.08em}
.who-names{display:flex;flex-direction:column;gap:.25rem}
.who-chip{color:var(--ink-soft);line-height:1.35}
.who-chip b{color:var(--ink);font-weight:600}
@media (max-width:700px){
  .drawer{width:100vw;border-left:0;top:auto;height:88vh;
    border-top-left-radius:6px;border-top-right-radius:6px;
    transform:translateY(100%)}
  .drawer.on{transform:translateY(0)}
}
@media (prefers-reduced-motion:reduce){.drawer,.scrim{transition:none}}
/* editable cells */
.cellbtn{width:100%;min-height:1.9rem;background:none;border:0;padding:0;
  font:inherit;cursor:pointer;display:grid;place-items:center;border-radius:2px}
.cellbtn:hover{background:var(--rule)}
.cellbtn:focus-visible{outline:2px solid var(--focus);outline-offset:-2px}
.cellbtn .mk.empty{color:var(--ink-faint);opacity:.45;font-weight:400}
.rowtools{display:flex;gap:.15rem;justify-content:flex-end;white-space:nowrap}
.icb{font:inherit;font-size:.8rem;line-height:1;background:none;border:1px solid transparent;
  color:var(--ink-faint);cursor:pointer;padding:.15rem .3rem;border-radius:2px}
.icb:hover{color:var(--ink);border-color:var(--rule-strong)}
.icb:focus-visible{outline:2px solid var(--focus);outline-offset:1px}
.icb.del:hover{color:var(--warn);border-color:var(--warn)}
.fnsel{font:inherit;font-size:.68rem;background:var(--raised);color:var(--ink-soft);
  border:1px solid var(--rule);border-radius:2px;max-width:8.5rem}
.addrow{padding:.6rem 0 .9rem}
/* mobile cards */
.cards{display:none}
@media (max-width:700px){
  .scroller{display:none}
  .cards{display:flex;flex-direction:column;gap:1px;background:var(--rule);
    border-block:1px solid var(--rule)}
  .card{background:var(--raised);padding:.8rem .85rem;display:flex;
    flex-direction:column;gap:.45rem}
  .card .who{display:flex;flex-wrap:wrap;gap:.35rem .9rem;font-size:var(--step--1)}
  .card .who span{display:inline-flex;gap:.4rem;align-items:center}
  .card .lbl{color:var(--ink-faint);font-size:.68rem;text-transform:uppercase;
    letter-spacing:.08em}
  h1{font-size:1.75rem}
  body.editing .cards{display:none}
  body.editing .scroller{display:block}
}
/* inline form, since the sandboxed frame blocks prompt() */
.inline-form{display:inline-flex;gap:.4rem;align-items:center}
.inline-form input{font:inherit;font-size:var(--step--1);background:var(--raised);
  color:var(--ink);border:1px solid var(--rule-strong);border-radius:2px;
  padding:.35rem .5rem;min-width:15rem}
.inline-form input:focus-visible{outline:2px solid var(--focus);outline-offset:1px}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);
  white-space:nowrap}
/* toast */
.toast-act{font:inherit;font-size:var(--step--1);font-weight:600;
  background:transparent;color:var(--ground);border:1px solid var(--ground);
  border-radius:2px;padding:.15rem .5rem;margin-left:.65rem;cursor:pointer}
.toast-act:hover{background:var(--ground);color:var(--ink)}
.toast-act:focus-visible{outline:2px solid var(--ground);outline-offset:2px}
.toast{position:fixed;left:50%;bottom:1.25rem;transform:translateX(-50%);
  background:var(--ink);color:var(--ground);font-size:var(--step--1);
  padding:.55rem .95rem;border-radius:3px;max-width:min(92vw,52ch);
  opacity:0;pointer-events:none;transition:opacity .18s ease;z-index:20;
  text-align:center;display:flex;align-items:center;justify-content:center;
  flex-wrap:wrap;gap:.15rem}
.toast.on{opacity:1;pointer-events:auto}
footer.page{margin-top:3.5rem;padding-top:1.25rem;border-top:1px solid var(--rule);
  font-size:var(--step--1);color:var(--ink-faint);display:flex;
  flex-direction:column;gap:.4rem;max-width:78ch}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = r"""
(function(){
  var PUB = window.__RACI__;
  var KEY = 'acb-raci-' + PUB.version;
  var D, editing = false, active = null, dirty = false;

  function clone(x){ return JSON.parse(JSON.stringify(x)); }

  function load(){
    try {
      var raw = localStorage.getItem(KEY);
      if(!raw) return null;
      var d = JSON.parse(raw);
      if(!d || !Array.isArray(d.rows) || !Array.isArray(d.functions)) return null;
      return d;
    } catch(err){ return null; }
  }
  function save(){
    dirty = true;
    try { localStorage.setItem(KEY, JSON.stringify(D)); }
    catch(err){ toast('Could not save locally. Export before you close the tab.'); }
    banner();
  }

  var saved = load();
  D = saved || clone(PUB);
  dirty = !!saved;

  // ---- position helpers
  function pos(id){
    for(var i=0;i<D.positions.length;i++) if(D.positions[i].id===id) return D.positions[i];
    return null;
  }
  function isOpen(id){ var p=pos(id); return !!p && (p.status==='recruiting'||p.status==='phased'); }
  function isPartner(id){ var p=pos(id); return !!p && p.status==='partner'; }
  function label(id){
    var p = pos(id); if(!p) return id || '';
    return (p.status==='filled'||p.status==='contractor') ? p.name : p.title;
  }

  // A row's letter for one position. '' | 'C' | 'I' | 'R' | 'A' | 'AR'
  function letterOf(row, id){
    var isA = row.A.indexOf(id)>-1;
    if(isA && row.R===id) return 'AR';
    if(isA) return 'A';
    if(row.R===id) return 'R';
    if(row.C.indexOf(id)>-1) return 'C';
    if(row.I.indexOf(id)>-1) return 'I';
    if(row.t===id) return 'T';
    return '';
  }
  var MK = {A:['a','A'], R:['r','R'], AR:['ar','A/R'], C:['c','C'], I:['i','I'], T:['t','\u2192']};

  function strip(row, id){
    row.A = row.A.filter(function(x){ return x!==id; });
    if(row.R===id) row.R = '';
    row.C = row.C.filter(function(x){ return x!==id; });
    row.I = row.I.filter(function(x){ return x!==id; });
    if(row.t===id) row.t = '';
  }

  // The two states that claim R sit at the end on purpose, so reaching C, I or A
  // never touches R. A vacancy cannot be accountable or responsible, and
  // accountability never leaves the company, so partners get no A and no A/R.
  function cycle(id){
    if(isOpen(id)) return ['','T','C','I'];
    if(isPartner(id)) return ['','C','I','R'];
    return ['','C','I','A','AR','R'];
  }
  function takesR(state){ return state==='R' || state==='AR'; }

  // Returns the letters this assignment took off other positions, so the change
  // is never silent. One A and one R per activity is the whole point.
  function setLetter(row, id, next){
    var moved = [];
    strip(row, id);
    if(next==='C') row.C.push(id);
    else if(next==='I') row.I.push(id);
    else if(next==='T') row.t = id;
    else if(next==='R'){
      if(row.R && row.R!==id) moved.push(['R', row.R]);
      row.R = id;
    }
    else if(next==='A'){
      // More than one A is allowed, so taking A displaces nobody.
      row.A.push(id);
    }
    else if(next==='AR'){
      if(row.R && row.R!==id) moved.push(['R', row.R]);
      row.A.push(id); row.R = id;
    }
    return moved;
  }

  // back=true steps backwards, so overshooting a cell costs one shift-click
  // rather than a lap through every other letter.
  function bump(row, id, back){
    var order = cycle(id), cur = letterOf(row, id);
    var L = order.length;
    var at = order.indexOf(cur);
    if(at<0) at = 0;
    var step = back ? -1 : 1;
    // R is single. Cycling must never take it off another position, or clicking
    // one cell quietly rewrites a different one. Step over any state that would
    // claim a taken R and say who has it: clear their cell first to move it.
    var blocked = '', next = cur;
    for(var k = 1; k <= L; k++){
      next = order[(((at + k*step) % L) + L) % L];
      if(takesR(next) && row.R && row.R !== id){ blocked = row.R; continue; }
      break;
    }
    return {next: next, moved: setLetter(row, id, next), blocked: blocked};
  }

  // ---- counts
  function counts(id){
    var a=0,r=0,ar=0,inc=0,out=0;
    D.rows.forEach(function(row){
      if(row.A.indexOf(id)>-1) a++;
      if(row.R===id) r++;
      if(row.A.indexOf(id)>-1 && row.R===id) ar++;
      if(row.t===id) inc++;
      if(row.R===id && row.t) out++;
    });
    return {a:a,r:r,ar:ar,inc:inc,out:out};
  }
  function problems(){
    var miss=0, both=0, multi=0;
    D.rows.forEach(function(row){
      if(!row.A.length || !row.R) miss++;
      if(row.R && row.A.indexOf(row.R)>-1) both++;
      if(row.A.length>1) multi++;
    });
    return {miss:miss, both:both, multi:multi};
  }

  // ---- rendering
  var stripEl = document.getElementById('posStrip');
  var matrix  = document.getElementById('matrix');
  var stateEl = document.getElementById('filterState');
  var bannerEl= document.getElementById('banner');
  var toastEl = document.getElementById('toast');
  var metaEl  = document.getElementById('meta');

  var STATUS = {filled:'', recruiting:'Open \u00b7 recruiting now',
                phased:'Open \u00b7 phased in after Ops', contractor:'Contractor',
                partner:'External partner'};

  function el(tag, cls, text){
    var n = document.createElement(tag);
    if(cls) n.className = cls;
    if(text!=null) n.textContent = text;
    return n;
  }

  function renderPositions(){
    stripEl.textContent = '';
    D.positions.forEach(function(p){
      var c = counts(p.id);
      var b = el('button','pos'); b.type='button';
      b.setAttribute('data-pos', p.id);
      b.setAttribute('aria-pressed', active===p.id ? 'true':'false');
      b.appendChild(el('span','pos-name', p.name));
      b.appendChild(el('span','pos-title', p.title));
      if(p.status==='recruiting'||p.status==='phased')
        b.appendChild(el('span','chip', STATUS[p.status]));
      else if(p.status==='contractor')
        b.appendChild(el('span','chip sub', STATUS[p.status]));
      else if(p.status==='partner')
        b.appendChild(el('span','chip partner', STATUS[p.status]));
      var t = el('span','tally');
      if(p.status==='recruiting'||p.status==='phased'){
        t.appendChild(tal('Absorbs', c.inc));
      } else {
        t.appendChild(tal('A', c.a)); t.appendChild(tal('R', c.r));
        if(c.out) t.appendChild(tal('Hands off', c.out));
      }
      b.appendChild(t);
      stripEl.appendChild(b);
    });
  }
  function tal(k,v){
    var s = el('span'); s.appendChild(document.createTextNode(k+' '));
    var b = el('b', null, String(v)); s.appendChild(b); return s;
  }

  function rowsOf(fn){ return D.rows.filter(function(r){ return r.f===fn; }); }

  function renderMatrix(){
    matrix.textContent = '';
    D.functions.forEach(function(fn, fi){
      var frows = rowsOf(fn);
      var d = el('details','fn');
      d.setAttribute('data-fn', fn);
      if(openState[fn]===undefined) openState[fn] = fi < 2;
      d.open = !!openState[fn];
      d.addEventListener('toggle', function(){ openState[fn] = d.open; });

      var s = el('summary');
      var nm = el('span','fn-name', fn);
      if(editing){
        nm.contentEditable = 'true';
        nm.addEventListener('keydown', function(ev){
          if(ev.key==='Enter'){ ev.preventDefault(); nm.blur(); }
        });
        nm.addEventListener('click', function(ev){ ev.preventDefault(); ev.stopPropagation(); });
        nm.addEventListener('blur', function(){
          var v = nm.textContent.trim();
          if(!v || v===fn){ nm.textContent = fn; return; }
          if(D.functions.indexOf(v)>-1){ toast('There is already a function called ' + v + '.');
            nm.textContent = fn; return; }
          D.functions[D.functions.indexOf(fn)] = v;
          D.rows.forEach(function(r){ if(r.f===fn) r.f = v; });
          openState[v] = openState[fn];
          save(); render();
        });
      }
      s.appendChild(nm);
      s.appendChild(el('span','fn-count', frows.length + ' activities'));
      d.appendChild(s);

      d.appendChild(buildTable(fn, frows));
      d.appendChild(buildCards(frows));

      if(editing){
        var wrapAdd = el('div','addrow');
        var add = el('button','btn quiet','+ Add activity');
        add.type='button';
        add.addEventListener('click', function(){ addRow(fn); });
        wrapAdd.appendChild(add);
        d.appendChild(wrapAdd);
      }
      matrix.appendChild(d);
    });
  }
  var openState = {};

  function buildTable(fn, frows){
    var sc = el('div','scroller');
    var tb = el('table');
    var thead = el('thead'), htr = el('tr');
    htr.appendChild(el('th','act','Activity'));
    D.positions.forEach(function(p){
      var th = el('th', null, p.id);
      th.setAttribute('data-col', p.id);
      th.title = p.name + ', ' + p.title;
      htr.appendChild(th);
    });
    if(editing) htr.appendChild(el('th','tools',''));
    thead.appendChild(htr); tb.appendChild(thead);

    var body = el('tbody');
    frows.forEach(function(row){
      var idx = D.rows.indexOf(row);
      var tr = el('tr');
      tr.setAttribute('data-row', String(idx));
      if(editing && (!row.A.length || !row.R)) tr.className = 'flag';

      var act = el('td','act');
      var txt;
      if(!editing){
        txt = el('button','acttext actbtn', row.act);
        txt.type = 'button';
        txt.setAttribute('aria-label', row.act + '. Open the breakdown.');
        txt.addEventListener('click', function(){ openDrawer(row, txt); });
      } else {
        txt = el('span','acttext', row.act);
      }
      if(editing){
        txt.contentEditable = 'true';
        txt.addEventListener('blur', function(){
          var v = txt.textContent.replace(/\s+/g,' ').trim();
          row.act = v || 'Untitled activity';
          if(!v) txt.textContent = row.act;
          save();
        });
        txt.addEventListener('keydown', function(ev){
          if(ev.key==='Enter'){ ev.preventDefault(); txt.blur(); }
        });
      }
      act.appendChild(txt);

      if(editing){
        var msgs = [];
        if(!row.A.length) msgs.push('no one accountable');
        if(!row.R) msgs.push('no one doing the work');
        if(msgs.length) act.appendChild(el('span','rowmsg', msgs.join('; ')));
      }
      tr.appendChild(act);

      D.positions.forEach(function(p){
        var td = el('td');
        td.setAttribute('data-col', p.id);
        var L = letterOf(row, p.id);
        if(editing){
          var b = el('button','cellbtn'); b.type='button';
          b.setAttribute('aria-label', p.name + ' on ' + row.act +
            '. Click to change, shift-click to step back.');
          b.appendChild(mark(L, true));
          b.addEventListener('click', function(ev){
            var res = bump(row, p.id, ev.shiftKey);
            save();
            if(res.blocked){
              toast('R belongs to ' + label(res.blocked) + ' on this activity, so A/R and R '
                    + 'were skipped. Clear that cell first to move R.');
            } else if(res.moved.length){
              toast(res.moved.map(function(m){
                return m[0] + ' moved off ' + label(m[1]);
              }).join(', ') + '. Only one R per activity.');
            }
            render();
          });
          td.appendChild(b);
        } else if(L){
          td.appendChild(mark(L, false));
        }
        tr.appendChild(td);
      });

      if(editing) tr.appendChild(rowTools(row, fn));
      body.appendChild(tr);

    });
    tb.appendChild(body);
    sc.appendChild(tb);
    return sc;
  }

  function mark(L, editable){
    if(!L) return el('i','mk empty', editable ? '\u00b7' : '');
    var m = MK[L];
    return el('i','mk '+m[0], m[1]);
  }

  function rowTools(row, fn){
    var td = el('td','tools');
    var box = el('div','rowtools');

    var up = el('button','icb','\u25b2'); up.type='button';
    up.title='Move up'; up.setAttribute('aria-label','Move activity up');
    up.addEventListener('click', function(){ move(row, -1); });
    var dn = el('button','icb','\u25bc'); dn.type='button';
    dn.title='Move down'; dn.setAttribute('aria-label','Move activity down');
    dn.addEventListener('click', function(){ move(row, 1); });

    var sel = el('select','fnsel');
    sel.title = 'Move to another function';
    sel.setAttribute('aria-label','Function');
    D.functions.forEach(function(f){
      var o = el('option', null, f); o.value = f;
      if(f===fn) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', function(){
      row.f = sel.value;
      var i = D.rows.indexOf(row);
      D.rows.splice(i,1);
      var last = -1;
      for(var k=0;k<D.rows.length;k++) if(D.rows[k].f===row.f) last = k;
      D.rows.splice(last+1, 0, row);
      openState[row.f] = true;
      save(); render();
      toast('Moved to ' + row.f + '.');
    });

    var del = el('button','icb del','\u00d7'); del.type='button';
    del.title='Delete'; del.setAttribute('aria-label','Delete activity');
    del.addEventListener('click', function(){
      var at = D.rows.indexOf(row);
      if(at < 0) return;
      var gone = row.act;
      D.rows.splice(at, 1);
      save(); render();
      toast('Deleted \u201c' + gone + '\u201d.', 'Undo', function(){
        D.rows.splice(Math.min(at, D.rows.length), 0, row);
        save(); render();
      });
    });

    box.appendChild(up); box.appendChild(dn); box.appendChild(sel); box.appendChild(del);
    td.appendChild(box);
    return td;
  }

  function move(row, dir){
    var same = rowsOf(row.f);
    var at = same.indexOf(row);
    var swapWith = same[at + dir];
    if(!swapWith) return;
    var i = D.rows.indexOf(row), j = D.rows.indexOf(swapWith);
    D.rows[i] = swapWith; D.rows[j] = row;
    save(); render();
  }

  function addRow(fn){
    var row = {f:fn, act:'New activity', A:'', R:'', C:[], I:[], t:'',
               src:'Added on the page', n:'Added by hand. Not yet sourced.'};
    var last = -1;
    for(var k=0;k<D.rows.length;k++) if(D.rows[k].f===fn) last = k;
    D.rows.splice(last+1, 0, row);
    openState[fn] = true;
    save(); render();
    var trs = matrix.querySelectorAll('details.fn[data-fn="'+cssEsc(fn)+'"] tbody tr');
    for(var q=0;q<trs.length;q++){
      if(trs[q].getAttribute('data-row')===String(D.rows.indexOf(row))){
        var t = trs[q].querySelector('.acttext');
        if(t){ t.focus(); document.getSelection().selectAllChildren(t); }
        break;
      }
    }
  }
  function cssEsc(s){ return s.replace(/"/g,'\\"'); }

  function buildCards(frows){
    var c = el('div','cards');
    frows.forEach(function(row){
      var card = el('div','card');
      if(!editing){
        var cb = el('button','cardbtn', row.act);
        cb.type = 'button';
        cb.setAttribute('aria-label', row.act + '. Open the breakdown.');
        cb.addEventListener('click', function(){ openDrawer(row, cb); });
        card.appendChild(cb);
      } else {
        card.appendChild(el('strong', null, row.act));
      }
      var who = el('div','who');
      var wa = el('span'); wa.appendChild(mark(row.A.length?'A':'', false));
      wa.appendChild(document.createTextNode(row.A.length
        ? row.A.map(label).join(', ') : 'no owner'));
      var wr = el('span'); wr.appendChild(mark(row.R?'R':'', false));
      wr.appendChild(document.createTextNode(row.R ? label(row.R) : 'unassigned'));
      who.appendChild(wa); who.appendChild(wr);
      if(row.t){
        var wt = el('span');
        wt.appendChild(el('span','lbl','moves to'));
        wt.appendChild(document.createTextNode(label(row.t)));
        who.appendChild(wt);
      }
      card.appendChild(who);
      c.appendChild(card);
    });
    return c;
  }

  // ---- filter + dimming
  function applyFilter(){
    document.querySelectorAll('[data-col]').forEach(function(n){
      n.classList.toggle('col-dim', !!active && n.getAttribute('data-col')!==active);
    });
    document.querySelectorAll('#matrix tbody tr[data-row]').forEach(function(tr){
      var show = true;
      if(active){
        var i = parseInt(tr.getAttribute('data-row'),10);
        show = !!letterOf(D.rows[i], active);
      }
      tr.hidden = !show;
      var s = document.getElementById('src'+tr.getAttribute('data-row'));
      if(s && !show) s.hidden = true;
    });
    document.querySelectorAll('#matrix details.fn').forEach(function(d){
      var vis = d.querySelectorAll('tbody tr[data-row]:not([hidden])').length;
      var total = d.querySelectorAll('tbody tr[data-row]').length;
      d.hidden = !!active && vis===0;
      if(active && vis>0) d.open = true;
      d.querySelector('.fn-count').textContent =
        active ? vis + ' of ' + total + ' activities' : total + ' activities';
    });
    if(active){
      var p = pos(active);
      stateEl.textContent = 'Showing ' + p.name + ', ' + p.title;
    } else {
      stateEl.textContent = 'Showing all positions';
    }
  }

  function banner(){
    var pr = problems();
    bannerEl.textContent = '';
    bannerEl.classList.toggle('on', editing || dirty);
    if(!(editing || dirty)) return;
    var lead = el('span');
    if(editing){
      lead.appendChild(document.createTextNode('Editing. Click a cell to cycle through '));
      lead.appendChild(el('b', null, 'C, I, A, A/R, R'));
      lead.appendChild(document.createTextNode(' and back to blank. Shift-click steps back. '
        + 'An activity can have several A\u2019s; only R is single. '
        + 'Edits save in this browser only.'));
    } else {
      lead.appendChild(el('b', null, 'Edited copy.'));
      lead.appendChild(document.createTextNode(' You are seeing local changes, not the published version.'));
    }
    bannerEl.appendChild(lead);
    if(pr.miss) bannerEl.appendChild(el('span','warn', pr.miss +
      (pr.miss===1 ? ' activity is missing an A or an R' : ' activities are missing an A or an R')));
    if(pr.multi) bannerEl.appendChild(el('span', null, pr.multi +
      ' with more than one A'));
    if(pr.both) bannerEl.appendChild(el('span', null, pr.both +
      ' with the same person on A and R'));
    bannerEl.appendChild(el('span', null, D.rows.length + ' activities \u00b7 ' +
      D.functions.length + ' functions'));
  }

  function metaLine(){
    metaEl.textContent = '';
    metaEl.appendChild(el('span', null, D.rows.length + ' activities \u00b7 ' +
      D.functions.length + ' functions'));
    metaEl.appendChild(el('span', null, 'As of ' + D.asOf));
    metaEl.appendChild(el('span', null,
      'Reflects the 30 July leadership review and the 31 July role corrections'));
  }

  function render(){
    closeDrawer();
    document.body.classList.toggle('editing', editing);
    renderPositions(); renderMatrix(); metaLine(); banner(); applyFilter();
  }

  // ---- drawer: what the activity actually is
  var drawer   = document.getElementById('drawer');
  var scrim    = document.getElementById('scrim');
  var dBody    = document.getElementById('drawerBody');
  var dClose   = document.getElementById('drawerClose');
  var lastFocus = null;

  function whoLine(label, ids){
    if(!ids.length) return null;
    var row = el('div','who-row');
    row.appendChild(el('span','who-lbl', label));
    var names = el('span','who-names');
    ids.forEach(function(id, i){
      var p = pos(id);
      var chip = el('span','who-chip');
      chip.appendChild(el('b', null, p ? p.name : id));
      if(p) chip.appendChild(document.createTextNode(' ' + p.title));
      names.appendChild(chip);
    });
    row.appendChild(names);
    return row;
  }

  function openDrawer(row, trigger){
    lastFocus = trigger || null;
    dBody.textContent = '';

    dBody.appendChild(el('p','eyebrow', row.f));
    dBody.appendChild(el('h3', null, row.act));

    if(row.what){
      var s1 = el('section','d-sec');
      s1.appendChild(el('h4', null, 'What it is'));
      s1.appendChild(el('p', null, row.what));
      dBody.appendChild(s1);
    }
    if(row.eg){
      var s2 = el('section','d-sec');
      s2.appendChild(el('h4', null, 'For example'));
      s2.appendChild(el('p','eg', row.eg));
      dBody.appendChild(s2);
    }
    if(!row.what && !row.eg){
      var s0 = el('section','d-sec');
      s0.appendChild(el('p','muted',
        'No breakdown recorded for this activity yet. It was probably added on the page.'));
      dBody.appendChild(s0);
    }

    var s3 = el('section','d-sec');
    s3.appendChild(el('h4', null, 'Who'));
    var whoWrap = el('div','who-wrap');
    var lines = [
      whoLine('Accountable', row.A),
      whoLine('Responsible', row.R ? [row.R] : []),
      whoLine('Consulted', row.C),
      whoLine('Informed', row.I)
    ];
    lines.forEach(function(l){ if(l) whoWrap.appendChild(l); });
    if(!row.A.length || !row.R){
      whoWrap.appendChild(el('p','warn-line',
        (!row.A.length ? 'Nobody is accountable for this yet. ' : '') +
        (!row.R ? 'Nobody is doing the work yet.' : '')));
    }
    if(row.R && row.A.indexOf(row.R) > -1){
      whoWrap.appendChild(el('p','muted',
        'The same position answers for this and does it, so there is no second pair of eyes.'));
    }
    if(row.t){
      var p2 = pos(row.t);
      whoWrap.appendChild(el('p','muted',
        'Moves to ' + (p2 ? p2.title : row.t) + ' once that seat is filled.'));
    }
    s3.appendChild(whoWrap);
    dBody.appendChild(s3);

    if(row.n){
      var s4 = el('section','d-sec');
      s4.appendChild(el('h4', null, 'Why it sits here'));
      s4.appendChild(el('p', null, row.n));
      dBody.appendChild(s4);
    }
    if(row.src){
      var s5 = el('section','d-sec');
      s5.appendChild(el('h4', null, 'Source'));
      s5.appendChild(el('code', null, row.src));
      dBody.appendChild(s5);
    }

    drawer.hidden = false; scrim.hidden = false;
    document.body.classList.add('drawer-open');
    requestAnimationFrame(function(){
      drawer.classList.add('on'); scrim.classList.add('on');
      dClose.focus();
    });
  }

  function closeDrawer(){
    if(drawer.hidden) return;
    drawer.classList.remove('on'); scrim.classList.remove('on');
    document.body.classList.remove('drawer-open');
    setTimeout(function(){ drawer.hidden = true; scrim.hidden = true; }, 180);
    if(lastFocus && document.contains(lastFocus)) lastFocus.focus();
    lastFocus = null;
  }

  dClose.addEventListener('click', closeDrawer);
  scrim.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function(ev){
    if(ev.key === 'Escape' && !drawer.hidden){ ev.preventDefault(); closeDrawer(); }
  });
  // keep tab focus inside the panel while it is open
  drawer.addEventListener('keydown', function(ev){
    if(ev.key !== 'Tab') return;
    var f = drawer.querySelectorAll('button, [href], input, [tabindex]:not([tabindex="-1"])');
    if(!f.length) return;
    var first = f[0], last = f[f.length-1];
    if(ev.shiftKey && document.activeElement === first){ ev.preventDefault(); last.focus(); }
    else if(!ev.shiftKey && document.activeElement === last){ ev.preventDefault(); first.focus(); }
  });

  // ---- toast
  // The artifact frame is sandboxed without allow-modals, so confirm() and
  // prompt() are ignored by the browser. Anything that needed a modal is done
  // in-page instead, with an undo action on the toast.
  var toastTimer;
  function toast(msg, actionLabel, actionFn){
    toastEl.textContent = '';
    toastEl.appendChild(document.createTextNode(msg));
    if(actionLabel && actionFn){
      var a = el('button','toast-act', actionLabel);
      a.type = 'button';
      a.addEventListener('click', function(){
        toastEl.classList.remove('on');
        clearTimeout(toastTimer);
        actionFn();
      });
      toastEl.appendChild(a);
    }
    toastEl.classList.add('on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function(){ toastEl.classList.remove('on'); },
                            actionLabel ? 9000 : 3600);
  }

  // ---- export / import
  function payload(){
    return JSON.stringify({version: D.version, asOf: D.asOf,
      positions: D.positions, functions: D.functions, rows: D.rows}, null, 2);
  }
  function download(name, text){
    if(window.claude && window.claude.downloads){
      window.claude.downloads.save({filename:name, data:text}).then(function(){
        toast('Saved ' + name + '.');
      }, function(err){
        var code = err && err.code;
        if(code==='declined') return;
        if(code==='rate_limited'){ toast('A save prompt is already open. Try again in a moment.'); return; }
        fallback(name, text);
      });
      return;
    }
    fallback(name, text);
  }
  function fallback(name, text){
    try {
      var url = URL.createObjectURL(new Blob([text], {type:'application/json'}));
      var a = document.createElement('a');
      a.href = url; a.download = name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function(){ URL.revokeObjectURL(url); }, 4000);
    } catch(err){
      copy(text, 'Could not download. The JSON is on your clipboard instead.');
    }
  }
  function copy(text, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){ toast(msg); },
        function(){ toast('Could not copy. Use Export instead.'); });
    } else { toast('Copying is not available here. Use Export instead.'); }
  }
  function tsv(){
    var head = ['Function','Activity'].concat(D.positions.map(function(p){ return p.id; }))
      .concat(['Transitions to','Source','Notes']);
    var lines = [head.join('\t')];
    D.rows.forEach(function(r){
      var cells = [r.f, r.act];
      D.positions.forEach(function(p){
        var L = letterOf(r, p.id);
        cells.push(L==='T' ? '\u2192' : (L==='AR' ? 'A/R' : L));
      });
      cells.push(r.t ? label(r.t) : '', r.src, r.n);
      lines.push(cells.map(function(c){ return String(c).replace(/[\t\r\n]+/g,' '); }).join('\t'));
    });
    return lines.join('\n');
  }

  // ---- wiring
  stripEl.addEventListener('click', function(ev){
    var b = ev.target.closest('.pos'); if(!b) return;
    var id = b.getAttribute('data-pos');
    active = (active===id) ? null : id;
    stripEl.querySelectorAll('.pos').forEach(function(x){
      x.setAttribute('aria-pressed', x.getAttribute('data-pos')===active ? 'true':'false');
    });
    applyFilter();
  });


  var editBtn = document.getElementById('editBtn');
  editBtn.addEventListener('click', function(){
    editing = !editing;
    editBtn.setAttribute('aria-pressed', editing ? 'true':'false');
    editBtn.textContent = editing ? 'Done editing' : 'Edit';
    document.getElementById('editTools').hidden = !editing;
    if(!editing && !addFnBox.hidden){ addFnBox.hidden = true; addFnBtn.hidden = false; }
    render();
  });

  var addFnBtn = document.getElementById('addFn');
  var addFnBox = document.getElementById('addFnBox');
  var addFnInput = document.getElementById('addFnName');
  function commitFn(){
    var name = (addFnInput.value || '').replace(/\s+/g,' ').trim();
    if(!name){ closeFn(); return; }
    if(D.functions.indexOf(name)>-1){ toast('There is already a function called ' + name + '.'); return; }
    D.functions.push(name);
    openState[name] = true;
    addFnInput.value = '';
    addFnBox.hidden = true;
    addFnBtn.hidden = false;
    save(); render();
    addRow(name);
  }
  function closeFn(){
    addFnInput.value = '';
    addFnBox.hidden = true;
    addFnBtn.hidden = false;
    addFnBtn.focus();
  }
  addFnBtn.addEventListener('click', function(){
    addFnBtn.hidden = true;
    addFnBox.hidden = false;
    addFnInput.focus();
  });
  document.getElementById('addFnGo').addEventListener('click', commitFn);
  document.getElementById('addFnCancel').addEventListener('click', closeFn);
  addFnInput.addEventListener('keydown', function(ev){
    if(ev.key === 'Enter'){ ev.preventDefault(); commitFn(); }
    if(ev.key === 'Escape'){ ev.preventDefault(); closeFn(); }
  });

  document.getElementById('exportBtn').addEventListener('click', function(){
    download('AC-Brands-RACI.json', payload());
  });
  document.getElementById('copyBtn').addEventListener('click', function(){
    copy(tsv(), 'Copied as tab-separated text. Paste straight into Excel.');
  });
  var file = document.getElementById('importFile');
  document.getElementById('importBtn').addEventListener('click', function(){ file.click(); });
  file.addEventListener('change', function(){
    var f = file.files && file.files[0]; if(!f) return;
    var fr = new FileReader();
    fr.onload = function(){
      try {
        var d = JSON.parse(String(fr.result));
        if(!d || !Array.isArray(d.rows) || !Array.isArray(d.positions) ||
           !Array.isArray(d.functions)) throw new Error('shape');
        D = d; openState = {}; save(); render();
        toast('Loaded ' + d.rows.length + ' activities from ' + f.name + '.');
      } catch(err){
        toast('That file is not a RACI export.');
      }
      file.value = '';
    };
    fr.readAsText(f);
  });
  document.getElementById('revertBtn').addEventListener('click', function(){
    var snapshot = clone(D), wasDirty = dirty;
    try { localStorage.removeItem(KEY); } catch(err){}
    D = clone(PUB); dirty = false; openState = {};
    render();
    toast('Back to the published version. Your edits are gone unless you undo.',
      'Undo', function(){
        D = snapshot; dirty = wasDirty; openState = {};
        save(); render();
        toast('Your edits are back.');
      });
  });

  document.getElementById('expandAll').addEventListener('click', function(){
    D.functions.forEach(function(f){ openState[f] = true; });
    document.querySelectorAll('#matrix details.fn').forEach(function(d){ d.open = true; });
  });
  document.getElementById('collapseAll').addEventListener('click', function(){
    D.functions.forEach(function(f){ openState[f] = false; });
    document.querySelectorAll('#matrix details.fn').forEach(function(d){ d.open = false; });
  });

  window.addEventListener('beforeunload', function(ev){
    if(editing){ ev.preventDefault(); ev.returnValue = ''; }
  });

  render();
  if(dirty && !editing) toast('Showing your edited copy. Revert to see the published version.');
})();
"""

# ---------------------------------------------------------------- build
parts = []
parts.append("<style>\n"
             "@font-face{font-family:'Adrianna';src:url(data:font/ttf;base64,"
             + FONT_REG + ") format('truetype');font-weight:400;font-display:block}\n"
             "@font-face{font-family:'Adrianna';src:url(data:font/ttf;base64,"
             + FONT_DEMI + ") format('truetype');font-weight:600;font-display:block}\n"
             + CSS + "</style>")

parts.append('<div class="wrap">')

parts.append("""<header class="page">
<p class="eyebrow">AC Brands &middot; Operations &amp; Product Development</p>
<h1>Who owns what</h1>
<p class="lede">Accountability across every function, by position. Someone answers for each
activity and one person does the work. Everyone else is consulted or kept informed.</p>
<div class="meta" id="meta"></div>
</header>""")

parts.append("""<section class="block">
<h2>Positions</h2>
<p class="filter-note">Select a position to see only the activities it touches. Select again to clear.</p>
<div class="pos-strip" id="posStrip"></div>
</section>""")

parts.append("""<section class="block"><h2>The matrix</h2>
<div class="legend">
<span><i class="mk a">A</i> Answers for the outcome, and can be shared</span>
<span><i class="mk r">R</i> Does the work</span>
<span><i class="mk ar">A/R</i> Both, so no second pair of eyes</span>
<span><i class="mk c">C</i> Consulted</span>
<span><i class="mk i">I</i> Informed</span>
<span><i class="mk t">&rarr;</i> Moves here on hire</span>
</div>
<div class="toolbar">
<div class="btnrow">
<button class="btn" type="button" id="editBtn" aria-pressed="false">Edit</button>
<button class="btn" type="button" id="expandAll">Expand all</button>
<button class="btn" type="button" id="collapseAll">Collapse all</button>
</div>
<span class="filter-note" id="filterState">Showing all positions</span>
</div>
<p class="filter-note">Click any activity for what it is, a worked example, and where the assignment came from.</p>
<div class="btnrow" id="editTools" hidden>
<button class="btn quiet" type="button" id="addFn">+ Add function</button>
<span class="inline-form" id="addFnBox" hidden><label class="vh" for="addFnName">New function name</label>
<input type="text" id="addFnName" placeholder="New function name" autocomplete="off">
<button class="btn" type="button" id="addFnGo">Add</button>
<button class="btn quiet" type="button" id="addFnCancel">Cancel</button></span>
<button class="btn quiet" type="button" id="exportBtn">Export JSON</button>
<button class="btn quiet" type="button" id="copyBtn">Copy for Excel</button>
<button class="btn quiet" type="button" id="importBtn">Import JSON</button>
<button class="btn quiet" type="button" id="revertBtn">Revert to published</button>
<input type="file" id="importFile" accept=".json,application/json" hidden>
</div>
<div class="banner" id="banner"></div>
<div id="matrix"></div>
</section>""")

parts.append("""<footer class="page">
<p><strong>Editing.</strong> Press Edit, then click any cell to cycle it through C, I, A, A/R and R
and back to blank. Shift-click steps backwards if you overshoot. Activity names and function names become
editable, rows can be reordered, moved to another function, added or deleted.</p>
<p>An activity can have more than one A, so giving someone A takes nothing away from anyone else. R
is single, and the two states that claim it, A/R and R, sit at the end of the cycle. Clicking never
takes R off someone: if R is already held on that activity the cycle skips straight past both and
tells you who has it, so clearing their cell is the only way to move it. Open seats can only receive the transition arrow and partner organisations
cannot hold A, because a vacancy cannot be accountable and accountability does not leave the company.
An activity with no A at all, or nobody doing the work, is marked in the margin.</p>
<p><strong>Where edits live.</strong> In your own browser, on this device. They are not shared with
anyone else opening this link, and they survive a reload but not a cleared cache. Export JSON when a
change is worth keeping and send it back to Alvin to fold into the repository, which is what the
spreadsheet and this page are both generated from. Copy for Excel puts the whole matrix on your
clipboard as a table.</p>
<p><strong>How this was built.</strong> Every published row traces to a source: the operating
procedures and role definitions in the SJ-OS repository, the two specialist job descriptions, or the
30 July leadership review. Click an activity to see which, alongside a plain description of the work
and a worked example. Rows you add on the page carry no breakdown and are marked as added by hand
rather than sourced.</p>
<p><strong>Partner organisations</strong> hold the work but never the accountability. That stays with
an employee. Pedrero Regulatory is consulted rather than responsible because our procedures make
them consult-only, with no access to our systems.</p>
<p>Coverage is Sweet July Skin plus company-wide work. Sweet July, the lifestyle brand, is not
represented, because nothing in our operating documentation defines who owns it.</p>
<p>Questions or a row that looks wrong: Alvin.</p>
</footer>""")

parts.append('</div>')
parts.append('<div class="scrim" id="scrim" hidden></div>')
parts.append('<aside class="drawer" id="drawer" hidden role="dialog" aria-modal="true" aria-label="Activity breakdown">'
             '<button class="drawer-close" id="drawerClose" type="button" aria-label="Close the breakdown">Close</button>'
             '<div class="drawer-body" id="drawerBody"></div></aside>')
parts.append('<div class="toast" id="toast" role="status" aria-live="polite"></div>')
parts.append('<script>window.__RACI__=' + json.dumps(PUB) + ';</script>')
parts.append('<script>' + JS + '</script>')

io.open(OUT, "w", encoding="utf-8").write(
    "<title>AC Brands: Who owns what</title>\n" + "\n".join(parts))
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
