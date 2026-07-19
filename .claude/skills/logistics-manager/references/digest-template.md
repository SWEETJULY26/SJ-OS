# Weekly logistics digest template

The Monday 9am digest. On-demand on "run the logistics digest" or "Monday
logistics" or "logistics one-pager." Pulls the live shipment view and hands a
structured YAML brief to sjs-status-reporter, which wraps it in SJS brand and
publishes the one-pager.

You don't write brand copy here. You produce the data shape; the reporter
handles the brand layer.

---

## Inputs (read-only)

Pull from PLM Supabase:

- `shipments` rows where `current_status` is open (not delivered/closed) — split
  by `lane_type`
- `shipments` rows where `customs_status` in ('in_clearance', 'hold',
  'examination')
- `shipments` rows where `exception_flags` jsonb has any active flag
- Aging escalation tasks from the dedicated Sweet July Skin Logistics Asana
  project, `Outbound — Escalations` section
- Retailer compliance posture: any `shipments.exception_flags` with rule
  violations from the past 7 days
- Last week's digest (the parent task in Asana `Weekly Digest` section) for
  carryover items

---

## Output shape

YAML brief, hand to sjs-status-reporter:

```yaml
period: "Week of YYYY-MM-DD"
generated_at: "YYYY-MM-DD HH:MM PT"

inbound_fg:
  open_count: <int>
  on_track: <int>
  eta_shifted: <int>
  exception: <int>
  highlights:
    - shipment_id: <id>
      vendor: <filler name>
      eta: <date>
      status: <plain language>
      flag: <eta_shift|customs_hold|delivery_overdue|none>

inbound_components:
  open_count: <int>
  on_track: <int>
  eta_shifted: <int>
  exception: <int>
  highlights:
    - shipment_id: <id>
      vendor: <component vendor>
      eta: <date>
      status: <plain language>
      flag: <eta_shift|customs_hold|customs_exam|delivery_overdue|none>

customs_watch:
  in_clearance: <int>
  on_hold: <int>
  on_exam: <int>
  detail:
    - shipment_id: <id>
      vendor: <vendor name>
      customs_status: <hold|examination|in_clearance>
      days_in_status: <int>
      next_action: <plain language>

outbound_retailer:
  open_count: <int>
  ulta_open: <int>
  amazon_open: <int>
  upcoming_asn_drafts: <int>
  compliance_posture:
    ulta:
      passed_7d: <int>
      failed_7d: <int>
      trend: <improving|steady|degrading>
    amazon:
      passed_7d: <int>
      failed_7d: <int>
      trend: <improving|steady|degrading>

escalations:
  open_count: <int>
  by_reason:
    ria: <int>
    label_fail: <int>
    lost: <int>
    address_bounce: <int>
    claim: <int>
    other: <int>
  aging:
    over_48h: <int>
    over_7d: <int>
  patterns_flagged: <int>

risk_callouts:
  - <plain language risk callout, one line each>

digest_actions_for_operations:
  - <one line each — what needs Operations attention this week>
```

---

## Authoring rules

**No AI jargon.** No "leverage," no "comprehensive," no "ecosystem," no
"landscape." Plain English.

**Plain language for status.** "Container at LA/LB awaiting customs release"
beats "in clearance phase, awaiting clearance." Write like a colleague briefing
another colleague.

**Highlights are exception-first.** If a lane has 8 on-track shipments and 1
ETA shift, only surface the ETA shift in highlights. Healthy lanes don't need
shipment-by-shipment commentary.

**Risk callouts are forward-looking.** What might break next week? Customs
clearance window narrowing. Compliance posture degrading at Ulta. Aging
escalations approaching the 7-day mark. Two lanes converging on the same
container.

**Actions for Operations.** What needs a decision or send-off this week —
typically 3 to 5 lines. ASN drafts ready to send, broker outreach to approve,
escalation threads needing sign-off, routing guide rev to ratify.

---

## Cadence and triggers

Scheduled: Monday 9am Pacific. Tunable via `settings.lm_digest_day` and
`settings.lm_digest_time`.

On-demand triggers:

- "run the logistics digest"
- "Monday logistics"
- "what's open in logistics"
- "logistics one-pager"
- "logistics health"

Off-cycle digest runs use the same template; the period field reflects the
ad-hoc window (e.g., "Generated 2026-04-30 — last 7 days").

---

## Handoff to sjs-status-reporter

Pass the YAML brief to sjs-status-reporter with framing intent =
`weekly_logistics_digest`. The reporter wraps in SJS brand and publishes per its
output convention. The digest also lands as a parent task in the Asana `Weekly
Digest` section with the YAML attached for reference and the published one-
pager linked.

If sjs-status-reporter is unavailable or Operations asks for the raw shape
("just give me the data"), return the YAML inline.

---

## When to swap to ops-status-reporter

When v6 (quality-manager) and v7 (sjs-ops-system) land, the call site
should swap to `ops-status-reporter` if it exists and is the canonical Ops
reporter at that point. Until then, sjs-status-reporter is the target.
