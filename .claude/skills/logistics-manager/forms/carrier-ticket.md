# Carrier escalation ticket — staged write

Use this form when oc3pl-order-manager hands off a carrier issue (RIA, label
fail, lost shipment, address bounce, claim). The form opens the parent task
in the Asana `Outbound — Escalations` section and stages the first carrier
outreach.

Carrier-specific procedure lives in `references/escalation-playbook.md`. This
form captures the fields; the playbook tells you how to run each carrier's
process.

---

## Form fields

```yaml
shipment_id: <FK to shipments.id, may be a fresh shipment row for DTC>
escalation_reason: <ria|label_fail|lost|address_bounce|damage|claim|other>
carrier: <UPS|FedEx|DHL|other>
tracking_number: <string>

# --- Underlying order context ---
order_id: <DTC order ID from Shopify or retailer order ID>
ship_date: <YYYY-MM-DD>
customer: <free text — name, region only; PII minimums>
declared_value: <decimal USD>
sku_list: <array of SJS SKUs in the order>

# --- First action taken ---
first_action: <opened_tracer|filed_claim|requested_address|awaiting_evidence|other>
first_action_at: <timestamp>
carrier_reference: <carrier's tracer or claim reference number, null if pending>

# --- Reship decision ---
reship_decision: <reship_now|wait_for_resolution|pending_evidence|n/a>
reship_order_id: <new Shopify order ID if reshipped, null otherwise>

# --- SLA timing ---
sla_target: <YYYY-MM-DD HH:MM, computed from carrier-specific SLA>
sla_breach_risk: <green|yellow|red>

# --- Pattern flag ---
similar_escalations_7d: <int — count of similar escalations in past 7 days>
pattern_flag: <true|false, true when similar_escalations_7d >= 3>

notes: <free text — short timeline of what's happened so far>
```

---

## Pattern recognition

When `similar_escalations_7d` reaches 3 (UPS damage on a single SKU, address
bounces from a Shopify segment, label fails on a single OC3PL run), the skill
flips `pattern_flag: true` and:

1. Opens a parent escalation task tagged `pattern_flag` separate from the
   individual cases
2. Names the pattern (carrier + reason + common SKU/segment) in the parent
3. Surfaces to Operations for a decision on whether to engage the carrier at
   the account level rather than ticket-by-ticket

---

## Reship rule

Default: reship the customer order through oc3pl-order-manager promptly when
loss or damage is clear. Treat the original ship cost as a write-off until
the carrier claim resolves. Do not wait for claim payout to keep the customer
whole.

The reship decision is the human's call, not the skill's. The skill stages
the recommendation; Operations or Order Ops approves; oc3pl-order-manager
runs the reship.

---

## Confirmation flow

1. Stage the YAML on the Asana parent task in `Outbound — Escalations`
2. Set custom field `escalation_reason` to the matching enum
3. Surface to Operations or Order Ops with the issue, the recommended action,
   and the SLA target
4. On approval, the carrier outreach goes (email to UPS tracer service, claim
   filed at fedex.com/claims, etc. per playbook)
5. Update the Asana task every 48 hours during active escalation
6. Close back to oc3pl-order-manager when resolved with a one-line summary
   (resolved by reship, claim paid, customer satisfied, etc.)

---

## SLA computation

SLA target is computed from `escalation_reason` and carrier:

- Lost shipment trace start: within 24h of expected delivery
- Damage claim file: within 5 business days of customer report
- Address bounce reship: within 24h of corrected address
- Other: 48h to first carrier action by default

Tunable via `settings.lm_escalation_sla_*`. Yellow at 80% of SLA window;
red at SLA breach.
