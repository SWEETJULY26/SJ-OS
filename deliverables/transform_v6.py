"""v5 -> v6.

Alvin, 2026-07-31:
1. Coastal Interactive is the managed service provider for higher-level IT and
   systems - back-end infrastructure, equipment onboarding. Alvin is the liaison.
2. Perrine should never be blank on a Product Development row. Her accountability
   is unchanged (he retracted the suggestion of dropping her A's); where she had
   no letter at all on a PD row she becomes Informed.
3. Soraya was on none of the eight PD rows. She should be Informed at minimum, so
   she picks up I wherever she was blank - marketing needs the PD signal.
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raci_rows_v5 as v5

ALVIN = "Alvin, 2026-07-31 (Coastal Interactive; PD visibility)"

POSITIONS = list(v5.POSITIONS) + [
    ("CI", "Coastal Interactive", "Managed IT service provider", "partner"),
]

def add_informed(row, who):
    """Give `who` an I on this row only if they currently hold no letter at all."""
    f, act, a, r, c, i, t, s, n = row
    if who in (a, r) or who in c or who in i:
        return row, False
    return (f, act, a, r, list(c), list(i) + [who], t, s, n), True

rows = []
pd_pc = pd_ss = 0
for row in v5.ROWS:
    if row[0] == "Product Development":
        row, ch = add_informed(row, "PC")
        pd_pc += ch
        row, ch = add_informed(row, "SS")
        pd_ss += ch
        if ch or True:
            f, act, a, r, c, i, t, s, n = row
            extra = ("Perrine and Soraya are never blank on a PD row - PD technical guidance and the "
                     "marketing read both need visibility on every product decision.")
            if extra not in n:
                n = f"{n} {extra}"
            row = (f, act, a, r, c, i, t, f"{s}; {ALVIN}", n)
    rows.append(row)

# ---- Coastal Interactive consulted where IT and onboarding overlap ----
CI_CONSULT = {
 "Asana project, section, custom-field and connector configuration":
   "Coastal Interactive consulted on identity, access and integration plumbing behind the "
   "connectors.",
 "Employee onboarding, offboarding and access deprovisioning":
   "Two partners split this: Calm HR runs the employment side, Coastal Interactive runs equipment "
   "and account provisioning. Alvin is the liaison to both and answers for the whole.",
}
out = []
for row in rows:
    hit = next((k for k in CI_CONSULT if row[1].startswith(k)), None)
    if hit:
        f, act, a, r, c, i, t, s, n = row
        if "CI" not in c and "CI" not in i and "CI" not in (a, r):
            c = list(c) + ["CI"]
        i = [k for k in i if k != "CI"]
        row = (f, act, a, r, c, i, t, f"{s}; {ALVIN}", f"{n} {CI_CONSULT[hit]}")
    out.append(row)
rows = out
for k in CI_CONSULT:
    assert any(r[1].startswith(k) for r in rows), f"CI consult target missing: {k}"

# ---------------------------------------------------------------- new rows
NEW = [
("IT / Systems & Data",
 "Back-end IT infrastructure, identity and endpoint management",
 "AB", "CI", ["NI"], ["DI"], "",
 ALVIN,
 "Coastal Interactive is the managed service provider and handles the higher-level IT and systems "
 "work. Alvin is the liaison and answers for it. Distinct from the web and digital stack, which "
 "sits with Danielle and Nicole."),

("IT / Systems & Data",
 "Equipment procurement, onboarding and asset lifecycle",
 "AB", "CI", ["NI", "CH"], ["DI"], "OPS",
 ALVIN,
 "Coastal Interactive provisions and recovers equipment. Pairs with the Calm HR employment side on "
 "every start and every exit - the departed-role-holder checklist covers the systems half. "
 "Transitions to the Operations Specialist on hire."),

("IT / Systems & Data",
 "Coastal Interactive managed-service engagement and escalation",
 "AB", "AB", ["CI", "NI", "DI"], [], "",
 ALVIN,
 "A and R both Alvin - he is the sole liaison to the IT managed-service partner. Same single-point "
 "shape as the other partner relationships."),
]
rows.extend(NEW)

# ---------------------------------------------------------------- emit
FUNC_ORDER = []
for r in v5.ROWS:
    if r[0] not in FUNC_ORDER:
        FUNC_ORDER.append(r[0])

o = io.open("raci_rows.py", "w", encoding="utf-8")
o.write('''"""RACI rows for AC Brands. v6 — the whole business, including managed IT.

Tuple: (Function, Activity, A, R, [C...], [I...], Transition, Source, Notes)
  A = answers for the outcome. R = does the work. One of each per row.
  Transition = "" | "OPS" | "PDS" — the incoming seat that absorbs R on hire.
  Open seats never hold A or R; a vacancy cannot be accountable.
  Partner organisations can hold R — they do the work — but never A.

Sources are the SJ-OS repo (paths relative to /home/user/SJ-OS), the AC Brands
landing hub (relative to /home/user/acb-thelanding, prefixed "acb-thelanding:"),
the 2026-07-30 leadership review, the 2026-07-27 email to Danielle, the two
specialist job descriptions, and Alvin's corrections of 2026-07-31.

v6 adds Coastal Interactive as the managed IT service partner, and guarantees that
Perrine and Soraya are never blank on a Product Development row — PD technical
guidance and the marketing read both need visibility on every product decision.
"""

''')
o.write("POSITIONS = [\n")
for p in POSITIONS:
    o.write(f"  {p!r},\n")
o.write("]\n\nROWS = [\n")
lastf = None
for r in sorted(rows, key=lambda r: FUNC_ORDER.index(r[0])):
    if r[0] != lastf:
        o.write(f"\n# ==== {r[0]} ====\n")
        lastf = r[0]
    o.write(f"  {r!r},\n")
o.write("]\n")
o.close()
print(f"v6 rows: {len(rows)} (v5 was {len(v5.ROWS)}, +{len(NEW)} new)")
print(f"PD rows where Perrine gained I: {pd_pc}")
print(f"PD rows where Soraya gained I: {pd_ss}")
print(f"positions: {len(POSITIONS)}")
