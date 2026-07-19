# Root Cause Analysis Tools

Mirrors SKN-OPS-001 Appendix C. The SOP names two RCA tools (Fishbone, 5 Whys) without specifying when to use which. This file scaffolds both and gives the skill a default selection rule that the operator can override.

The skill *prompts*, the team *answers*. RCA artifacts are evidence — they must show the actual reasoning, not a sanitized summary. Capture the working notes verbatim as a comment thread on the CAPA task; only the final root cause statement gets a structured custom field.

---

## Default tool selection

| Situation | Tool | Why |
|---|---|---|
| Single event, single chain of causation | 5 Whys | Quick, sequential, gets to a likely root in 4–6 prompts |
| Systemic pattern, multiple contributing factors, or the "why" branches | Fishbone | Forces breadth across categories before depth |
| Recurrence of a previously closed CAPA | Both — start with Fishbone for breadth, then 5 Whys on the strongest branch | The first CAPA missed something; need both lenses |

Operator can override the default at team formation (Job 3). RCA tool used gets captured in the CAPA record.

---

## 5 Whys

A sequential prompt structure. Each "why" digs one layer deeper. Stop when the answer becomes a process or system property the team can act on, not a person.

### Prompt structure

**Statement of the non-conformance.** One sentence. What happened, when, to what.

**Why 1.** Why did that happen?
**Why 2.** Why did *that* happen?
**Why 3.** Why did *that* happen?
**Why 4.** Why did *that* happen?
**Why 5.** Why did *that* happen?

Five is a guideline. If a confident root cause shows up at Why 3, stop there and document. If Why 5 still reads like a symptom, keep going. Don't pad.

### Stopping rules

A good stopping point is one where:
- The answer points to a process, system, or design choice (not a person).
- The answer is something the team can act on in a corrective or preventive action.
- A reasonable third party reading the chain can follow the logic without needing more context.

A bad stopping point — keep going if you see these:
- "Human error" — almost always means the system allowed the error to happen.
- "We were rushed" — the rush is a symptom; what caused the rush?
- "We forgot" — what was missing from the process that made forgetting possible?
- A name — root causes are systemic, not personal.

### Worked example (do not paste into actual CAPAs)

**Statement:** Lot 26-04 of Pava Toner shipped to OC3PL with the wrong batch label, discovered on incoming inspection.

**Why 1?** The label printed for Lot 26-04 was the template from Lot 26-03 — the batch number didn't update.
**Why 2?** The label generation step in the packaging run sheet pulls the batch number from a free-text field, not from the batch record.
**Why 3?** The free-text field exists because the batch record schema doesn't expose batch number to the label-generation tool.
**Why 4?** The label-generation tool was set up before the batch record schema was finalized, and was never updated to read the structured field.
**Stop.** Root cause: label-generation tool reads from an unmaintained free-text field instead of the structured batch number field. Corrective: route label generation off the structured field. Preventive: audit other tools using free-text references that should be structured.

---

## Fishbone (Ishikawa)

Six standard categories. The skill prompts each category for contributing factors, then the team identifies the strongest branch and may follow up with 5 Whys on it.

### The six categories

**Manpower (People).** Who was involved? What training did they have? Were there handoffs that lost context? Was the right authority level present?

**Method (Process).** What procedure was followed? Was the procedure documented? Was it the right procedure for this situation? Were steps skipped or modified?

**Machine (Equipment).** What tools, software, or equipment were involved? Was anything calibrated, configured, or version-locked incorrectly? Did anything fail or behave unexpectedly?

**Material.** What inputs (raw materials, components, data) went into the process? Were they within spec? Were they from the expected source? Were they handled correctly upstream?

**Measurement.** How was the process or output measured? Was the measurement accurate? Was the right thing being measured? Did anyone act on a measurement that turned out to be wrong?

**Environment.** What context surrounded the event? Time pressure, physical conditions, organizational priority shifts, communication patterns, external dependencies?

### Prompt structure

For each of the six categories, the skill asks: "What in [category] contributed to this non-conformance?"

The team answers with one or more contributing factors per category. Empty categories are fine and informative — capture "no contribution" with a brief reason.

After all six are populated, the team identifies:
- **Strongest branch** — the category with the most contributing factors or the most direct line to the non-conformance
- **Cross-category links** — factors that show up across multiple categories often signal a deeper systemic issue

### Worked example (do not paste into actual CAPAs)

**Statement:** Three vendor receipts of FOA-ROSE component this quarter failed incoming inspection for moisture content, all from the same vendor.

| Category | Contributing factors |
|---|---|
| Manpower | Receiving team rotated mid-quarter; new staff didn't know moisture spec was unusual for this material |
| Method | Incoming inspection SOP doesn't specify moisture testing for botanicals — only visual + COA review |
| Machine | Moisture analyzer is shared with lab; not always available at receiving |
| Material | Vendor sources from a new farm this quarter; growing region has higher humidity |
| Measurement | COA from vendor reports moisture but uses a different test method; incoming inspection didn't catch the discrepancy until the third receipt |
| Environment | Q1 receiving volume up 40% vs. Q4; less time per receipt |

**Strongest branch:** Method + Measurement — the SOP doesn't require independent moisture verification, and the COA discrepancy went unnoticed.

**Cross-category link:** Material change (new farm) + Method gap (no spec verification) is the recurring failure pattern.

**Follow-up 5 Whys** on the Method branch:

- Why didn't the SOP require moisture verification? Because it was written for previously stable materials.
- Why wasn't it updated when the vendor changed sourcing? Because there's no process to trigger SOP review on vendor sourcing changes.
- Why is there no such process? Because vendor sourcing changes don't reliably propagate from purchasing to quality.

Root cause: vendor sourcing changes don't trigger a quality SOP review. Preventive action: build the trigger.

---

## RCA artifact format

The skill captures RCA work as a comment thread on the CAPA task. Format:

```
**RCA — CAPA-YYYY-NNN — [Tool used] — [Date]**

Team: [names + roles]

[Tool walk verbatim — every prompt + answer]

**Root cause statement:** [one sentence, attributable to a process/system/design choice]

**Strongest branch / chain:** [for Fishbone: which category and why; for 5 Whys: implicit]

**Cross-references:** [links to source NCR, related CAPAs, batch records, audit findings]
```

The root cause statement also goes in the `Root Cause Statement` custom field on the task. The Fishbone category (if used) goes in `Root Cause Category`. Both are required before the CAPA can advance to Action Plan (Job 4).

---

## When neither tool fits

Some non-conformances don't yield to 5 Whys or Fishbone — software bugs, data corruption, novel chemical interactions. The SOP doesn't address this. Skill default: capture what the team *did* do (timeline of investigation, hypotheses tested, evidence considered) and document the root cause statement directly. Flag the case in the CAPA record so future RCA tooling can be considered for §7 revision.
