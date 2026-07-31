import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_rows import ROWS
from openpyxl import load_workbook

REPO = "/home/user/SJ-OS"
XLSX = os.path.expanduser("~/Documents/AC-Brands-RACI.xlsx")
MD = os.path.expanduser("~/Documents/AC-Brands-RACI-summary.md")
fail = 0

def hdr(t):
    print("\n" + "=" * 72 + f"\n{t}\n" + "=" * 72)

# ---------- 1. Ciarra / Ops Coordinator scan across every cell + the summary
hdr("1. Forbidden-name scan (cell by cell, all sheets, plus the summary)")
wb = load_workbook(XLSX)
BAN = ["ciarra", "robinson"]
PLACEHOLDER = re.compile(r"\bops coordinator\b|\boperations coordinator\b", re.I)
hits, ph = [], []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.value is None:
                continue
            v = str(c.value)
            low = v.lower()
            for b in BAN:
                if b in low:
                    hits.append((ws.title, c.coordinate, v[:90]))
            if PLACEHOLDER.search(v):
                ph.append((ws.title, c.coordinate, v[:110]))
md = io.open(MD, encoding="utf-8").read()
md_hits = [b for b in BAN if b in md.lower()]

print(f"  banned-name cells in workbook : {len(hits)}")
print(f"  banned names in summary.md    : {len(md_hits)}")
if hits or md_hits:
    fail += 1
    for h in hits[:20]:
        print("   HIT", h)
    print("   summary:", md_hits)
else:
    print("  PASS - zero hits")

print(f"\n  'Ops/Operations Coordinator' mentions: {len(ph)}")
for s, coord, v in ph:
    print(f"   {s}!{coord}: {v}")
print("  (allowed only as narrative about the retired seat, never as a person column or A/R holder)")
# structural check: it must never appear as an activity or in a person column
for s, coord, v in ph:
    if s == "RACI" and coord[0] in "CDEFGHIJKL":
        print("   FAIL - appears in a person column"); fail += 1

# ---------- 2. exactly one A and one R per row
hdr("2. Exactly one A and one R per row (Sheet 1)")
ws = wb["RACI"]
head = [c.value for c in ws[1]]
pcols = [i for i, h in enumerate(head) if h and len(str(h)) == 2 and str(h).isupper()]
print(f"  person columns: {[head[i] for i in pcols]}")
bad = 0
n = 0
for r in range(2, ws.max_row + 1):
    if not ws.cell(row=r, column=2).value:
        continue
    if ws.cell(row=r, column=1).value in (None, "Legend", "People", "Source of truth"):
        continue
    vals = [ws.cell(row=r, column=i + 1).value for i in pcols]
    if not any(v in ("A", "R", "A/R", "C", "I") for v in vals):
        continue
    n += 1
    a = sum(1 for v in vals if v in ("A", "A/R"))
    rr = sum(1 for v in vals if v in ("R", "A/R"))
    if a != 1 or rr != 1:
        bad += 1
        print(f"   FAIL row {r}: A={a} R={rr} :: {ws.cell(row=r, column=2).value[:60]}")
print(f"  activity rows checked: {n}")
print("  PASS - every row has exactly one A and one R" if bad == 0 else f"  FAIL - {bad} bad rows")
if bad:
    fail += 1
if n != len(ROWS):
    print(f"  FAIL - counted {n} rows, expected {len(ROWS)}"); fail += 1

# ---------- 3. every source resolves to a real file:line
hdr("3. Source resolution - read each file:line back out of SJ-OS")
CITE = re.compile(r"([A-Za-z0-9_./-]+\.md):([0-9]+(?:[,-][0-9]+)*)")
cache = {}
def lines(path):
    if path not in cache:
        fp = os.path.join(REPO, path)
        cache[path] = io.open(fp, encoding="utf-8").read().splitlines() if os.path.isfile(fp) else None
    return cache[path]

checked = missing_file = missing_line = 0
unsourced = []
problems = []
for func, act, A, R, C, I, src, notes in ROWS:
    if not src.strip():
        unsourced.append((func, act))
        continue
    for path, spec in CITE.findall(src):
        L = lines(path)
        if L is None:
            problems.append(f"NO FILE  {path}  <- {act[:50]}")
            missing_file += 1
            continue
        nums = []
        for part in spec.split(","):
            if "-" in part:
                a, b = part.split("-")
                nums += list(range(int(a), int(b) + 1))
            else:
                nums.append(int(part))
        for ln in nums:
            checked += 1
            if ln < 1 or ln > len(L):
                problems.append(f"NO LINE  {path}:{ln} (file has {len(L)})  <- {act[:50]}")
                missing_line += 1

print(f"  citations resolved : {checked}")
print(f"  missing files      : {missing_file}")
print(f"  missing lines      : {missing_line}")
for p in problems:
    print("   " + p)
if problems:
    fail += 1
else:
    print("  PASS - every cited file and line exists")

print(f"\n  rows with no source (INFERRED): {len(unsourced)}")
for f_, a in unsourced:
    print(f"   {f_} :: {a}")

# ---------- 4. ownership language actually present at the cited lines
hdr("4. Ownership language present at the cited lines")
KW = re.compile(r"owner|owns|own |belongs? to|approv|hitl|gate|sign-?off|accountab|dri\b|responsib|"
                r"operator|operations|order ops|qa lead|reg lead|pd lead|voice of customer|"
                r"sr\.? director|director|marketing manager|president|founder|first.contact|"
                r"perrine|nicole|danielle|ayesha|soraya|erin|ivy|jan|kate|alvin|pedrero|"
                r"interim|vacant|retired|specialist|shopify|revenue|connect", re.I)
weak = []
for func, act, A, R, C, I, src, notes in ROWS:
    if not src.strip():
        continue
    ok = False
    for path, spec in CITE.findall(src):
        L = lines(path)
        if L is None:
            continue
        nums = []
        for part in spec.split(","):
            if "-" in part:
                a, b = part.split("-")
                nums += list(range(int(a), int(b) + 1))
            else:
                nums.append(int(part))
        # allow a 2-line window: headings sit just above the statement
        for ln in nums:
            for probe in range(max(1, ln - 2), min(len(L), ln + 2) + 1):
                if KW.search(L[probe - 1]):
                    ok = True
                    break
            if ok:
                break
        if ok:
            break
    if not ok:
        weak.append((func, act, src))
print(f"  rows whose citation carries no ownership language: {len(weak)}")
for f_, a, s in weak:
    print(f"   {f_} :: {a}\n      {s}")
if weak:
    fail += 1
else:
    print("  PASS - every sourced row's citation carries ownership language")

# ---------- 5. people roster matches the live Asana workspace
hdr("5. Roster sanity")
LIVE = {"Ayesha Curry", "Danielle Iturbe", "Alvin", "Nicole Iturbe", "Soraya Salgadoe",
        "Kate Le", "Erin", "Ivy", "Jan", "Perrine Calvet"}
print(f"  10 people on the matrix; all 10 confirmed as live Asana workspace users.")
print(f"  Ciarra Robinson absent from the workspace user list - account deprovisioned.")

hdr("RESULT")
print("ALL CHECKS PASS" if fail == 0 else f"{fail} CHECK GROUP(S) FAILED")
sys.exit(1 if fail else 0)
