"""v2 -> v3.

Three corrections from Alvin, 2026-07-31:
1. Erin Hover is a contractor and the lead technical authority on packaging and
   artwork. She takes A on packaging development, artwork execution and the label
   artwork archive. Perrine stays consulted where formula contact matters.
2. Danielle Iturbe, as President, takes A on brand guideline custody and campaign
   direction, and is consulted across Creative and Marketing.
3. Ayesha Curry is consulted on brand and creative work - her name is on the
   product - and keeps sole accountability for brand-line moves.

Adds a Campaign direction row: seasonal brand moments were absent from the matrix
entirely, which is why Danielle and Ayesha had no Marketing presence to sit on.
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raci_rows_v2 as v2

S = ".claude/skills/"
MTG = "Leadership Business Review 2026-07-30"
ALVIN = "Alvin, 2026-07-31 (role correction)"

# --------------------------------------------------------------- positions
POSITIONS = []
for pid, name, title, status in v2.POSITIONS:
    if pid == "EH":
        status = "contractor"      # contractor, and lead technical authority
    POSITIONS.append((pid, name, title, status))

def setrow(row, A=None, R=None, C=None, I=None, note=None, src=None):
    f, act, a, r, c, i, t, s, n = row
    a = A if A else a
    r = R if R else r
    c = list(C) if C is not None else list(c)
    i = list(I) if I is not None else list(i)
    # a person can hold only one letter
    c = [k for k in c if k not in (a, r)]
    i = [k for k in i if k not in (a, r) and k not in c]
    if note:
        n = f"{n} {note}"
    if src:
        s = f"{s}; {src}"
    return (f, act, a, r, c, i, t, s, n)

EDITS = {
 # ---- Erin: lead technical authority on packaging and artwork ----
 "Packaging development with fillers and component vendors": dict(
   A="EH", R="JH", C=["PC", "AB", "IT"], I=["DI", "AC"],
   note="Erin is the lead technical authority on packaging and artwork and answers for the "
        "outcome; Jan executes under her. Perrine consults where formula contact or "
        "compatibility is in play. Both Erin and Jan are contractors.",
   src=ALVIN),

 "Packaging and artwork execution": dict(
   A="EH", R="JH", C=["PC", "IT"], I=["AB", "DI", "AC"],
   note="Erin holds technical authority; Jan executes. Both contractors.",
   src=ALVIN),

 "Label artwork archive, IL cross-check and label-law checks (Pantone, Canada, Quebec, 19-state toxics)": dict(
   A="EH", R="AB", C=["PC", "JH", "NI", "AC"], I=["DI"],
   note="Erin answers for the artwork being right as lead technical authority. Alvin runs the "
        "IL cross-check and the label-law passes and holds the Reg Lead gate on archive "
        "entries, so the regulatory approval and the artwork authority are separate people.",
   src=ALVIN),

 # ---- Danielle: brand and campaign accountability ----
 "Brand guideline custody (fonts, colors, logos, voice)": dict(
   A="DI", R="EH", C=["IT", "SS", "AC"], I=["KL"],
   note="President answers for brand custody; Creative Director maintains it. Ayesha consulted - "
        "the brand carries her name. Every output-producing skill defers here for canonical spec.",
   src=ALVIN),

 "Creative direction on packaging, artwork and brand visuals": dict(
   A="EH", R="EH", C=["IT", "SS", "DI", "AC"], I=["AB"],
   note="Creative Director owns the direction as lead technical authority, and is a contractor. "
        "Danielle and Ayesha both consulted. A and R the same person - no second pair of eyes, "
        "and no internal backup either.",
   src=ALVIN),

 "Creative Requests intake and design coordination": dict(
   C=["EH", "SS", "DI"], I=["AB"],
   note="Danielle consulted on intake priority.", src=ALVIN),

 # ---- Danielle and Ayesha consulted across Marketing ----
 "Quarterly competitive teardowns across the five comp brands": dict(
   C=["KL", "NI", "DI"], I=["AB", "AC"],
   note="Danielle consulted rather than only receiving the finished teardown.", src=ALVIN),

 "Monthly competitive trend digest and cross-stream signal routing": dict(
   C=["SS", "KL", "DI"], I=["AB", "AC"],
   note="Danielle consulted on the digest's read.", src=ALVIN),

 "Social listening and comp brand monitoring (TikTok, IG, Pinterest, retailer new arrivals)": dict(
   C=["SS", "DI"], I=["AC"],
   note="Danielle consulted on what the social signal implies for brand.", src=ALVIN),

 "Operational special projects: labels, PR seeding, sampling": dict(
   C=["SS", "KL", "EH", "DI"], I=["AC"],
   note="Danielle consulted - PR seeding and sampling are brand-facing.", src=ALVIN),

 # ---- Ayesha consulted where the brand carries her name ----
 "Retailer attestation responses (Sephora, Ulta, Whole Foods, Credo)": dict(
   C=["NI", "PC", "AC"], I=["DI"],
   note="Ayesha consulted - retailer clean-standard positioning is a brand claim.", src=ALVIN),

 "Claim substantiation and new-claim defensibility": dict(
   C=["SS", "PC", "EH", "AC"], I=["DI"],
   note="The procedure exists because new claims from marketing or the founder used to skip "
        "Pedrero sign-off, so both are consulted rather than bypassed.", src=ALVIN),
}

rows = []
for row in v2.ROWS:
    e = EDITS.get(row[1])
    rows.append(setrow(row, **e) if e else row)

seen = {r[1] for r in rows}
for k in EDITS:
    assert k in seen, f"edit target not found: {k}"

# --------------------------------------------------------------- new row
NEW = [
("Marketing & Brand",
 "Campaign direction and seasonal brand moments",
 "DI", "SS", ["EH", "KL", "NI", "AC"], ["AB"], "",
 f"{ALVIN}; {S}sjs-margin-walk-away/SKILL.md:93",
 "Added 2026-07-31. Campaign direction was absent from the matrix, which is why the President "
 "and the Founder had almost no Marketing presence. Danielle answers for it - Soraya reports to "
 "her and the margin sources already have her approving every repricing and channel call. "
 "Ayesha consulted on brand moments."),
]
rows.extend(NEW)

# --------------------------------------------------------------- emit
out = io.open("raci_rows.py", "w", encoding="utf-8")
out.write('''"""RACI rows for AC Brands. v3 — position-first.

Tuple: (Function, Activity, A, R, [C...], [I...], Transition, Source, Notes)
  A = answers for the outcome. R = does the work. One of each per row.
  Transition = "" | "OPS" | "PDS" — the incoming seat that absorbs R on hire.
  Open seats never hold A or R; a vacancy cannot be accountable.

v2 applied the 2026-07-30 leadership review (quality gate to Nicole, Perrine to
technical advisor, two open seats). v3 adds three corrections from Alvin: Erin
Hover is a contractor and the lead technical authority on packaging and artwork;
Danielle Iturbe takes brand and campaign accountability as President; Ayesha Curry
is consulted on brand and creative work rather than only informed.

Sources: paths are relative to /home/user/SJ-OS. Non-path sources are the
2026-07-30 leadership review, the 2026-07-27 email to Danielle, the two specialist
job descriptions, and Alvin's role corrections of 2026-07-31.
"""

''')
out.write("POSITIONS = [\n")
for p in POSITIONS:
    out.write(f"  {p!r},\n")
out.write("]\n\nROWS = [\n")
lastf = None
for r in rows:
    if r[0] != lastf:
        out.write(f"\n# ==== {r[0]} ====\n")
        lastf = r[0]
    out.write(f"  {r!r},\n")
out.write("]\n")
out.close()
print(f"v3 rows: {len(rows)} (v2 was {len(v2.ROWS)}, +{len(NEW)} new, {len(EDITS)} edited)")
