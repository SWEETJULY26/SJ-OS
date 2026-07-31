"""Transform v1 rows into v2: position-first, new quality gates, two open seats.

v1 tuple: (Function, Activity, A, R, [C], [I], Source, Notes)
v2 tuple: (Function, Activity, A, R, [C], [I], Transition, Source, Notes)

Transition is "" | "OPS" | "PDS" — which incoming seat absorbs the R.
Open seats never hold A or R; a vacancy cannot be accountable.
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_rows_v1 import ROWS as V1

S = ".claude/skills/"
MTG = "Leadership Business Review 2026-07-30"
EMAIL = "Email to Danielle 2026-07-27 'Proposed Ops Positions'"
JD_OPS = "SharePoint: Sweet July Skin - Operations Specialist - Job Description.docx"
JD_PD = "SharePoint: Sweet July Skin - Product Development Specialist - Job Description.docx"

# ---- A/R reassignments, keyed by an unambiguous substring of the activity ----
# (new_A, new_R, add_C, drop_C, note_suffix)
REASSIGN = {
    # Quality: process-shaped gates move to Nicole; Perrine becomes consult.
    "Customer complaint intake": ("NI", "AB", ["PC"], [],
        f"Gate moved to Nicole as the final quality check per {MTG} 25:18-26:01."),
    "Complaint trend analysis": ("NI", "AB", ["PC"], [],
        f"Nicole already held this gate; monthly trend review formalizes it per {MTG} 26:02-26:17."),
    "NCR and CAPA lifecycle": ("NI", "AB", ["PC"], [],
        f"A moved from Perrine to Nicole per {MTG} 25:18-25:50. Perrine consults on technical root cause."),
    "Lab finding intake": ("NI", "AB", ["PC"], [],
        f"Gate moved to Nicole per {MTG} 25:35-25:50. Perrine consults on the technical call."),
    "Vendor quality flag": ("NI", "AB", ["PC"], [],
        f"A moved from Perrine to Nicole per {MTG} 25:18-25:50. Perrine consults."),
    "Batch hold and release": ("NI", "AB", ["PC"], [],
        f"A moved from Perrine to Nicole per {MTG} 25:35-26:01. Perrine consults on the technical basis."),
    "Cross-cutting quality tasks": ("NI", "AB", ["PC"], [],
        f"Gate moved to Nicole per {MTG} 25:18-25:50."),
    "Quality-of-supply threshold": ("NI", "AB", ["PC"], [],
        f"Gate moved to Nicole per {MTG} 26:02-26:17."),
    "Quality dashboard publish": ("NI", "AB", ["PC"], [],
        f"Nicole gates the content; Alvin retains the publish mechanics. Per {MTG} 26:02-26:17."),
    # Framework rows stay with Alvin, Nicole added as consult.
    "SOP ratification, annual review": ("AB", "AB", ["NI"], [],
        "Framework sits with the VP of Operations. Nicole consults on documentation quality. "
        "The QA Manager seat SOP §7 calls for is now covered internally by Nicole rather than vacant."),
    "Serious adverse event triage": ("AB", "AB", ["NI"], [],
        "Stays with Alvin as Reg Lead — legal and agency exposure. Nicole consults."),
}

# Split the merged stability row: technical call is Perrine's, disposition is Nicole's.
SPLIT_STABILITY = "In-market stability scheduling and near-expiry decisions"

# ---- Which incoming seat absorbs the R on each existing row ----
TRANSITION = {
    "OPS": [
        "Vendor master data, onboarding",
        "Purchase order lifecycle",
        "Three-way reconciliation",
        "Vendor invoice classification",
        "Inventory position keeping",
        "Adjustments, write-offs and return dispositions",
        "S&OP: forecast, inventory targets",
        "Inbound freight, customs, duty and carrier claims",
        "Daily DTC order operations",
        "Pre-ship out-of-stock holds",
        "Retailer ASN / EDI 856",
        "Daily DTC fulfillment KPIs",
    ],
    "PDS": [
        "Customer complaint intake",
        "Complaint trend analysis",
        "NCR and CAPA lifecycle",
        "Lab finding intake",
        "Vendor quality flag",
        "Batch hold and release",
        "Quality dashboard publish",
        "Pre-launch ingredient list review gate",
        "Claim substantiation",
        "Retailer attestation responses",
        "MoCRA registrations, state filings",
        "PD signal intake from meetings",
        "Formula stage-gate progression",
    ],
}

def find(needle, rows):
    hits = [i for i, r in enumerate(rows) if needle.lower() in r[1].lower()]
    assert len(hits) == 1, f"{needle!r} matched {len(hits)} rows"
    return hits[0]

v2 = []
for func, act, A, R, C, I, src, notes in V1:
    C, I = list(C), list(I)
    if act == SPLIT_STABILITY:
        # technical testing decision -> Perrine A; disposition -> Nicole A
        v2.append((func, "In-market stability testing decisions (PET, accelerated, real-time)",
                   "PC", "AB", ["NI"], [], "PDS",
                   src, "Technical testing call stays with Perrine as the R&D and quality technical "
                        f"advisor. Operator approves schedule edits. Per {MTG} 25:18-25:35 the process "
                        "gate moved to Nicole but the technical judgment did not."))
        v2.append((func, "Near-expiry batch disposition at the 30-day threshold",
                   "NI", "AB", ["PC"], [], "PDS",
                   src, "Disposition is a quality gate, so it moves to Nicole. Posts back to inventory "
                        "before any write-off."))
        continue
    matched = None
    for needle, (nA, nR, addC, dropC, suffix) in REASSIGN.items():
        if needle.lower() in act.lower():
            matched = (nA, nR, addC, dropC, suffix)
            break
    if matched:
        nA, nR, addC, dropC, suffix = matched
        A, R = nA, nR
        for k in addC:
            if k not in C and k != A and k != R:
                C.append(k)
        C = [k for k in C if k not in dropC and k != A and k != R]
        I = [k for k in I if k != A and k != R and k not in C]
        notes = f"{notes} {suffix}"
    trans = ""
    for seat, needles in TRANSITION.items():
        if any(n.lower() in act.lower() for n in needles):
            trans = seat
            break
    v2.append((func, act, A, R, C, I, trans, src, notes))

# ---------------------------------------------------------------- new rows
NEW = [
("Quality",
 "Final quality check on product and documentation across every function",
 "NI", "NI", ["AB", "PC", "SS", "EH"], ["DI", "AC"], "",
 f"{MTG} 25:35-26:01",
 "The new cross-function gate. Verbatim: \"anything related to quality of service or quality of "
 "product will go through Nicole's eyes as sort of that final quality check... Even with each "
 "function having or being the primary owner, we'll still have that quality gate.\" A and R both NI."),

("Quality",
 "Quality management system framework and monthly quality-trend review",
 "AB", "NI", ["PC"], ["DI"], "",
 f"{MTG} 25:18-26:17",
 "Alvin owns the overall framework; Nicole runs it. Monthly trend review so recurring issues "
 "(the pump issue was the worked example) can drive packaging or formula decisions. "
 "Target: implemented by end of Q3."),

("Product Development",
 "Document control: specifications, dielines, artwork versions, BOMs, landed-cost integrity",
 "NI", "AB", ["EH", "JH", "PC"], [], "PDS",
 JD_PD,
 "Documentation quality is Nicole's gate. The PD Specialist JD names document control as a core "
 "responsibility, so this row transitions on hire."),

("Operations & Supply Chain",
 "Production scheduling with manufacturing partners",
 "AB", "AB", ["PC", "NI"], [], "OPS",
 f"{JD_OPS}; {MTG} 35:18",
 "Named in the Ops Specialist JD under Planning & Special Projects. Today Alvin coordinates KDC "
 "scheduling directly. A and R both AB until the seat is filled."),

("Ecommerce & DTC",
 "Channel operations and promo setup across DTC, UBM and Amazon",
 "NI", "AB", ["SS", "KL"], ["DI"], "OPS",
 JD_OPS,
 "Named in the Ops Specialist JD under Order Management & Channel Operations. Nicole holds the "
 "channel relationship."),

("Ecommerce & DTC",
 "Proactive reships and fulfillment-issue resolution",
 "NI", "NI", ["AB"], [], "OPS",
 JD_OPS,
 "JD wording: resolve fulfillment issues \"before a customer has to follow up.\" Sits inside "
 "Nicole's interim OC3PL coverage. A and R both NI."),

("Marketing & Brand",
 "Operational special projects: labels, PR seeding, sampling",
 "NI", "AB", ["SS", "KL", "EH"], [], "OPS",
 f"{JD_OPS}; {EMAIL}",
 "Named in the Ops Specialist JD, and in the email as making sure product is where it needs to be "
 "for launches, promos, PR seeding and sampling."),

("People & Admin",
 "Operations Specialist recruiting",
 "AB", "NI", ["DI"], ["AC"], "",
 f"{MTG} 52:48-53:17; {EMAIL}",
 "Prioritized first. Danielle: \"we're going to prioritize the operations... Specialist.\" "
 "Reports to Nicole. Target in place before Q4. Salary band $72-90K."),

("People & Admin",
 "PD Specialist role definition and phased recruiting",
 "AB", "NI", ["DI"], ["AC"], "",
 f"{MTG} 53:17-57:10; {EMAIL}",
 "Phased in after the Ops Specialist. Danielle scopes it as \"air traffic control, holding people "
 "accountable\" rather than strategy or ideation, and is adding trend-forecasting language to the JD. "
 "Reports to Nicole. Salary band $75-95K."),

("People & Admin",
 "SOP cleanup and operational prep before new-hire onboarding",
 "AB", "NI", [], ["DI"], "",
 f"{MTG} 54:24-55:43, 1:00:32",
 "Danielle's condition on the hire: clean up the system first so the role can function. "
 "Nicole's action item from the review."),

("IT / Systems & Data",
 "RACI and role framework across Operations and PD",
 "AB", "NI", ["DI"], [], "",
 f"{MTG} 52:12-52:39",
 "Alvin owns the framework, built with Nicole in the builder session, then to Danielle for final "
 "review before it goes to Calm HR to start recruiting."),
]

v2.extend(NEW)

# ---------------------------------------------------------------- emit
POSITIONS = [
    ("AC", "Ayesha Curry", "Owner / Founder", "filled"),
    ("DI", "Danielle Iturbe", "President", "filled"),
    ("AB", "Alvin Belt", "VP of Operations", "filled"),
    ("NI", "Nicole Iturbe", "Sr. Director, Consumer Strategy & Operations", "filled"),
    ("OPS", "Open seat", "Operations Specialist", "recruiting"),
    ("PDS", "Open seat", "Product Development Specialist", "phased"),
    ("SS", "Soraya Salgadoe", "Marketing Manager", "filled"),
    ("KL", "Kate Le", "Social Media Coordinator", "filled"),
    ("EH", "Erin Hover", "Creative Director", "filled"),
    ("IT", "Ivy Tan", "Creative / Design Coordinator", "filled"),
    ("JH", "Jan Haeck", "Packaging Engineer", "contractor"),
    ("PC", "Perrine Calvet", "PD / R&D contractor, Milinyc", "contractor"),
]

out = io.open("raci_rows.py", "w", encoding="utf-8")
out.write('''"""RACI rows for AC Brands. v2 — position-first, 2026-07-30 leadership review applied.

Tuple: (Function, Activity, A, R, [C...], [I...], Transition, Source, Notes)
  A = answers for the outcome. R = does the work. One of each per row.
  Transition = "" | "OPS" | "PDS" — the incoming seat that absorbs R on hire.
  Open seats never hold A or R; a vacancy cannot be accountable.
Sources: paths are relative to /home/user/SJ-OS. Non-path sources are the four
primary sources from the 2026-07-30 leadership review and the 2026-07-27 email.
"""

''')
out.write("POSITIONS = [\n")
for p in POSITIONS:
    out.write(f"  {p!r},\n")
out.write("]\n\nROWS = [\n")
last_func = None
for r in v2:
    if r[0] != last_func:
        out.write(f"\n# ==== {r[0]} ====\n")
        last_func = r[0]
    out.write(f"  {r!r},\n")
out.write("]\n")
out.close()
print(f"v2 rows: {len(v2)} (v1 was {len(V1)}, +1 from the stability split, +{len(NEW)} new)")
