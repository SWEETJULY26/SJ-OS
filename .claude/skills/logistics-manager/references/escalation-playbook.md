# Carrier escalation playbook

When oc3pl-order-manager hands off a carrier issue, you run the escalation. The
playbook is per-carrier because each one has a different claim portal, evidence
requirement, and turnaround.

For every escalation:

1. Open a parent task in the Asana `Outbound — Escalations` section
2. Set custom field `escalation_reason` (RIA / Label / Lost / Address / Claim /
   Other)
3. Pull the underlying order info from oc3pl-order-manager (order ID, ship date,
   tracking number, carrier, customer, value)
4. Run the carrier-specific path below
5. Track the resolution thread; close back to order-manager when resolved

Document the timeline in the Asana task — every email, every status change.
Patterns matter for vendor scorecards over time.

---

## UPS

### Lost shipment

1. Wait 24 hours past expected delivery. UPS sometimes delivers late.
2. Open a tracer at ups.com/lostpackage with the tracking number, ship date,
   shipper account, declared value
3. UPS investigation runs 8 business days for ground, 5 for air
4. If declared not delivered, file a claim at ups.com/claims with proof of
   value (commercial invoice or DTC order receipt) and proof of damage if
   applicable
5. Reship the customer order through oc3pl-order-manager once the tracer
   confirms loss (don't wait for claim payout)

Tracer email pattern: notifications come from `tracerservices@ups.com`. Save
the tracer reference number in the Asana task.

### Damage

1. Customer sends a photo and description through DTC support → oc3pl-order-
   manager → escalation
2. File at ups.com/claims with photos
3. Reship if damage is clear; UPS reimburses the order value if claim approved

### Address bounce

1. UPS attempts → bounces back to OC3PL
2. Reach out to customer for corrected address through oc3pl-order-manager
3. OC3PL re-sends with corrected address; original UPS leg charged back
4. Document the bounce in shipment exception_flags

---

## FedEx

### Lost shipment

1. Wait 24 hours past expected delivery
2. Open a trace at fedex.com/customer-support with tracking number
3. FedEx investigation runs 5–10 business days
4. If declared lost, file a claim at fedex.com/claims with proof of value
5. Reship via oc3pl-order-manager once trace confirms loss

### Damage

1. Customer evidence (photos)
2. File claim within 60 days of ship date
3. Reship promptly

### Address bounce

Similar to UPS. Reach out, correct, reship.

---

## DHL (international DTC, occasional)

### Lost shipment

1. Open tracer at dhl.com customer service with tracking number
2. International tracers run 10–15 business days
3. Claims filed through DHL Global Forwarding portal if international, DHL
   eCommerce portal if domestic injection

DHL is slower than UPS or FedEx. Set customer expectations accordingly.

---

## Freight forwarder (Flexport — inbound ocean/air)

This is the inbound side. Container delays, port congestion, customs holds.

### Container delay

1. Flexport sends weekly tracking updates (`@flexport.com` email)
2. If ETA shifts ≥3 days, the shipment row's `eta_revised_at` updates and an
   exception flag fires
3. Surface to purchasing-manager so they can adjust the next reorder timing
4. Surface to supply-demand-planner if the delay creates a component shortfall

### Port congestion

Same pattern as container delay. Flexport flags when LA/LB or another port has
known congestion; ETA expands.

### Damage in transit

Less common but documented. File with Flexport's claims team within 30 days of
delivery. Cargo insurance covers value if filed in time.

---

## Common patterns across carriers

### Reship vs. wait-for-claim

Reship promptly to keep the customer happy. Don't wait for the claim payout —
treat the original ship cost as a write-off until the claim resolves.

### Class-action shape

If three or more escalations in a week point to a single failure mode (label
fail at OC3PL, address bounces from a Shopify segment, UPS damage on a single
SKU), surface as a pattern issue, not a one-off. Open a parent task in
escalations with the pattern noted; tag relevant SKUs and channels.

### Documentation cadence

Update the Asana task every 48 hours during an active escalation. Stale
escalation threads waste time and lose context. Close immediately on
resolution; don't let resolved threads sit open.

---

## SLAs

Tunable defaults in `settings.lm_escalation_sla_*`:

- Lost shipment trace start: within 24 hours of expected delivery
- Damage claim file: within 5 business days of customer report
- Address bounce reship: within 24 hours of corrected address
- Pattern recognition flag: 3+ similar escalations in 7 rolling days

These are starting values. Tune from running data.
