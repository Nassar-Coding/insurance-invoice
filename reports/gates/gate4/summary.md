# Gate 4 — contract rules

## Exit criteria (development partition)

| Criterion | Target | Result |
|---|---|---|
| Cumulative detection | ≥ 35 of 42 | **PASS — 40 of 42** |
| False positives on the 580 clean development invoices | 0 | **PASS — 0** |
| Decoy-proxy flags | 0 | **PASS — 0 of 184** |
| `daily_cap_exceeded` | 2 of 2 | **PASS — 2 of 2** |
| `exclusion_window_violation` | ≥ 3 of 3 | **PASS — 3 of 3** |
| Flag rates H2–H5 | reported | **5.60 / 7.19 / 6.47 / 6.00 %** |

Development: **40 TP, 2 FN, 0 FP, cost 10**, from 38/4/0 and cost 20 at Gate 3.
Amount exact match 0.775. Submission rows 1,872 → 1,881.

The two remaining development misses are `unit_price_mismatch` (INV-H1-000151)
and `premium_omitted` (INV-H1-000619), both pricing-family and both Gate 5 work.

## Step 1 — reviewed rule files

Caps and windows were bare fields on the service records with no citation of
their own. Each hospital now ships `contracts/rules_hospital_N.json` naming the
services, the cap or window, the clause it comes from and the dates it is
effective between. A schema validator checks the file against the contract it
cites in both directions, so a rule cannot be silently added or dropped, and
every entry must carry a citation.

Effective dates span the whole term everywhere. Hospital 3 is the only hospital
with an amendment, and clause A1.4.1 states the caps, exclusion windows and
calculation conventions of the Base Agreement are unchanged and apply to the
substituted rates in the same way. That reading is recorded in the H3 file.

## Step 2 — daily caps across invoices

The cap was previously applied per line inside the pricing path, so a quantity
split across two invoices never reached it and a capped line on an otherwise
unresolved invoice was withheld. Quantity is now summed per patient, service and
Service Day **across every invoice in the retained history**, and a total over
the cap is a finding reported whatever else on the invoice is unresolved.

INV-H1-000049 shows why both halves mattered: its capped line is 15 units
against a cap of 12, and the invoice was withheld only because two *other* lines
were ambiguous.

**Hospital 2's Service Day.** H2 defines a Service Day as 07:00 to 06:59 the
next calendar day, but the snapshots record dates and no times, so nothing can
be shown to cross that boundary, and clause 2.2 puts a service delivered wholly
within a calendar day on the Service Day bearing that date. The calendar date is
used as the Service Day, which is the same reading the after-invoice check has
relied on since Gate 2. Caps are judged on the patient's total for that Service
Day across all lines, not per line.

## Step 3 — exclusion windows

A service billed inside an excluded window is now a finding, read from the
contract's own rules and the retained history rather than inferred from a priced
rate, so it survives an unresolved line elsewhere on the invoice.

**Boundary.** "Not billable within N days of this Service" covers a Service Date
exactly N days away. That is the ordinary meaning of "within", and it makes the
boundary day the last day the window covers rather than the first day outside
it. The code previously treated the boundary as uncertain and withheld; the
semantics label `uncertain_at_equal` has been replaced by `inclusive_at_equal`
across all five contracts so the name matches the behaviour. INV-H1-000646 is
exactly this case: its anchor sits 7 days from a 7-day window.

**Direction, recorded per hospital.**

| Hospital | Direction | Reading |
|---|---|---|
| H1, H4 | `both` | Clause 10.1 measures the window in either direction. |
| H2 | `uncertain_before_or_both` | Audited under every reading; only an anchor the readings agree on is reported. |
| H3, H5 | `uncertain_direction` | The clause does not fix the direction, so the line is audited under every reading, and only an anchor on the Service Date itself is excluded under all of them. |

Hospital 3's direction is the known ambiguity, and it goes through the
every-reading method rather than a guess: where the readings disagree the
question stays open and nothing is reported.

## Flag rates

| Hospital | Invoices | Rows | Flags | Flag rate |
|---|---:|---:|---:|---:|
| H1 (unscored) | 913 | 644 | 56 | 6.13% |
| H2 | 1,125 | 128 | 63 | 5.60% |
| H3 | 932 | 690 | 67 | 7.19% |
| H4 | 835 | 460 | 54 | 6.47% |
| H5 | 1,050 | 603 | 63 | 6.00% |

All four scored hospitals sit inside the 4–12% band and close to the 7.2%
scored base rate. 149 tests pass. The check partition was not read.
