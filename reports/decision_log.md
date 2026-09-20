# Decision log

Every contract ambiguity found, and what was decided. Each decision is applied uniformly to all five hospitals and recorded in the decision traces. Development stands at 42 of 42 errors with no false positive; the check partition at 16 of 16, also with none.

## Ambiguities resolved

H2 clause 2.2 defines a Service Day as 07:00 to 06:59, but the records carry dates and no times, and the same clause places a service delivered wholly within a calendar day on that date. Both readings are admissible, so each was tested against H2's own billing: the calendar reading accounts for 5,004 of 5,094 relevant lines (98.23%), the 07:00 envelope for 2,175 (42.70%). The calendar reading is adopted, settling the weekend uplift, daily premium, bundle presence and cap allocation together. The denominator is every relevant line, not the subset a reading chooses to price; scored the other way the envelope appears to win by declining to price 2,912 lines.

Volume discounts are line-level in all five agreements. H2 clause 8.3 says "each subsequent Unit", but clause 3.5, in the calculation article, applies the discount to a line item on utilisation prior to that line. The calculation clause governs, so no line straddles a threshold. H1 2.4, H3 6.1 and H4 8.3-8.5 state the same rule directly.

"Not billable within N days" includes a service date exactly N days away, the ordinary meaning of "within". Where a clause does not fix the direction of an exclusion window (H3, H5) the line is audited under every reading and only an anchor all readings agree on is reported.

H2 never defines invoice_date, yet a service cannot be invoiced before it happens, so the after-invoice check stays enabled there. On H1 all twelve invoices with a line dated after the invoice date are labelled erroneous.

A reused invoice identifier's lines are attributed by the record number inside each line identifier, used only where every group's billed total reconciles to one header exactly. That holds for 29 of 31 reused identifiers; the other two report the canonical billed total unchanged.

Where a line's wording names more than one service, it is priced under every candidate and reported only when more than half the readings find a fault. Swept on development, any lower threshold flags 143 invoices of which 142 are clean.

## Ambiguities left unresolved

H4's clause never says whether volume utilisation aggregates across patients. The better reading accounts for 94.4% of its lines, below the 98% bar, so the stage stays ambiguous. H5's two facility readings are indistinguishable at 97.2% each, so its billing does not choose between them. Both leave those invoices withheld rather than decided on a guess. Where a billed quantity exceeds a daily cap the delivered quantity is unobservable: the corrected amount is the capped quantity, and the row is penalised in confidence rather than guessed.

## Standing rules

A billed price is never evidence of which service a line names. Every one of the 925 ambiguous lines in H2-H5 has exactly one candidate whose contracted rate equals the billed rate, and that signal is deliberately unused: on a line whose rate is wrong it would select the service that makes the error vanish. Using the billed population to choose between readings of a clause is a different thing, and is disclosed above.

A description naming no contracted service has no contracted rate, so its billed amount stands and only the naming is reported. Confidence is confidence in the whole emitted row, flag and corrected amount together, not in the flag alone.
