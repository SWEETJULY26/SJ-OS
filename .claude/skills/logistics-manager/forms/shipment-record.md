# Shipment record — staged write

Use this form when staging a new row in `shipments`. Every field below maps
directly to a column in the table. plm-assistant commits after Operations
approves.

The same template covers four lane types — FG inbound, component inbound,
retailer outbound, DTC escalation. Fill what's known; leave nulls where the
data hasn't landed yet (ETA, customs, costs typically come in waves).

The international outbound DTC lane (`lane_type=international_outbound_dtc`)
has its own dedicated form — see `forms/international-dtc-shipment.md`.
That lane carries declaration, DDP/DDU posture, and regulatory filing
fields that do not apply to the four lanes covered here.

---

## Form fields

```yaml
# --- Identity ---
lane_type: <fg_inbound|component_inbound|retailer_outbound|dtc_escalation|international_outbound_dtc>
po_id: <FK to purchase_orders.id, null if outbound retailer or DTC escalation>
outbound_order_id: <FK to outbound_orders.id, null if inbound or DTC>
batch_id: <FK to batches.id, null if not yet assigned>

# --- Carrier and tracking ---
carrier: <UPS|FedEx|DHL|Flexport|LTL provider name|Other>
tracking_number: <string, may be null at PO-ships time>
asn_number: <string, retailer outbound only>

# --- Origin and destination ---
origin: <vendor location or filler site, free text>
destination: <OC3PL|Ulta DC|Amazon FC|customer ZIP|other>

# --- Schedule ---
ship_date: <YYYY-MM-DD, null if not yet shipped>
eta: <YYYY-MM-DD, vendor or carrier estimate>
eta_revised_at: <timestamp of last ETA shift, null if no shift>
receipt_date: <YYYY-MM-DD, null until landed>

# --- Status ---
current_status: <pre_ship|in_transit|at_port|in_clearance|delivered|exception|closed>
customs_status: <not_applicable|in_clearance|cleared|hold|examination>
broker: <Flexport|other broker name|null>

# --- Customs and landed cost ---
hts_code_ref: <single HTS code or "see multi_hts" if multiple>
multi_hts: <jsonb array of {code, description, qty}, optional>
duty_paid: <decimal USD, null until customs clears>
brokerage_fee: <decimal USD, null until invoiced>
freight_paid: <decimal USD, null until invoiced>
landed_cost_line: <decimal USD, computed sum once all costs land>

# --- Exception flags ---
exception_flags: <jsonb array — see flag taxonomy below>

# --- Source and audit ---
source_email_id: <Outlook message ID via outlook-plm-bridge, null if manual>
source_meeting_id: <Fireflies transcript ID, null if not from a meeting>
notes: <free text — short, plain language>
```

---

## Exception flag taxonomy

Active flags accepted in `exception_flags` jsonb:

- `eta_shift_3d` — ETA moved ≥3 days from prior estimate
- `eta_shift_7d` — ETA moved ≥7 days
- `customs_hold` — customs status is `hold`
- `customs_exam` — customs status is `examination`
- `delivery_overdue` — past ETA without receipt confirmation
- `compliance_fail` — retailer compliance check failed (outbound only)
- `damage_in_transit` — carrier or receiver flagged damage
- `lost` — carrier tracer declared loss
- `pattern_flag` — part of a 3+ pattern surfaced by escalation playbook

Each flag is an object: `{flag: <name>, raised_at: <ts>, resolved_at: <ts|null>, note: <text>}`.

---

## Required minimums by lane

**FG inbound and component inbound.** Need at minimum: `lane_type`, `po_id`,
`carrier`, `origin`, `destination`, `ship_date` or `eta`, `current_status`. The
rest fills in over the lane's life cycle.

**Retailer outbound.** Need at minimum: `lane_type`, `outbound_order_id`,
`carrier`, `destination` (DC name), `ship_date`, `current_status`. ASN number
populates when the ASN draft commits.

**DTC escalation.** Need at minimum: `lane_type`, `carrier`, `tracking_number`,
`origin` (OC3PL), `destination` (customer ZIP region — not full address), and
the escalation parent task in Asana (link in `notes`).

**International outbound DTC.** Use `forms/international-dtc-shipment.md`
instead — that lane needs declaration, DDP/DDU, partner of record, and
regulatory filing fields beyond what this form covers.

---

## Confirmation flow

1. Stage the YAML above as a Markdown comment on the Asana parent task in the
   correct section
2. Surface to Operations with the lane summary in plain language
3. On approval, plm-assistant commits the row
4. The Asana parent task is created or updated with the shipment_id linked
5. Source email or meeting reference logged in the audit fields
