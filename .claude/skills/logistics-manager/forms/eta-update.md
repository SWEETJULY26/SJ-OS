# ETA update — staged write

Use this form when an existing shipment's ETA shifts. Most common signal: a
carrier or freight forwarder email saying the container or truck is delayed.
The Outlook bridges flag these; the skill stages the update.

ETA shifts ≥3 days raise an exception flag automatically (configurable via
`settings.lm_eta_shift_threshold_days`). Smaller shifts are logged silently.

---

## Form fields

```yaml
shipment_id: <FK to shipments.id>
prior_eta: <YYYY-MM-DD>
new_eta: <YYYY-MM-DD>
shift_days: <int, computed (new_eta - prior_eta)>
reason: <port_congestion|weather|customs_delay|carrier_capacity|vendor_delay|other>
reason_detail: <free text, one sentence>
source_email_id: <Outlook message ID>
exception_flag_to_raise: <eta_shift_3d|eta_shift_7d|none>
downstream_impacts:
  - <plain language — affected reorder, batch, retailer commitment>
```

---

## Downstream surfacing rules

When the ETA shifts ≥3 days on an inbound FG or component lane:

1. Surface to purchasing-manager so the next reorder timing can adjust
2. Surface to supply-demand-planner if the delay creates a component shortfall
   against the active S&OP plan
3. Update the Asana parent task with the new ETA and the reason
4. Add the exception flag to the shipment row's `exception_flags` jsonb

When the ETA shifts ≥3 days on an outbound retailer lane:

1. If the shift pushes ship outside Ulta or Amazon's required ship window,
   surface as a routing-request issue requiring outreach to the retailer
2. Recompute the ASN due-by timing
3. Update the Asana parent task

---

## Confirmation flow

1. Stage the YAML on the Asana parent task as a comment
2. Surface to Operations with the prior → new ETA and the impact in one sentence
3. On approval, plm-assistant updates `shipments.eta`, `eta_revised_at`, and
   appends to `exception_flags` if applicable
4. Downstream skills (purchasing-manager, supply-demand-planner) get a comment
   on their relevant tasks if the shift propagates

---

## When ETA shifts repeatedly

If a single shipment racks up three or more ETA shifts in its life cycle, that
pattern matters for the vendor scorecard. Surface to purchasing-manager at the
third shift so the vendor performance review captures the pattern.
