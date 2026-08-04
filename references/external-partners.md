---
name: External partner registry
description: Canonical record of the outside organisations that hold execution of an AC Brands function (regulatory, finance, HR) plus the individual contractors. Who they are, what they own, where accountability stays in-house, and what the RACI says about each. Read this before assuming a function is unowned.
last_updated: 2026-07-31
---

# External partners

Six whole functions at AC Brands run through outside organisations, and three more areas
run through individual contractors. That is nine external parties covering nine functions
for a team of nine. It is a reasonable shape at this size; it is also worth
writing down, because none of it was recorded anywhere in this repo before 2026-07-31
and two functions were showing as unowned purely because the partners were missing.

**Accountability never leaves the company.** Partners hold R: they do the work. A
stays with an employee on every row. `deliverables/verify.py` enforces this.

## Partner organisations

### Pedrero Regulatory: regulatory

External regulatory partner for Sweet July Skin. Amy Pedrero is the principal and
holds the binding regulatory calls; Heather Folkes and Teona Bebia are secondary.
Contact card and subject-line conventions live in
`.claude/skills/regulatory-manager/references/pedrero-contacts.md`.

All substantive regulatory review flows through them: IL approval, claim sign-off,
attestation review, SAE classification, recall classification. **Consult-only
internally**: no Asana access, no internal authority, no privileged read of PLM or
Outlook. Every engagement goes out over Outlook.

On the RACI they are consulted on 11 rows and responsible for none. That is not an
undervaluation, it is the direct consequence of the consult-only rule: Pedrero forms
every regulatory opinion, and the Operator performs every regulatory action, because
they cannot act inside our systems. Both halves are single-threaded. The engagement
letter governs scope, retainer, response windows and dispute resolution, and renews
annually.

### Ironclad Finance: finance

Dan Bender is the contact. Runs accounts payable, bookkeeping, payroll, month-end
close and management reporting, annual budget consolidation, and carries inventory
valuation and cost of goods into the books.

Accountability is split. **Danielle** answers for reporting-side work: month-end
close, management reporting, the annual budget. **Alvin** answers for cost-side work
(AP, vendor invoices, inventory valuation), because it flows out of purchasing,
receiving and the inventory ledger, and the vendor-invoice pipeline with its five
approval gates already sits in Operations.

There is no internal finance headcount, so continuity rests entirely on this
engagement.

### Calm HR: people and HR

PEO and co-employer. Claire Nahzi, Jarret Geist and D. Cavell are the working
contacts. Handles the employee handbook and HR policy, benefits administration and
payroll processing, onboarding and offboarding, employment compliance and
separations, and runs recruiting when a seat opens.

**Alvin is the liaison and accountable throughout; Danielle co-approves**. She is on
every Calm HR thread and every separation.

One half of offboarding stays internal and is not Calm HR's: Asana reassignment,
wiki contact state, and access deprovisioning across our own systems. The
departed-role-holder checklist in
`.claude/skills/asana-pd-manager/references/role-map.md` is that procedure, and it
exists because a stale role record broke collaborator resolution during a build.

### WITHIN: digital marketing

Digital marketing agency. Runs most of our digital marketing: paid media across Meta and
Google, and Klaviyo email flows and campaign sends. Quarterly business reviews; the most
recent was 20 July, where Q3 strategy confirmed Pineapple Punch as the primary driver.

**Soraya is accountable** for the Marketing function including both channels, and holds
the agency relationship. Alvin consulted on paid spend against margin floors. Danielle
consulted on campaign direction.

The landing hub listed Marketing as "Owned by TBD" until 2026-07-31.

### Teknologics: web development

Web development partner for sweetjuly.com and the Shopify storefront. A sizeable team; they
hold multiple seats in the Asana workspace.

**Danielle is accountable** for the website and web releases. **Nicole is the systems and
tech owner** for the web and digital stack. Erin and Ivy on visual design, Soraya
consulted on merchandising and content, Alvin informed.

Scope note: Nicole's systems-and-tech ownership is recorded here against web and digital.
The PLM write path, Asana configuration, landing-hub publish and the 23 scheduled Routines
still sit with Alvin. Widen if that was meant more broadly.

### Coastal Interactive: managed IT

Managed service provider for the higher-level IT and systems work: back-end
infrastructure, identity and endpoint management, equipment procurement and onboarding,
and asset lifecycle through to recovery on exit.

**Alvin is the liaison and accountable** for the IT function; Coastal Interactive is
responsible for the work. Nicole consulted.

Distinct from the web and digital stack, which sits with Danielle as accountable and
Nicole as systems and tech owner, with Teknologics developing. Coastal is the back end;
Teknologics is the storefront.

Onboarding and offboarding is split across two partners. Calm HR runs the employment
side, Coastal Interactive runs equipment and account provisioning, and Alvin is the
liaison to both. The internal systems half (Asana reassignment, wiki contact state) stays
with the departed-role-holder checklist.

## Individual contractors

| Who | Scope | Accountability held |
|---|---|---|
| **Perrine Calvet**, Milinyc Beauty | Technical guidance on R&D, Quality, Production and Regulatory requirements for product | 7 rows, all formulation: formula stage-gate, compatibility / stability / RIPT / PET, in-market stability testing, reformulation, PD-linked receipt, and the two margin rows that turn on formulation cost. Consult-only on process-shaped gates as of 2026-07-30. |
| **Erin Hover** | Creative Director and lead technical authority on packaging and artwork | 4 rows: creative direction, packaging development, artwork execution, label artwork archive. On creative direction she is both A and R. |
| **Jan Haeck** | Packaging Engineer, executes under Erin | 2 rows as R: packaging development and artwork execution. Holds no accountability. |

## What this means for continuity

Continuity across nine functions rests on engagements rather than on employment, and each
one is a renewal decision rather than a retention conversation. Engagement terms are
recorded for Pedrero only; the other eight need the same. Two specific
exposures, both on the RACI Gaps sheet:

Erin and Perrine each hold a row where they are both accountable and responsible with
no internal counterpart: creative direction and pre-launch stability respectively.
Nobody on staff can check that work or continue it. Neither the Operations Specialist
nor the PD Specialist job description covers creative or formulation authority, so the
two approved hires do not close this.

The Operator and Reg Lead gates are the same person, so on a regulatory filing the two
approvals that were designed to be independent both come to Alvin, and the opinion
they are approving comes from a partner who cannot act in our systems.

## Update protocol

1. Confirm the change with the operator.
2. Update this file and `last_updated`.
3. If the change affects who holds A or R, update `deliverables/raci_rows.py` and
   re-run `build_raci.py`, `build_html.py` and `verify.py`.
4. If the change touches regulatory, keep
   `.claude/skills/regulatory-manager/references/pedrero-contacts.md` in sync.
5. Log the decision in `decisions/log.md`.

## History

- **2026-07-31 (third pass)**: Added Coastal Interactive as the managed IT service
  provider. Nine external parties now. Also recorded that Perrine and Soraya are never
  blank on a Product Development row. See `decisions/log.md`.
- **2026-07-31 (second pass)**: Added WITHIN (digital marketing) and Teknologics (web
  development) after they surfaced from the AC Brands landing hub, which defines eleven
  functions with a named lead each and had Marketing reading "Owned by TBD." Eight
  external parties now, not six.
- **2026-07-31**: Created. Pedrero was documented inside the regulatory skill but
  Ironclad Finance and Calm HR appeared nowhere in the repo, which is why Finance and
  People & Admin were showing as unowned functions on the first RACI pass. Added the
  contractor table alongside them so the whole external surface reads in one place.
