"""v3 -> v4: add the three external partner organisations.

Alvin, 2026-07-31:
- Pedrero Regulatory — external regulatory partner, contractors, "a big piece of this."
  Already documented in the repo as consult-only with no internal authority, but
  Amy Pedrero holds the binding regulatory calls. Added as C across Regulatory and
  on the Quality rows where classification is reportable.
- Ironclad Finance (Dan Bender) — manages the finance function. Split accountability:
  Danielle on reporting, Alvin on cost. Ironclad responsible throughout.
- Calm HR — PEO and co-employer, handles most HR with Alvin as liaison. Alvin
  accountable throughout, Danielle co-approves, Calm HR responsible.

Two of the three previously unowned functions now have owners. Finance and People &
Admin stop being gaps.
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raci_rows_v3 as v3

S = ".claude/skills/"
ALVIN = "Alvin, 2026-07-31 (external partners)"
PED = f"{S}regulatory-manager/references/pedrero-contacts.md:9,13,21"

POSITIONS = list(v3.POSITIONS) + [
    ("PR", "Pedrero Regulatory", "External regulatory partner", "partner"),
    ("IF", "Ironclad Finance", "Outsourced finance (Dan Bender)", "partner"),
    ("CH", "Calm HR", "PEO and co-employer", "partner"),
]

def upd(row, A=None, R=None, addC=(), addI=(), note=None, src=None, clear_inferred=False):
    f, act, a, r, c, i, t, s, n = row
    a = A or a
    r = R or r
    c = list(c) + [k for k in addC if k not in c]
    i = list(i) + [k for k in addI if k not in i]
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

# ---- Pedrero: consulted wherever substantive regulatory review happens ----
PEDRERO_C = [
 "Pre-launch ingredient list review gate",
 "Pedrero engagement and send approval",
 "Claim substantiation and new-claim defensibility",
 "Label artwork archive, IL cross-check and label-law checks",
 "Reformulation claim bridge",
 "Retailer attestation responses",
 "MoCRA registrations, state filings and Leaping Bunny renewal",
 "SAE and recall agency filings",
 "Regulatory fan-out routing and the regulatory dashboard publish",
 "Serious adverse event triage and recall kickoff",
]
PED_NOTE = ("Pedrero Regulatory holds the binding external review; consult-only internally, with no "
            "Asana access and no internal authority, so the Reg Lead gate stays in-house.")

# ---- targeted edits ----
EDITS = {
 "Accounts payable, bookkeeping and payroll": dict(
   A="AB", R="IF", addC=("DI",), clear_inferred=True,
   note="Ironclad Finance runs AP, bookkeeping and payroll; Dan Bender is the contact. Cost-side "
        "accountability sits with Operations because the vendor-invoice pipeline and its five "
        "approval gates feed it. No longer an unowned function.",
   src=ALVIN),

 "Employee onboarding, offboarding and access deprovisioning": dict(
   A="AB", R="CH", addC=("DI", "NI"), clear_inferred=True,
   note="Calm HR is the PEO and co-employer and runs the process; Alvin is the liaison and answers "
        "for it. Danielle consulted. No longer an unowned function - the departed-role-holder "
        "checklist in the PD role-map remains the internal system-side counterpart.",
   src=ALVIN),

 "Monthly and quarterly vendor cost rollups": dict(
   addC=("IF",),
   note="Ironclad consulted - the rollup feeds their books.", src=ALVIN),

 "Hiring the Operations Specialist and the PD Project Manager Specialist": dict(
   addC=("CH",),
   note="Calm HR runs the recruiting process once the RACI clears Danielle.", src=ALVIN),

 "Vendor invoice classification and cost capture": dict(
   addC=("IF",),
   note="Ironclad consulted - classified invoices land in their ledger.", src=ALVIN),
}

rows = []
for row in v3.ROWS:
    act = row[1]
    e = None
    for k, v in EDITS.items():
        if act.startswith(k):
            e = v
            break
    if e:
        row = upd(row, **e)
    if any(act.startswith(k) for k in PEDRERO_C):
        row = upd(row, addC=("PR",), note=PED_NOTE, src=PED)
    rows.append(row)

for k in EDITS:
    assert any(r[1].startswith(k) for r in rows), f"edit target missing: {k}"
for k in PEDRERO_C:
    assert any(r[1].startswith(k) for r in rows), f"pedrero target missing: {k}"

# ---------------------------------------------------------------- new rows
NEW = [
# ---- Finance: Danielle on reporting, Alvin on cost, Ironclad responsible ----
("Finance", "Month-end close and management reporting",
 "DI", "IF", ["AB", "NI"], ["AC"], "",
 ALVIN,
 "Ironclad Finance closes the books and produces the reporting; Dan Bender is the contact. "
 "Reporting accountability sits with the President."),

("Finance", "Annual budget and forecast consolidation",
 "DI", "IF", ["AB", "NI", "SS"], ["AC"], "",
 ALVIN,
 "President answers for the budget. Operations and Consumer Strategy feed the operating and "
 "channel assumptions."),

("Finance", "Inventory valuation and cost of goods",
 "AB", "IF", ["NI", "PC"], ["DI"], "",
 f"{ALVIN}; {S}inventory-manager/SKILL.md:18",
 "Cost side, so accountability sits with Operations - it flows out of purchasing, receiving and "
 "the inventory ledger. Ironclad carries it into the books."),

# ---- People & Admin: Alvin accountable throughout, Danielle co-approves ----
("People & Admin", "Employee handbook and HR policy",
 "AB", "CH", ["DI"], ["NI", "AC"], "",
 ALVIN,
 "Calm HR drafts and maintains; Alvin is the liaison and answers for it; Danielle co-approves. "
 "Handbook is in flight as of 2026-07-30 and goes to legal review before implementation."),

("People & Admin", "Benefits administration and payroll processing",
 "AB", "CH", ["DI", "IF"], [], "",
 ALVIN,
 "Calm HR administers as co-employer. Ironclad consulted where payroll hits the books."),

("People & Admin", "Employment compliance and separations",
 "AB", "CH", ["DI"], [], "",
 ALVIN,
 "Calm HR runs the process with outside counsel where needed. Danielle co-approves every "
 "separation."),

# ---- Regulatory: the partner relationship itself ----
("Regulatory & Compliance", "Pedrero engagement letter, scope and renewal",
 "AB", "AB", ["PR", "DI"], ["NI"], "",
 f"{S}regulatory-manager/references/pedrero-contacts.md:50; {ALVIN}",
 "The engagement letter governs scope, retainer, response windows and dispute resolution. Annual "
 "renewal. A and R both AB - the only person managing the regulatory partner relationship."),
]
rows.extend(NEW)

# ---------------------------------------------------------------- emit
out = io.open("raci_rows.py", "w", encoding="utf-8")
out.write('''"""RACI rows for AC Brands. v4 — position-first, external partners included.

Tuple: (Function, Activity, A, R, [C...], [I...], Transition, Source, Notes)
  A = answers for the outcome. R = does the work. One of each per row.
  Transition = "" | "OPS" | "PDS" — the incoming seat that absorbs R on hire.
  Open seats never hold A or R; a vacancy cannot be accountable.
  Partner organisations can hold R — they do the work — but never A, which stays
  in-house.

v2 applied the 2026-07-30 leadership review. v3 added Erin's packaging authority and
Danielle's and Ayesha's brand roles. v4 adds the three external partners: Pedrero
Regulatory, Ironclad Finance (Dan Bender) and Calm HR. Finance and People & Admin
stop being unowned functions as a result.
"""

''')
out.write("POSITIONS = [\n")
for p in POSITIONS:
    out.write(f"  {p!r},\n")
out.write("]\n\nROWS = [\n")
# keep v3's function order, so new rows land inside their existing section
FUNC_ORDER = []
for r in v3.ROWS:
    if r[0] not in FUNC_ORDER:
        FUNC_ORDER.append(r[0])
lastf = None
for r in sorted(rows, key=lambda r: FUNC_ORDER.index(r[0])):
    if r[0] != lastf:
        out.write(f"\n# ==== {r[0]} ====\n")
        lastf = r[0]
    out.write(f"  {r!r},\n")
out.write("]\n")
out.close()
print(f"v4 rows: {len(rows)} (v3 was {len(v3.ROWS)}, +{len(NEW)} new)")
print(f"positions: {len(POSITIONS)}")
