# Gate 7 — decoy and distribution audit

## Exit criteria

| Criterion | Target | Result |
|---|---|---|
| Decoy-proxy flags | 0 | **PASS — 0 of 184** |
| Audit findings and fixes listed | listed | **PASS — 2 found, 2 fixed** |
| Flag rates H2–H5 | within 4–12% | **PASS — 5.60 / 7.19 / 6.47 / 6.19 %** |
| Submission regenerated | SHA-256 reported | **PASS** |

Development after the fixes: 40 TP, 2 FN, 0 FP, cost 10; amount exact match
0.925; ECE 0.0322 — every figure unchanged from Gate 6, as required.

## 1. Decoy proxies

0 flags on all 184, and 0 on every pattern taken separately: rare description
(78), unusual quantity (66), service date equal to the invoice date (42), one
patient on two invoices for the same Service Day (27), the near-duplicate pair
across invoices (2), and the contract-term boundary date (1).

## 2. Trace audit — 15 flagged and 15 withheld per hospital

Two findings, both general and both fixed.

**A priced difference carried no named evidence.** 8 of the 60 sampled flags
(H3 2, H4 2, H5 4) rested on a recomputed rate whose working existed only on the
line, so `finding_evidence` was empty and a reviewer had nothing to read. A
priced difference now records the billed unit price, the rebuilt contracted
rate, both line totals, the adjustments applied in order, and the clause
references. Every sampled flag in all four hospitals now carries at least one
evidence item.

**The same arithmetic defect was named twice.** A line whose quantity times unit
price does not equal its line total was reported as both `line_total_arithmetic`
(findings layer) and `line_arithmetic_mismatch` (pricing path) on the same row.
The pricing path no longer names it, exactly as the unit-basis duplicate was
resolved at Gate 4, so a row carries the contract's own category once.

**No abstention leaks.** No withheld invoice in any sample had a definite error
category already named against it, and no withheld invoice lacked a named
reason. The withheld mix is dominated by genuine unresolvable facts: rate
outcomes that stay ambiguous, composite dimensions the record does not observe,
split readings of a description, and H2's unobserved Service Day cap allocation.

No flag was found resting on thin evidence, so no check was tightened, and
because nothing was loosened the development figures are unchanged.

## 3. Distribution

| Hospital | Invoices | Rows | Flags | Flag rate | Band |
|---|---:|---:|---:|---:|---|
| H1 (unscored) | 913 | 661 | 56 | 6.13% | — |
| H2 | 1,125 | 133 | 63 | 5.60% | in band |
| H3 | 932 | 720 | 67 | 7.19% | in band |
| H4 | 835 | 460 | 54 | 6.47% | in band |
| H5 | 1,050 | 664 | 65 | 6.19% | in band |

All four scored hospitals sit inside 4–12% and close to the 7.2% scored base
rate, and to Hospital 1's own 6.13%. H2 emits far fewer rows than the others
(133 against 460–720) because its Service Day is defined by a start time the
data never records, so its cap allocations and several rate outcomes stay
unresolved; its *flag* rate is nonetheless in band, which is what the cost
depends on.

## Submission

- **SHA-256** `c94dc630882dbbfc66b34fbc31dc7d6f2a5a2a52aa1fe6f2c8d8c90a0d53574a`
- **1,977 rows**, H2 133, H3 720, H4 460, H5 664; Hospital 1 is excluded.
- Validated by `verify-submission`: column order, one row per identifier,
  integer cents, confidence in range, and every billed total reconciled against
  the source records.

175 tests pass. The check partition was not read. The Final Gate has not begun.
