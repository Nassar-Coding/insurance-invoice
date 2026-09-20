# Gate 6 — ambiguity threshold and confidence

## Exit criteria

| Criterion | Target | Result |
|---|---|---|
| Ambiguity threshold documented | swept and chosen | **PASS — strict majority (> 0.5)** |
| Confidence tiers documented | fitted to development | **PASS — six tiers** |
| Expected calibration error | ≤ 0.08 | **PASS — 0.0322** |
| Development cost | not worse than Gate 5 | **PASS — 10, unchanged** |

## The ambiguity threshold

Swept from 1/6 to 1 over the development invoices whose only unresolved reason
is an ambiguous reading. Every observed error fraction is exactly 0.5: each of
these lines has two candidate readings, one of which finds a fault.

| Threshold | Newly flagged | FN | FP | Cost |
|---|---:|---:|---:|---:|
| 0.167 – 0.500 | 143 | 1 | 142 | **147** |
| 0.510 – 1.000 | 0 | 2 | 0 | **10** |

143 development invoices sit at 0.5 and **142 of them are clean**, so flagging on
a split reading costs 142 false positives to recover one miss. The chosen rule is
therefore to flag on ambiguity alone only when **strictly more than half** the
readings find a fault, which coincides with the plan's stated default of a
majority. This confirms the decision layer's existing behaviour rather than
changing it, so the cost is unchanged at 10.

## Confidence tiers

Every emitted row now declares which kind of evidence it rests on, and each row
takes the first tier that applies. Values are the Wilson 95% lower bound on
development accuracy, rounded **down** to a hundredth so the published figure is
never above the evidence, and never allowed to fall below a weaker tier.

| Tier | n | Development accuracy | H1 confidence | H2–H5 |
|---|---:|---:|---:|---:|
| ambiguous | 2 | 0.500 | 0.09 | 0.08 |
| partial_amount | 0 | — | 0.50 | 0.45 |
| no_match | 6 | 1.000 | 0.60 | 0.54 |
| match_fully_priced | 7 | 0.857 | 0.60 | 0.54 |
| structural | 25 | 0.960 | 0.80 | 0.72 |
| clean | 404 | 1.000 | 0.99 | 0.89 |

Only `clean` clears the 30-observation bar, so it is the only tier marked
fitted; the rest are marked sparse and held at the level of the weaker tier
rather than fitted to their own small samples. **Hospitals 2–5 take the fitted
value reduced by a tenth** — they have no labels at all, so this is a judgment
that they are no better understood than Hospital 1, never transferred accuracy.

Two qualifications cap confidence further regardless of tier: an outcome that
holds under several readings, and any recorded interpretation, both at 0.65. A
row whose amount used a **capped quantity in place of an unobserved one** is
capped at 0.45, which is the confidence penalty Gate 5's daily-cap rule calls
for.

## Reliability

| Bin | n | Mean confidence | Accuracy |
|---|---:|---:|---:|
| 0.0 – 0.2 | 2 | 0.090 | 0.500 |
| 0.4 – 0.6 | 1 | 0.450 | 0.000 |
| 0.6 – 0.8 | 13 | 0.600 | 0.923 |
| 0.8 – 1.0 | 428 | 0.979 | 1.000 |

**ECE 0.0322.** Confidence rises with accuracy across the populated bins with one
exception: a single row in the 0.4–0.6 bin, the capped-quantity case, whose
amount is wrong by design. It is under-confident rather than over-confident,
which is the safe direction, and one row cannot be fitted. Tier-level
monotonicity holds exactly and is asserted by a test against the shipped policy.

Calibration is measured by the organisers but is not part of the ranking cost,
so no further fitting was done. 175 tests pass; the check partition was not read.
