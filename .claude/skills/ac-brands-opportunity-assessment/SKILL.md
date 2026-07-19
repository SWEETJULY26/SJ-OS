---
name: ac-brands-opportunity-assessment
description: >
  Pre-decision strategic analysis for AC Brands and its portfolio of brands.
  Use whenever someone brings a half-formed opportunity, founder instinct,
  or "should we enter this category" question that needs structured analysis
  before a decision can be made. Triggers on phrases like "should we enter
  [category]", "run market intel on [topic]", "what's the opportunity in
  [X]", "is [category] worth entering", "pressure-test this idea", "should
  AC Brands do [X]", or "Ayesha had an idea about [X]" when the ask is for
  analysis rather than execution. Operates at the AC Brands corporate level —
  works across SJS, Sweet July, and any future brands. Does NOT fire for
  execution work (PD briefs, supplier sourcing), existing-product margin
  questions, recurring competitive monitoring, or operational decisions —
  those route to the relevant operational skill instead.
---

<!--
WRITING STYLE — NO AI JARGON
This skill follows the AC Brands organization-wide writing rules. See the
full rules in the user's Claude system prompt under <organizationInstructions>.
Key constraints: no banned words (delve, leverage, utilize, etc.), no banned
openers ("In today's fast-paced world"), no banned transitions (furthermore,
moreover), no banned closings ("In conclusion"), no "It's not X — it's Y"
reframes, default to paragraphs over bullets, no bolded lead words on bullets,
no vibe emojis, em dashes preferred over hyphens. Write how a smart, specific
person talks to a colleague.
-->

# AC Brands Opportunity Assessment

Pre-decision strategic analysis for AC Brands. Takes a half-formed opportunity
— a founder instinct, a market signal, a "should we enter this category"
question — and produces a structured, decision-ready point of view that
integrates inputs from every relevant function.

The skill's defining function is **cross-functional synthesis**. No single
AC Brands function (PD, Ops, Brand, Margin, etc.) produces this kind of
output on its own. The skill's job is to be the integration layer.

---

## When to use this skill

**Triggers:**

- "Should we [enter / launch / build / acquire] [category / product / brand]"
- "What's the opportunity in [category]"
- "Run market intel on [topic]"
- "Is [category] worth entering"
- "Pressure-test this idea"
- "Should AC Brands do [X]"
- "Ayesha had an idea about [X]" — when the ask is for analysis, not execution
- Any time a founder instinct, market signal, or competitive move surfaces
  that warrants a structured assessment before a decision is made

**Does NOT trigger for:**

- Existing-product margin questions → route to `sjs-margin-architect` family
- Supplier or PD execution questions → route to `sjs-pd-system`
- Recurring competitive monitoring → route to `sjs-comp-intel`
- Operational decisions → route to `ac-brands-ops-system`
- Brand-architecture decisions for products already in development → future
  sibling skill (`ac-brands-brand-architecture`, not yet built)

---

## Scope and altitude

**Operates at:** AC Brands corporate level — works across SJS, Sweet July,
and any future brands.

**Decision-stage focus:** Pre-decision analysis only. Once a decision is made
to pursue an opportunity, handoff goes to whichever execution system owns it.

**Out of scope:** Execution work, operational decisions, margin pressure-tests
of existing SKUs, recurring competitive sweeps, brand-architecture decisions
for in-flight products.

---

## The 7-domain synthesis methodology

Every opportunity assessment integrates seven domains. The full methodology
— what to research in each domain, where to look, what good output looks
like, common traps — lives in `references/7-domain-methodology.md`. Read
that file at the start of any assessment.

The seven domains, walked in order:

1. **Consumer & Category Reality** — Is the demand real? Durable? Fad or
   structural shift?
2. **Competitive Reality** — Who's there? Where's the white space? How
   long is the window?
3. **PD Reality** — Can AC Brands actually make this? What's the supplier
   landscape? What's the timeline?
4. **Operations Reality** — What does this do to supply chain, 3PL, retail?
   Are MOQs realistic?
5. **Margin Reality** — What are the unit economics? Does it clear the
   relevant brand's margin framework?
6. **Brand Reality** — Does this strengthen or muddy the host brand? What's
   the architecture question?
7. **Regulatory Reality** — What's the regulatory regime? What can you say
   on the label? In marketing?

The output integrates these seven into a single point of view. Not seven
separate sections — one synthesized argument that names tensions across
domains and resolves them.

> **Future refactor note:** This 7-domain methodology is the connective
> tissue across what will eventually be a multi-skill AC Brands strategy
> system. When the second strategy skill is built (e.g., `ac-brands-brand-architecture`),
> this methodology must be extracted into a shared layer — either the
> future `ac-brands-strategy-new-ventures` master router or a standalone
> reference doc — so it's reused, not duplicated.

---

## Workflow — the 4 phases

### Phase 1: Frame the question

Before any research, confirm what's actually being asked. Common pattern:
the surface question ("should we do hydration") is not the real question
("what's the strongest brand-architecture path for this opportunity").
Name the surface question, the underlying question, and any assumptions
baked in.

For quick assessments, this can be implicit. For high-stakes assessments,
explicitly check in with the user before proceeding.

### Phase 2: 7-domain synthesis

Walk through the 7 domains in sequence, doing real research at each step.
Web search and web fetch are the primary tools. Research depth scales to
question complexity — a quick gut-check might do 3 to 5 searches per domain,
a high-stakes assessment 10 to 15.

Reference `references/7-domain-methodology.md` for what to research in each
domain.

This phase is internal — the synthesis is forming, not yet shared with
the user.

### Phase 3: Form a point of view

Form a clear, defensible position on:

- Is the opportunity real?
- What are the realistic options for pursuing it (typically 2 to 4
  architectural paths)?
- What are the tradeoffs of each option?
- What's the recommendation?
- What are the gating questions that need answers before any decision?
- What's the next 30 days of work?

Be opinionated. Hedging and "it depends" answers are explicitly disallowed
unless the question genuinely cannot be answered without more information —
in which case name exactly what's missing.

### Phase 4: Deliver

Default output is conversational — written analysis in chat, structured by
section, with embedded data and citations from web research.

Use the conversational output structure in
`references/output-structure-template.md`.

Escalate to a branded deliverable (Canva deck, PDF, doc) when:

- The output is going to Ayesha or Danielle directly
- The user explicitly asks for a deck, doc, or PDF
- The analysis is part of a board or investor conversation

When escalating, follow the same brand guidelines used by `sjs-status-reporter`,
selecting the appropriate brand kit (AC Brands corporate, SJS, or Sweet July)
based on scope.

---

## Inputs and dependencies

**Primary input:** A strategic question from the user, in any form.

**Light-touch references** — name and pull insight from these, but do not
actively invoke them:

- `sjs-pd-system` and child skills — for current-state PD context when
  SJS is the host brand
- `ac-brands-ops-system` and child skills — for current-state Ops context
- `sjs-margin-architect` family — for framework rules when SJS is the host
- `sjs-comp-intel` and `sjs-retail-intel` — for current competitive context
- Web search and web fetch — primary research tools
- Conversation search and recent chats — for past context the user may be
  referencing

If deep data from another skill is needed, name the gap and ask the user
to bring it in. Do not actively call other skills.

---

## Quality bar

An opportunity assessment is high-quality when:

- The seven domains are integrated, not just listed in sequence
- The recommendation is opinionated and defensible
- The tradeoffs are named honestly, including the ones that argue against
  the founder's instinct
- The brand-architecture question is surfaced explicitly (line extension
  vs. sister brand vs. new brand)
- The next 30 days of work is specific, actionable, and prioritized
- The writing follows the AC Brands anti-AI-jargon rules and reads like
  a smart human wrote it
- Real data and citations are used wherever available

An assessment fails when it hedges, treats founder instinct as a settled
premise, produces a list of "considerations" instead of a recommendation,
dodges the hard structural questions (brand architecture, regulatory, real
MOQs, real margins), or reads like consulting boilerplate.

---

## Reference files

- `references/7-domain-methodology.md` — Deep methodology for each of the
  seven domains. Read at the start of any assessment.
- `references/output-structure-template.md` — The 5-part conversational
  output structure with detailed guidance on each section.
- `references/hydration-analysis-example.md` — The canonical worked example.
  The ingestible hydration assessment for SJS / AC Brands, with annotations
  explaining why it's structured the way it is. Reference when needing to
  see what a finished assessment looks like.

---

## Backward-update pass

**Status: N/A — this is the first skill in the AC Brands strategy system.**

When the second strategy skill is built (likely `ac-brands-brand-architecture`),
return here and complete this section as a real checklist. The minimum
updates this skill will need at that point:

- Extract the 7-domain synthesis methodology to a shared layer
- Update this skill to reference the shared layer instead of containing
  the methodology inline
- Add a "handoff to [new sibling]" section
- Update description and trigger fields to ensure no ambiguity with
  the new sibling
- Update any cross-references and file paths

Per the user's standing instruction, every new skill in a system triggers
a backward-update pass on its siblings. This skill must be updated as
part of any future strategy-skill build.
