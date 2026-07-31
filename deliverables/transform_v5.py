"""v4 -> v5: real Marketing, Retail & Wholesale, and Web activities.

Alvin, 2026-07-31: the matrix was only as complete as the skill suite, and there are
no skills for marketing, wholesale or web. The AC Brands landing hub is the source for
those - `data/links.json` in the acb-thelanding repo defines eleven functions with an
explicit `lead` field per function, three of which read "Owned by TBD".

Decisions taken on those:
- Marketing: Soraya accountable. WITHIN responsible for paid media, Kate for social
  content. Danielle keeps campaign direction and consults throughout.
- Channels: Nicole accountable for ALL channels - DTC, Amazon and wholesale - with
  Alvin consulted and Danielle informed. Broader than the hub, which split DTC/Amazon
  to Alvin and left wholesale TBD.
- Web: Danielle accountable. Nicole is the systems and tech owner. Teknologics
  responsible for development. Erin and Ivy on visual design, Soraya consulted on
  content, Alvin informed.

Two new partner organisations: WITHIN (digital marketing) and Teknologics (web dev).
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raci_rows_v4 as v4

S = ".claude/skills/"
HUB = "acb-thelanding: data/links.json"
ALVIN = "Alvin, 2026-07-31 (marketing, wholesale and web)"

POSITIONS = list(v4.POSITIONS) + [
    ("WI", "WITHIN", "Digital marketing agency", "partner"),
    ("TK", "Teknologics", "Web development", "partner"),
]

def upd(row, A=None, R=None, addC=(), addI=(), dropI=(), note=None, src=None,
        clear_inferred=False):
    f, act, a, r, c, i, t, s, n = row
    a = A or a
    r = R or r
    c = list(c) + [k for k in addC if k not in c]
    i = [k for k in i if k not in dropI] + [k for k in addI if k not in i]
    c = [k for k in c if k not in (a, r)]
    i = [k for k in i if k not in (a, r) and k not in c]
    if clear_inferred:
        n = n.split("INFERRED")[0].rstrip(" .-")
        if n and not n.endswith("."):
            n += "."
    if note:
        n = f"{n} {note}".strip()
    if src:
        s = f"{s}; {src}".lstrip("; ")
    return (f, act, a, r, c, i, t, s, n)

# ---- Nicole takes accountability for every channel ----
EDITS = {
 "Shopify revenue and channel position read": dict(
   A="NI", R="AB", addC=("SS",), addI=("DI",), clear_inferred=True,
   note="Nicole is accountable for all channels - DTC, Amazon and wholesale - with Alvin "
        "consulted and Danielle informed. This was the last row on the matrix with no owner; "
        "it now has one.",
   src=f"{HUB}; {ALVIN}"),

 "Channel operations and promo setup across DTC, UBM and Amazon": dict(
   A="NI", addC=("AB",), addI=("DI",),
   note="Part of Nicole's all-channel accountability.", src=f"{HUB}; {ALVIN}"),

 "Retail channel launch programs": dict(
   A="NI", R="AB", addC=("SS",), addI=("DI",),
   note="Hub lists wholesale as \"Owned by TBD\" (links.json, Sales & Commerce lead). Resolved to "
        "Nicole as part of all-channel accountability.",
   src=f"{HUB}; {ALVIN}"),

 "Retailer and reseller first contact": dict(
   addI=("DI",), note="Consistent with Nicole's all-channel accountability.", src=HUB),

 # Hub records the function lead for Brand & Creative
 "Brand guideline custody": dict(
   note="Hub lists Brand & Creative as \"Owned by Soraya\" as function lead; custody "
        "accountability sits with the President per the 31 July correction. Both hold: Soraya "
        "runs the function, Danielle answers for the brand standard.",
   src=HUB),
}

rows = []
for row in v4.ROWS:
    act = row[1]
    for k, v in EDITS.items():
        if act.startswith(k):
            row = upd(row, **v)
            break
    rows.append(row)
for k in EDITS:
    assert any(r[1].startswith(k) for r in rows), f"edit target missing: {k}"

# ---------------------------------------------------------------- new rows
NEW = [
# ============ Marketing & Brand — Soraya accountable ============
("Marketing & Brand", "Editorial and content calendar",
 "SS", "KL", ["EH", "NI", "DI"], ["AB", "AC"], "",
 f"{HUB} (Marketing / Owned Channels); {ALVIN}",
 "Hub lists Marketing as \"Owned by TBD\"; resolved to Soraya as Marketing Manager. Editorial "
 "Calendar is a named tool under Owned Channels."),

("Marketing & Brand", "Email marketing: Klaviyo flows and campaign sends",
 "SS", "WI", ["KL", "NI", "DI"], ["AB", "AC"], "",
 f"{HUB} (Marketing / Klaviyo Performance); {ALVIN}",
 "WITHIN runs most of our digital marketing including email execution. Soraya answers for the "
 "channel. Klaviyo Performance is a named tool on the hub."),

("Marketing & Brand", "Paid media: Meta, Google and channel spend",
 "SS", "WI", ["AB", "NI", "DI"], ["AC"], "",
 f"{HUB} (Marketing / Paid Media Dashboard); {ALVIN}",
 "WITHIN is the digital marketing agency and runs paid execution. Alvin consulted on spend "
 "against margin floors. Quarterly business reviews with WITHIN - the most recent was 20 July."),

("Marketing & Brand", "Social media content and publishing",
 "SS", "KL", ["EH", "IT", "DI"], ["AC"], "",
 f"{HUB} (Marketing / Social Media Dashboard); {ALVIN}",
 "Distinct from social listening, which Kate is accountable for. Here she does the publishing "
 "work and Soraya answers for the channel."),

("Marketing & Brand", "Influencer and earned media programs",
 "SS", "KL", ["DI", "NI"], ["AB", "AC"], "",
 f"{HUB}; {ALVIN}",
 "Brand-facing and founder-adjacent, so Danielle consulted and Ayesha informed. The physical "
 "seeding logistics sit on the Operations special-projects row."),

("Marketing & Brand", "WITHIN agency relationship and quarterly business reviews",
 "SS", "SS", ["AB", "NI", "DI"], ["AC"], "",
 ALVIN,
 "A and R both Soraya. WITHIN holds most of our digital marketing execution, so the engagement "
 "is a single point of dependency - same shape as the other five external parties."),

# ============ Retail & Wholesale — Nicole accountable ============
("Retail & Wholesale", "Wholesale pipeline and new retail partner development",
 "NI", "NI", ["AB", "SS"], ["DI", "AC"], "",
 f"{HUB} (Sales & Commerce lead: \"TBD (wholesale)\"); {ALVIN}",
 "Hub left wholesale unowned. Resolved to Nicole with all-channel accountability. A and R both "
 "Nicole - no second pair of eyes on new-partner decisions."),

("Retail & Wholesale", "Retail price architecture and the pricing matrix",
 "NI", "AB", ["DI", "SS", "PC"], ["AC"], "",
 f"{HUB} (Sales & Commerce / Retail Price Architecture, SJS Pricing Matrix); {ALVIN}",
 "Live pricing matrix on the hub carries retail, wholesale and subscription prices with margin "
 "colouring. Ties to the margin framework, so Danielle consulted as the walk-away approver."),

("Retail & Wholesale", "Retailer promo calendar (Sephora, Ulta) and promo planning",
 "NI", "SS", ["AB", "KL"], ["DI", "AC"], "",
 f"{HUB} (Market Intelligence / Promo Landscape); {ALVIN}",
 "Promo Landscape tracks the Sephora and Ulta promo calendar. Marketing runs the planning; "
 "Nicole answers for the channel commitment."),

("Ecommerce & DTC", "Amazon channel management (FBA, AWD, Seller Central)",
 "NI", "AB", ["SS"], ["DI", "AC"], "OPS",
 f"{HUB} (Sales & Commerce / Amazon Dashboard); {ALVIN}",
 "Hub gave Amazon to Alvin; resolved to Nicole under all-channel accountability with Alvin doing "
 "the work. Inventory and inbound pipeline transition to the Ops Specialist."),

("Ecommerce & DTC", "Product detail page content and product copy",
 "SS", "SS", ["NI", "PC", "EH", "IT"], ["AB", "DI"], "",
 f"{HUB} (Sales & Commerce / SJS Product Copy Database); {ALVIN}",
 "Product Copy Database is live from PLM and carries every claim, ingredient line, FAQ and Amazon "
 "title across DTC, Amazon and wholesale. Perrine and Regulatory consulted because claims on a "
 "PDP are claims. A and R both Soraya."),

# ============ IT / Systems & Data — web ============
("IT / Systems & Data", "Website platform, Shopify storefront and web releases",
 "DI", "TK", ["NI", "SS", "EH", "IT"], ["AB"], "",
 ALVIN,
 "Teknologics is the web development partner. Danielle accountable; Nicole is the systems and "
 "tech owner; Erin and Ivy on visual design; Soraya consulted on merchandising and content; "
 "Alvin informed."),

("IT / Systems & Data", "Web and digital systems ownership, including the Teknologics engagement",
 "DI", "NI", ["TK", "AB", "SS"], ["AC"], "",
 ALVIN,
 "Nicole is the systems and tech owner for the web and digital stack. Scoped here to web and "
 "digital rather than the whole IT function - the PLM, Asana, hub-publish and Routine rows still "
 "sit with Alvin. Confirm whether that should widen."),
]
rows.extend(NEW)

# ---------------------------------------------------------------- emit
FUNC_ORDER = []
for r in v4.ROWS:
    if r[0] not in FUNC_ORDER:
        FUNC_ORDER.append(r[0])

out = io.open("raci_rows.py", "w", encoding="utf-8")
out.write('''"""RACI rows for AC Brands. v5 — the whole business, not just what has a skill.

Tuple: (Function, Activity, A, R, [C...], [I...], Transition, Source, Notes)
  A = answers for the outcome. R = does the work. One of each per row.
  Transition = "" | "OPS" | "PDS" — the incoming seat that absorbs R on hire.
  Open seats never hold A or R; a vacancy cannot be accountable.
  Partner organisations can hold R — they do the work — but never A.

Sources are the SJ-OS repo (paths relative to /home/user/SJ-OS), the AC Brands
landing hub (paths relative to /home/user/acb-thelanding, prefixed "acb-thelanding:"),
the 2026-07-30 leadership review, the 2026-07-27 email to Danielle, the two specialist
job descriptions, and Alvin's corrections of 2026-07-31.

v5 adds real Marketing, Retail & Wholesale and Web activities that have no skill
behind them, sourced from the hub's function definitions. Nicole takes accountability
for all channels; Soraya for Marketing; Danielle for web. WITHIN and Teknologics join
as partner organisations. Nothing on the matrix is unowned any more.
"""

''')
out.write("POSITIONS = [\n")
for p in POSITIONS:
    out.write(f"  {p!r},\n")
out.write("]\n\nROWS = [\n")
lastf = None
for r in sorted(rows, key=lambda r: FUNC_ORDER.index(r[0])):
    if r[0] != lastf:
        out.write(f"\n# ==== {r[0]} ====\n")
        lastf = r[0]
    out.write(f"  {r!r},\n")
out.write("]\n")
out.close()
print(f"v5 rows: {len(rows)} (v4 was {len(v4.ROWS)}, +{len(NEW)} new)")
print(f"positions: {len(POSITIONS)}")
