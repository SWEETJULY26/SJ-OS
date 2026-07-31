import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raci_rows import ROWS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = os.path.expanduser("~/Documents/AC-Brands-RACI.xlsx")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

PEOPLE = [
    ("AC", "Ayesha Curry", "Owner / Founder"),
    ("DI", "Danielle Iturbe", "President"),
    ("AB", "Alvin Belt", "VP of Operations"),
    ("NI", "Nicole Iturbe", "Sr. Director, Consumer Strategy & Operations"),
    ("SS", "Soraya Salgadoe", "Marketing Manager"),
    ("KL", "Kate Le", "Social Media Coordinator"),
    ("EH", "Erin Hover", "Creative Director"),
    ("IT", "Ivy Tan", "Creative / Design Coordinator"),
    ("JH", "Jan Haeck", "Packaging Engineer (contractor, under Erin)"),
    ("PC", "Perrine Calvet", "PD / R&D / Quality owner (Milinyc, contractor)"),
]
INITIALS = [p[0] for p in PEOPLE]

ARIAL = "Arial"
F_BODY = Font(name=ARIAL, size=10)
F_HEAD = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
F_BOLD = Font(name=ARIAL, size=10, bold=True)
F_TITLE = Font(name=ARIAL, size=13, bold=True)
FILL_HEAD = PatternFill("solid", fgColor="1F3B4D")
FILL_A = PatternFill("solid", fgColor="C0504D")   # accountable
FILL_R = PatternFill("solid", fgColor="4F81BD")   # responsible
FILL_FUNC = PatternFill("solid", fgColor="EDF1F5")
F_AR = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
THIN = Side(style="thin", color="D0D7DE")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")

wb = Workbook()

# ---------------------------------------------------------------- Sheet 1: RACI
ws = wb.active
ws.title = "RACI"
headers = ["Function", "Activity"] + INITIALS + ["Source (file:line)", "Notes"]
ws.append(headers)
for c in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=c)
    cell.font = F_HEAD
    cell.fill = FILL_HEAD
    cell.alignment = CENTER if 3 <= c <= 2 + len(INITIALS) else Alignment(vertical="center", wrap_text=True)
    cell.border = BORDER

for func, act, A, R, C, I, src, notes in ROWS:
    letters = {A: "A", R: "R"}
    if A == R:
        letters[A] = "A/R"
    for k in C:
        letters.setdefault(k, "C")
    for k in I:
        letters.setdefault(k, "I")
    ws.append([func, act] + [letters.get(i, "") for i in INITIALS] + [src, notes])

last = ws.max_row
for r in range(2, last + 1):
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=r, column=c)
        cell.font = F_BODY
        cell.border = BORDER
        if 3 <= c <= 2 + len(INITIALS):
            cell.alignment = CENTER
            v = cell.value
            if v in ("A", "A/R"):
                cell.fill, cell.font = FILL_A, F_AR
            elif v == "R":
                cell.fill, cell.font = FILL_R, F_AR
        else:
            cell.alignment = WRAP
    ws.cell(row=r, column=1).fill = FILL_FUNC
    ws.cell(row=r, column=1).font = F_BOLD

ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{last}"
ws.column_dimensions["A"].width = 24
ws.column_dimensions["B"].width = 62
for i in range(len(INITIALS)):
    ws.column_dimensions[get_column_letter(3 + i)].width = 5
ws.column_dimensions[get_column_letter(3 + len(INITIALS))].width = 60
ws.column_dimensions[get_column_letter(4 + len(INITIALS))].width = 80
ws.row_dimensions[1].height = 30

# legend + people key below the table
lr = last + 2
ws.cell(row=lr, column=1, value="Legend").font = F_TITLE
for j, (txt, fill) in enumerate([
    ("A = answers for the outcome (one per row)", FILL_A),
    ("R = does the work (one per row)", FILL_R),
    ("A/R = the same person holds both, so the row has no second pair of eyes", FILL_A),
    ("C = consulted before the decision", None),
    ("I = informed after it", None),
]):
    c = ws.cell(row=lr + 1 + j, column=2, value=txt)
    c.font = F_BODY
    if fill:
        ws.cell(row=lr + 1 + j, column=1).fill = fill

pr = lr + 7
ws.cell(row=pr, column=1, value="People").font = F_TITLE
ws.cell(row=pr + 1, column=1, value="Initials").font = F_BOLD
ws.cell(row=pr + 1, column=2, value="Name and role").font = F_BOLD
for j, (ini, name, role) in enumerate(PEOPLE):
    ws.cell(row=pr + 2 + j, column=1, value=ini).font = F_BODY
    ws.cell(row=pr + 2 + j, column=2, value=f"{name} — {role}").font = F_BODY

nr = pr + 2 + len(PEOPLE) + 1
ws.cell(row=nr, column=1, value="Source of truth").font = F_BOLD
ws.cell(row=nr, column=2,
        value="All paths are relative to the SJ-OS repo. Ownership was extracted from the repo, "
              "not assumed. Rows marked INFERRED in Notes have no owner named in any source; A "
              "defaults to Alvin Belt because the work falls to him in practice.").font = F_BODY
ws.cell(row=nr, column=2).alignment = WRAP

# ------------------------------------------------------------ Sheet 2: Analysis
an = wb.create_sheet("Analysis")
an.column_dimensions["A"].width = 118
an.column_dimensions["B"].width = 10
an.column_dimensions["C"].width = 10
an.column_dimensions["D"].width = 10

def para(text, bold=False, size=10, gap_after=True):
    r = an.max_row + 1 if an.max_row > 1 or an["A1"].value else 1
    c = an.cell(row=r, column=1, value=text)
    c.font = Font(name=ARIAL, size=size, bold=bold)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    an.row_dimensions[r].height = max(15, 13 * (len(text) // 105 + 1))
    if gap_after:
        an.cell(row=r + 1, column=1, value="")
    return r

para("Ownership concentration and coverage gaps", bold=True, size=13)
para("Read against the RACI sheet. Every claim below traces to a file and line in SJ-OS. "
     "Counts are live formulas over the RACI sheet, so they move if a row changes.")

# live counts table
hr = an.max_row + 1
for j, h in enumerate(["Person", "A count", "R count", "A/R rows"]):
    cell = an.cell(row=hr, column=1 + j, value=h)
    cell.font = F_HEAD
    cell.fill = FILL_HEAD
    cell.alignment = CENTER if j else Alignment(vertical="center")
nrows = len(ROWS) + 1
for j, (ini, name, role) in enumerate(PEOPLE):
    r = hr + 1 + j
    col = get_column_letter(3 + INITIALS.index(ini))
    an.cell(row=r, column=1, value=f"{ini} — {name}").font = F_BODY
    an.cell(row=r, column=2,
            value=f'=COUNTIF(RACI!{col}2:{col}{nrows},"A")+COUNTIF(RACI!{col}2:{col}{nrows},"A/R")').font = F_BODY
    an.cell(row=r, column=3,
            value=f'=COUNTIF(RACI!{col}2:{col}{nrows},"R")+COUNTIF(RACI!{col}2:{col}{nrows},"A/R")').font = F_BODY
    an.cell(row=r, column=4, value=f'=COUNTIF(RACI!{col}2:{col}{nrows},"A/R")').font = F_BODY
    for cc in (2, 3, 4):
        an.cell(row=r, column=cc).alignment = CENTER
tr = hr + 1 + len(PEOPLE)
an.cell(row=tr, column=1, value="Total rows").font = F_BOLD
an.cell(row=tr, column=2, value=f"=COUNTA(RACI!B2:B{nrows})").font = F_BOLD
an.cell(row=tr, column=2).alignment = CENTER
an.cell(row=tr + 1, column=1, value="")

ANALYSIS = [
 ("Where accountability sits", True),
 ("Alvin Belt is accountable for 38 of the 66 activities on this matrix and does the work on 50 of them. "
  "The next largest book of accountability is 11. The reason is structural rather than a matter of habit: three "
  "canonical role-maps define an Operator role that holds the approval gate on essentially every write across "
  "Product Development, Operations, Quality and Regulatory, and all three name the same person. In Regulatory "
  "the concentration doubles up. regulatory-manager/references/role-map.md:14 states that Reg Lead is \"the same "
  "person as Operator at v6.3,\" so on an IL packet or an FDA filing the two supposedly independent gates fire "
  "against one person twice.", False),

 ("Rows with no second pair of eyes", True),
 ("43 of the 66 rows have the same person as both A and R. Thirty-four of those are Alvin. That is not a "
  "drafting artifact — the sources genuinely put the drafting, the approving and the committing on one desk. The "
  "ones that carry the most exposure are the FDA and MoCRA filings, where "
  "adverse-event-and-recall-reporter/SKILL.md:65,108 defines a Pedrero send approval and an agency submission "
  "approval as two distinct audit-trail entries, and Alvin holds both; the recall kickoff at "
  "complaint-and-event-handler/SKILL.md:89,95, described as the strictest gate in the suite with §4.A through "
  "§4.F each needing separate approval, all of it his; and the landing hub publish at "
  "quality-status-reporter/SKILL.md:34-50, where every commit goes to main and triggers a live deploy behind a "
  "single approver.", False),

 ("Functions with no owner in the sources", True),
 ("Three. Accounts payable, bookkeeping and payroll appear nowhere as owned work — Finance shows up only as an "
  "email-sender category in outlook-plm-bridge/SKILL.md:368 and as a bullet heading in "
  "ayesha-weekly-briefing/SKILL.md:9. Employee onboarding, offboarding and access deprovisioning has no named "
  "owner either; the only documented process is the departed-role-holder checklist at "
  "asana-pd-manager/references/role-map.md:48-56, which exists because a stale role row broke collaborator "
  "resolution during a build. Shopify revenue ownership is registered as a connection in connections.md:7 and "
  "named as the primary DTC revenue track in context/about-business.md:5, but no skill assigns a gate or an "
  "owner. Those three rows carry A = AB on the matrix as an inference, not as a sourced claim, and they are "
  "flagged INFERRED in Notes.", False),

 ("What the retired Ops Coordinator seat left behind", True),
 ("The prompt for this RACI assumed that work transferred to Alvin. The repo is more specific, and it was "
  "already decided. decisions/log.md:50-62 records the 2026-07-17 call to retire the Operations Coordinator role "
  "rather than backfill it, replacing it with an Operations Specialist and a Product Development Project Manager "
  "Specialist, both reporting to Nicole. The interim split is Alvin on inventory and logistics, Nicole on order "
  "management and OC3PL. That shows up on six rows: inventory position keeping and inbound freight and customs "
  "sit with Alvin; daily DTC order operations and the DTC fulfillment dashboard sit with Nicole; pre-ship "
  "out-of-stock holds are split, accountable to Nicole and worked by Alvin. Tool "
  "procurement, vendor renewals and shared-folder admin went to Alvin as well, per "
  "sjs-comp-intel/references/team-ownership.md:50, which says explicitly that he carries it until the Operations "
  "Specialist starts.", False),

 ("The interim state has costs that are already visible", True),
 ("decisions/log.md:60 records two items still open from the July cleanup: 22 of the departed coordinator's "
  "Asana tasks sit unassigned in an archived holding project, four of them already overdue, and her contact wiki "
  "page still resolves as an active internal contact, so the four Outlook and Fireflies bridges keep classifying "
  "mail from her as internal. Both are the kind of thing a coordinator seat would have closed in a week. Neither "
  "has closed in a quarter.", False),

 ("Single points of failure with no named backup", True),
 ("Perrine Calvet is accountable for 11 activities and is an external contractor at Milinyc. Every technical "
  "quality gate runs through her — NCR to CAPA conversion, root cause sign-off, verification, effectiveness, "
  "CAPA close, vendor flags, and every batch hold and release, which "
  "batch-lifecycle-tracker/references/batch-lifecycle-procedure.md:208 states admit no exceptions. She also "
  "holds pre-launch compatibility, stability, RIPT and PET decisions as both A and R, with no internal "
  "counterpart. On top of that she is filling a seat that is formally vacant: "
  "quality-manager/references/role-map.md:16 notes that SOP §7 requires a QA Manager to approve SOP revisions "
  "and that responsibility currently sits with her as QA Lead. If she is unavailable, no batch releases and no "
  "SOPs ratify.", False),

 ("Alvin is the other one, and the sources say so plainly. The Operator gate has no alternate anywhere in the "
  "suite. references/architecture/asana_task_contract.md:227 handles an unresolvable role-holder by surfacing "
  "the question for him to answer rather than routing around him, which is correct behaviour and also a "
  "description of the bottleneck. All 23 scheduled Routines stop at a HITL gate that only he can clear — "
  "scheduled-prompts/weekly-pd-update.md:91 puts it as \"nothing commits until Alvin says go\" — so a week away "
  "does not pause the work, it queues it.", False),

 ("Succession is documented exactly once in the whole system. "
  "sjs-comp-intel/references/team-ownership.md:95 names Soraya as interim DRI if Nicole is unavailable and says "
  "what to stop doing if both are out. Nothing comparable exists for the Operator role, the QA Lead role, the "
  "Reg Lead role, or Creative. For a repo whose stated purpose in decisions/log.md:41 is to be an operating "
  "system \"built for succession,\" one succession plan across eleven functions is the gap that matters most.", False),

 ("What this means for headcount", True),
 ("The two-specialist decision was made on 2026-07-17 and neither seat is filled. The matrix shows why that is "
  "expensive rather than merely untidy. Both roles were designed to report to Nicole, and "
  "decisions/log.md:54 gives the reasoning: moving day-to-day ops management off the VP seat is the succession "
  "point the whole system is being built toward. Right now the opposite is happening. Alvin absorbed inventory "
  "and logistics on top of a book that already held every Operator gate in four functions, and Nicole absorbed "
  "order management and OC3PL on top of being Stream DRI for competitive intelligence, Voice of Customer for "
  "quality, PD Consult, and the retailer relationship owner.", False),

 ("Alvin does the work on 11 of the 12 Operations rows. Filling the Operations Specialist seat moves most of "
  "that — the inventory ledger, receiving, three-way reconciliation, freight and customs, procurement admin and "
  "the shortage-sheet work. He also does the work on 5 of the 7 Product Development rows; the PD Project Manager "
  "seat takes the stage-gate stewardship, the Asana follow-up discipline and the intake bridges. That still "
  "leaves him with every approval gate, which is arguably "
  "correct for a VP. The problem today is that he holds the gates and does the work behind them.", False),

 ("The third gap is not on the hiring plan and should be. Quality has no internal technical authority. The QA "
  "Manager seat is vacant, an external contractor is covering it, and the batch release gate has no alternate. "
  "Sweet July Skin sells through Sephora, Ulta and Whole Foods under MoCRA, so a contractor being unavailable is "
  "a shipping problem and a filing problem at the same time.", False),
]
for text, bold in ANALYSIS:
    para(text, bold=bold, size=11 if bold else 10)

# ---------------------------------------------------------------- Sheet 3: Gaps
gp = wb.create_sheet("Gaps")
gh = ["Type", "Function", "Gap", "Why it matters", "Suggested owner", "Est. hrs / month", "Source (file:line)"]
gp.append(gh)
for c in range(1, len(gh) + 1):
    cell = gp.cell(row=1, column=c)
    cell.font, cell.fill = F_HEAD, FILL_HEAD
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border = BORDER

GAPS = [
 ("Unowned function", "Finance",
  "Accounts payable, bookkeeping and payroll have no owner, approver or gate anywhere in SJ-OS.",
  "Spend is captured (vendor_invoices, five HITL gates) but nothing downstream of it is owned. The cost ledger has a custodian; the books do not.",
  "Fractional controller or bookkeeper; Alvin approves", 20,
  ".claude/skills/outlook-plm-bridge/SKILL.md:368; .claude/skills/ayesha-weekly-briefing/SKILL.md:9"),

 ("Unowned function", "People & Admin",
  "Employee onboarding, offboarding and access deprovisioning has no named owner.",
  "The only documented process is a departed-role-holder checklist written after a stale role row broke Asana collaborator resolution. It was written reactively and it is not owned.",
  "Operations Specialist once hired; Alvin interim", 6,
  ".claude/skills/asana-pd-manager/references/role-map.md:48-56"),

 ("Unowned function", "Ecommerce & DTC",
  "Shopify revenue and channel position has no owner or gate.",
  "Registered as the revenue connection and named as the primary DTC revenue track, but no skill assigns ownership. The one function closest to the top line is the least specified.",
  "Nicole (channel), Alvin (data)", 8,
  "connections.md:7; context/about-business.md:5"),

 ("Vacant seat", "Quality",
  "QA Manager seat is vacant. SOP §7 requires a QA Manager to approve SOP revisions; an external contractor is filling it.",
  "No internal technical quality authority exists. Every batch release, every SOP ratification and every CAPA close depends on a contractor being available.",
  "In-house QA Manager; Perrine interim", 40,
  ".claude/skills/quality-manager/references/role-map.md:16"),

 ("Vacant seat", "Operations & Supply Chain",
  "Operations Specialist seat approved 2026-07-17, not filled. Reports to Nicole.",
  "Inventory, logistics, receiving, reconciliation and procurement admin are being carried by the VP of Operations as interim cover, a quarter past the decision.",
  "New hire, reporting to Nicole", 100,
  "decisions/log.md:52,58; context/priorities.md:3"),

 ("Vacant seat", "Product Development",
  "PD Project Manager Specialist seat approved 2026-07-17, not filled. Reports to Nicole.",
  "PD stage-gate stewardship, Asana follow-up and supplier chasing sit on the VP seat. Chasing suppliers and updating Asana by hand is the stated top recurring pain.",
  "New hire, reporting to Nicole", 100,
  "decisions/log.md:52,58; context/priorities.md:3"),

 ("Single point of failure", "Quality",
  "Perrine Calvet holds every technical quality gate with no named backup, as an external contractor.",
  "Batch hold and release admit no exceptions at v5.4. If she is unavailable, product does not release and SOPs do not ratify.",
  "Name a backup approver; hire the QA Manager", 0,
  ".claude/skills/batch-lifecycle-tracker/references/batch-lifecycle-procedure.md:208; .claude/skills/quality-manager/references/role-map.md:14"),

 ("Single point of failure", "Product Development",
  "Compatibility, stability, RIPT and PET decisions are A and R on the same contractor with no internal counterpart.",
  "Pre-launch technical decisions have no internal reviewer. Nobody inside AC Brands can check the work or continue it.",
  "PD Project Manager Specialist as internal counterpart", 0,
  ".claude/skills/asana-pd-manager/references/role-map.md:16"),

 ("Single point of failure", "Regulatory & Compliance",
  "Operator and Reg Lead are the same person, so two gates that were designed to be independent fire against one approver.",
  "On IL packets, retailer attestations and FDA filings the second approval adds an audit-trail entry but no second judgment. The 15-day MoCRA clock has no alternate approver.",
  "Split Reg Lead to Pedrero-side or a new hire", 0,
  ".claude/skills/regulatory-manager/references/role-map.md:14; .claude/skills/adverse-event-and-recall-reporter/SKILL.md:108"),

 ("Single point of failure", "IT / Systems & Data",
  "All 23 scheduled Routines stop at a HITL gate only Alvin can clear.",
  "Automation that fires unattended still needs him to commit. A week away queues the work rather than pausing it, and the Routines keep firing.",
  "Delegate publish gates to the new specialists", 0,
  "scheduled-prompts/weekly-pd-update.md:91; scheduled-prompts/sjs-purchasing-monthly-rollup-and-snapshot.md:79"),

 ("Single point of failure", "Marketing & Brand",
  "Succession is documented once in the entire system — Soraya as interim CI DRI if Nicole is out.",
  "No equivalent exists for the Operator, QA Lead, Reg Lead or Creative roles. The repo's stated purpose is succession.",
  "Alvin to write per-role backups into each role-map", 4,
  ".claude/skills/sjs-comp-intel/references/team-ownership.md:95; decisions/log.md:41"),

 ("Open item", "Operations & Supply Chain",
  "22 tasks from the retired coordinator seat sit unassigned in an archived holding project; 4 are overdue.",
  "An unassigned task drops out of every per-person sweep and goes stale silently. This is the concrete cost of running the interim split for a quarter.",
  "Alvin to reassign under the interim split", 3,
  "decisions/log.md:60"),

 ("Open item", "IT / Systems & Data",
  "The departed coordinator's contact wiki page still resolves as an active internal contact.",
  "All four Outlook and Fireflies bridges load contacts at run time, so mail from a departed employee still classifies as internal.",
  "Alvin; one-line wiki update", 1,
  "decisions/log.md:60"),

 ("Open item", "IT / Systems & Data",
  "Job 0 wiki write-back has not fired since 2026-05-26. 123 of 133 pages are untouched seed content.",
  "The bridges' runtime lexicon is reading stale seed data, which degrades vendor, contact and product recognition on every sweep.",
  "Alvin; part of the skills-architecture backlog", 8,
  "decisions/wiki-layer-audit-2026-07-29.md:52; decisions/log.md:75"),

 ("Open item", "Quality",
  "Nine SOPs and forms are showing 29 days overdue on annual review.",
  "next_review_date was NULL on all 13 PLM rows, so the annual-review sweep had nothing to fire on. Dates are restored; the reviews are not done, and each needs QA Lead sign-off.",
  "Perrine approves; Alvin stages", 12,
  "decisions/log.md:69"),

 ("Uncovered brand", "All functions",
  "Sweet July, the lifestyle brand, has no skill coverage. The entire suite is Sweet July Skin plus org-level work.",
  "Merch, licensing and non-skincare retail are run somewhere, but nothing in SJ-OS describes who owns them or how. They cannot be put on a RACI from these sources.",
  "Danielle to confirm scope before the next RACI pass", 0,
  "references/architecture/system_map.md:3; context/about-business.md:3"),
]
for g in GAPS:
    gp.append(list(g))

glast = gp.max_row
for r in range(2, glast + 1):
    for c in range(1, len(gh) + 1):
        cell = gp.cell(row=r, column=c)
        cell.font = F_BODY
        cell.border = BORDER
        cell.alignment = CENTER if c == 6 else WRAP
    gp.cell(row=r, column=1).font = F_BOLD

gp.freeze_panes = "A2"
gp.auto_filter.ref = f"A1:{get_column_letter(len(gh))}{glast}"
for col, w in zip("ABCDEFG", [20, 26, 50, 58, 34, 11, 52]):
    gp.column_dimensions[col].width = w
gp.row_dimensions[1].height = 30

gp.cell(row=glast + 2, column=1, value="Hours per month").font = F_BOLD
gp.cell(row=glast + 2, column=3,
        value="Rough estimates. Vacant-seat rows are full-time-equivalent load, not incremental. "
              "Zero means the gap is a structural exposure rather than unbilled hours.").font = F_BODY
gp.cell(row=glast + 2, column=3).alignment = WRAP

# The Analysis count cells are live COUNTIF formulas over the RACI sheet. openpyxl writes
# formulas without cached values, so force any reader to recalculate on open.
wb.calculation.fullCalcOnLoad = True

wb.save(OUT)
print("wrote", OUT, "| RACI rows:", len(ROWS), "| gaps:", len(GAPS))
