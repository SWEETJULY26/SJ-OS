# International DTC shipment record — staged write

Use this form when staging a row in `shipments` for the international outbound
DTC lane (`lane_type=international_outbound_dtc`). This is the cross-border
consumer parcel — Canada today, EU/UK/AU when those markets land. The failure
mode is regulatory and customs declarations, so this form captures fields
that the standard `shipment-record.md` form does not — destination country,
declared HS, declared value, DDP/DDU posture, partner of record, regulatory
filing reference.

plm-assistant commits after Operations approves. Reference
`references/international-dtc.md` for per-market posture and the Canada
playbook before staging.

Writing follows the AC Brands writing style rules in the organization-wide
Claude instructions.

---

## Form fields

```yaml
# --- Identity ---
lane_type: international_outbound_dtc
outbound_order_id: <FK to outbound_orders.id>
batch_id: <FK to batches.id, null if not yet assigned at fulfillment>

# --- Destination ---
destination_country: <ISO 3166-1 alpha-2 — CA, GB, FR, DE, AU, etc.>
destination_postal_region: <free text region or postal prefix, not full address>

# --- Declaration ---
declared_hts: <HTS code per declaration — see international-dtc.md sample codes>
declared_value_usd: <decimal USD>
declared_description: <plain English product description for customs>

# --- Posture and partners ---
ddp_or_ddu: <ddp|ddu>
ddu_exception_reason: <free text, required if ddp_or_ddu=ddu>
cross_border_partner: <FK to vendors.id where category=cross_border_partner>
customs_broker_id: <FK to vendors.id where category=customs_broker, null if partner-included>

# --- Regulatory ---
regulatory_filing_ref: <FK to regulatory record — CNF id for Canada, CPNP id for EU, etc. Null if market does not require>
regulatory_filing_status: <on_file|pending|expired|not_required>
labeling_compliance_ref: <FK to labeling check artifact in PLM, or SharePoint URL to the proof>

# --- Carrier and tracking ---
carrier: <cross-border partner forwarding carrier name>
tracking_number: <string, may be null at order release>

# --- Schedule ---
ship_date: <YYYY-MM-DD, null if not yet shipped>
eta: <YYYY-MM-DD>
eta_revised_at: <timestamp of last ETA shift, null if no shift>
delivery_date: <YYYY-MM-DD, null until delivered>

# --- Status ---
current_status: <pre_ship|in_transit|in_clearance|delivered|exception|closed>
customs_status: <not_applicable|in_clearance|cleared|hold|refused|returned|abandoned>

# --- Cost ---
duty_paid: <decimal USD, null until partner invoices>
broker_fee: <decimal USD, null until invoiced>
parcel_forwarding_fee: <decimal USD>
landed_cost_line: <decimal USD, computed sum once costs land>

# --- Exception flags ---
exception_flags: <jsonb array — see flag taxonomy below>

# --- Source and audit ---
source_email_id: <Outlook message ID via outlook-plm-bridge, null if manual>
source_oc3pl_export_id: <reference to the Logiwa export row that surfaced the order>
notes: <free text — short, plain language>
```

---

## Exception flag taxonomy — additions for this lane

In addition to the flags from `forms/shipment-record.md`, the international
DTC lane uses these:

- `customs_refused` — destination customs refused the parcel (CBSA, EU customs, etc.)
- `customs_returned` — refused parcel returned to origin
- `customs_abandoned` — refused parcel abandoned by customs (cost write-off)
- `bilingual_label_fail` — label proof failed bilingual check (Canada) or
  language requirement check (EU/UK/AU)
- `ddu_duty_complaint` — customer complaint on duty charge from carrier (DDU lane only)
- `cnf_filing_pending` — Canada parcel staged but CNF not yet on file — blocks ship
- `cpnp_filing_pending` — EU parcel staged but CPNP not yet on file — blocks ship
- `hotlist_review_pending` — Health Canada Hotlist revision triggered review
  on this SKU — pause Canada DTC until cleared
- `partner_integration_break` — cross-border partner Shopify integration
  failed; landed cost not injected at checkout

Each flag is an object: `{flag: <name>, raised_at: <ts>, resolved_at: <ts|null>, note: <text>}`.

---

## Required minimums

Before staging the row, confirm: `lane_type`, `outbound_order_id`,
`destination_country`, `declared_hts`, `declared_value_usd`, `ddp_or_ddu`,
`cross_border_partner`, `regulatory_filing_status`, `current_status`.

If `regulatory_filing_status` is anything other than `on_file` or
`not_required`, the parcel does not ship — raise the corresponding
`*_filing_pending` exception flag and surface to Operations before approval.

If `ddp_or_ddu=ddu`, `ddu_exception_reason` is required. The default
posture is DDP per the per-market matrix in `references/international-dtc.md`.

---

## Confirmation flow

1. Stage the YAML above as a Markdown comment on the Asana parent task in
   the correct logistics section (the international DTC parcels live under
   `Outbound — Escalations` until a dedicated section is added)
2. Surface to Operations with the order summary in plain language,
   highlighting destination country, DDP/DDU posture, and regulatory
   filing status
3. On approval, plm-assistant commits the row
4. The Asana parent task is created or updated with the shipment_id linked
5. Source email or OC3PL export reference logged in the audit fields

If a refusal lands after the row commits, update `customs_status`,
raise the `customs_refused` exception flag, and route the consumer
complaint thread (if any) to complaint-and-event-handler.
