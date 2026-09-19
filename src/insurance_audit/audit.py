"""Complete invoice opinions; no label or model access.

Two decisions can be reached. A *finding* is evidence that is itself the error:
it is reported whatever else on the invoice is unresolved. A *complete audit*
prices every line and either reports the priced differences or asserts the
invoice is clean. Only an invoice with neither is withheld, and every withheld
invoice carries a named unresolved fact.
"""
from collections import defaultdict
from datetime import date, timedelta
from .context import Context
from .findings import Findings, order
from .resolve import resolve
from .pricing import rate_for, Uncertain
from .checks import validate_line_facts, line_result


def line_key(source, row):
    return f'{source}:{row}'


def corrected_total(facts, priced, categories):
    """Full correction where every line is priced, partial correction otherwise.

    A line the audit could not price keeps its billed amount, except where a
    contract-free correction exists: an arithmetic line total is recomputed from
    its own quantity and unit price, and a line billed twice across invoices is
    not payable at all and contributes nothing.
    """
    canonical = facts['canonical_header']
    billed = canonical['invoice_total_cents']
    if facts['reused_invoice_id']:
        # Lines cannot be attributed between the physical records sharing the
        # identifier, so no line-level correction is supportable.
        return billed, 'reused_identifier_canonical_billed_total', []
    total = 0
    contributions = []
    full = True
    for line in facts['lines']:
        key = line_key(line['source'], line['row'])
        entry = {'source': line['source'], 'source_row': line['row'], 'line_id': line['line_id']}
        if 'cross_invoice_duplicate' in line['defects']:
            contributions.append(dict(entry, contribution_cents=0, basis='duplicate_not_payable'))
            full = False
            continue
        result = priced.get(key)
        if result is not None:
            total += result['expected_total_cents']
            contributions.append(dict(entry, contribution_cents=result['expected_total_cents'], basis='corrected'))
            continue
        full = False
        if 'line_total_arithmetic' in line['defects']:
            value = line['quantity'] * line['unit_price_cents']
            total += value
            contributions.append(dict(entry, contribution_cents=value, basis='arithmetic_recomputed'))
            continue
        if line['line_total_cents'] is None:
            return billed, 'unrecoverable_line_amount_billed_total', []
        total += line['line_total_cents']
        contributions.append(dict(entry, contribution_cents=line['line_total_cents'], basis='billed'))
    return total, 'full_correction' if full else 'partial_correction', contributions


def audit(data, contract, mappings):
    context = Context(data, contract, mappings)
    structure = Findings(data, contract, mappings)
    by_invoice = defaultdict(list)
    for line in data.lines:
        by_invoice[line.invoice_id].append(line)
    opinions = []
    abstentions = []
    traces = []
    for invoice_id in sorted(context.invoice_ids):
        facts = structure.assess(invoice_id)
        canonical = facts['canonical_header']
        source_headers = context.header_evidence[invoice_id]
        trace = {'invoice_id': invoice_id, 'hospital': data.hospital,
                 'source_headers': [{'source': h['source'], 'row': h['row']} for h in source_headers],
                 'findings': facts['categories'], 'finding_evidence': facts['evidence'], 'lines': []}
        if any(h['status'] == 'quarantined' for h in source_headers):
            trace['header_ownership_evidence'] = source_headers
        reasons = []
        qualifications = set()
        if canonical is None:
            reasons.append({'reason': 'no_accepted_invoice_header'})
        if facts['reused_invoice_id']:
            reasons.append({'reason': 'conflicting_reused_invoice_id', 'detail': {
                'patients': sorted({h['patient_id'] for h in facts['headers'] if h['patient_id']}),
                'billed_totals': sorted({h['invoice_total_cents'] for h in facts['headers']
                                         if h['invoice_total_cents'] is not None})}})
        if structure.unattributable:
            reasons.append({'reason': 'unlinked_quarantined_invoice_header',
                            'detail': [{'source': r['source'], 'row': r['row'], 'reason': r['reason']}
                                       for r in structure.unattributable]})
        for line in facts['lines']:
            if line['status'] == 'quarantined' and not line['quarantine_category']:
                reasons.append({'reason': 'quarantined_required_source_record',
                                'detail': {'source_row': line_key(line['source'], line['row']),
                                           'quarantine_reason': line['reason']}})
        if not facts['lines']:
            reasons.append({'reason': 'invoice_without_accepted_lines'})
        # Hospital 2's Article XIII makes an invoice effective only if submitted
        # within sixty days of discharge, but no submission date is recorded, so
        # the condition is unobservable. It is logged and never suppresses a
        # finding or a priced difference: the invoice date does not prove the
        # submission date either way.
        if contract['semantics']['invoice_eligibility'] == 'unobserved_submission_deadline_and_waiver' and canonical:
            discharge = canonical['record'].discharge_date
            deadline = (date.fromisoformat(discharge) + timedelta(days=60)).isoformat() if discharge else None
            trace['unobserved_eligibility'] = {
                'source': 'H2 Articles II.5 and XIII.1-XIII.5', 'recorded_discharge_date': discharge,
                'provisional_60_day_deadline': deadline, 'invoice_date': canonical['invoice_date'],
                'missing': ['actual submission date', 'applicable episode/leave evidence',
                            'written agreement or exception if late'],
                'effect': 'Effectiveness is unresolved. It is recorded, not treated as an error, '
                          'and every other check proceeds normally.'}
            qualifications.add('unobserved_submission_deadline_and_waiver')
        priced = {}
        categories = []
        grades = set()
        invariant = False
        complete = canonical is not None and not facts['reused_invoice_id'] and bool(facts['lines'])
        line_reasons = []
        if canonical is not None and not facts['reused_invoice_id']:
            invoice = canonical['record']
            for line in sorted(by_invoice[invoice_id], key=lambda l: (l.line_no, l.line_id, l.source_row)):
                key = line_key(line.source, line.source_row)
                sid, possible, grade = resolve(line.description, context.index, context.services)
                entry = {'line_id': line.line_id, 'source': line.source, 'source_row': line.source_row,
                         'description': line.description, 'service_id': sid,
                         'possible_service_ids': sorted(possible), 'mapping_grade': grade,
                         'quantity': line.quantity, 'billed_unit': line.unit_basis_as_billed,
                         'billed_unit_price_cents': line.unit_price_cents,
                         'billed_line_total_cents': line.line_total_cents}
                try:
                    if sid is None:
                        raise Uncertain('unresolved_service_mapping',
                                        {'description': line.description, 'candidates': sorted(possible)})
                    service = context.services[sid]
                    entry['source_refs'] = service['refs']
                    entry['duplicate_check'] = validate_line_facts(line, invoice, service, contract, context)
                    price = rate_for(line, invoice, service, contract, context)
                    result = line_result(line, service, price)
                    entry.update(status='supported', pricing=price, result=result)
                    priced[key] = result
                    categories.extend(result['error_categories'])
                    grades.add(grade)
                    invariant |= price['outcome_invariant_uncertainty']
                    qualifications.update(price.get('qualifications', []))
                except Uncertain as error:
                    reason = {'reason': error.reason, 'line_id': line.line_id, 'detail': error.detail}
                    line_reasons.append(reason)
                    entry.update(status='uncertain', reason=reason)
                    complete = False
                trace['lines'].append(entry)
        if any(l['status'] == 'quarantined' for l in facts['lines']):
            complete = False
        reasons.extend(line_reasons)
        findings = facts['categories']
        # No accepted header record means no billed total to report against, so
        # even a named finding cannot be emitted as a row.
        if canonical is not None and (findings or (complete and categories)):
            named = order(list(dict.fromkeys(findings + sorted(set(categories)))))
            expected, basis, contributions = corrected_total(facts, priced, named)
            billed = canonical['invoice_total_cents']
            if complete and expected != billed and 'invoice_total_mismatch' not in named:
                named = order(named + ['invoice_amount_mismatch'])
            unchanged = None
            if expected == billed:
                unchanged = ('finding_does_not_affect_the_payable_amount'
                             if not facts['amount_affecting'] and not categories
                             else 'corrections_offset_to_the_billed_total')
            opinion = {'invoice_id': invoice_id, 'hospital': data.hospital, 'flagged': 1,
                       'error_category': ';'.join(named), 'expected_total_cents': expected,
                       'billed_total_cents': billed, 'confidence': None,
                       'mapping_evidence': 'elided' if 'elided' in grades else 'explicit',
                       'outcome_invariant_uncertainty': invariant,
                       'confidence_state': 'not_assigned_before_policy',
                       'interpretation_qualifications': sorted(qualifications),
                       'decision_basis': 'complete_audit' if complete and not findings else 'finding',
                       'amount_basis': basis, 'amount_unchanged_reason': unchanged,
                       'trace_key': invoice_id}
            trace.update(status='supported', opinion=opinion, amount_contributions=contributions,
                         unresolved_facts=reasons)
            opinions.append(opinion)
        elif reasons or not complete:
            if not reasons:
                reasons.append({'reason': 'invoice_not_completely_audited'})
            definite = order(list(dict.fromkeys(findings + sorted(set(categories)))))
            trace.update(status='abstained', reasons=reasons, definite_error_categories=definite)
            abstentions.append({'invoice_id': invoice_id, 'hospital': data.hospital, 'reasons': reasons,
                                'definite_error_categories': definite})
        else:
            opinion = {'invoice_id': invoice_id, 'hospital': data.hospital, 'flagged': 0,
                       'error_category': '', 'expected_total_cents': sum(r['expected_total_cents'] for r in priced.values()),
                       'billed_total_cents': canonical['invoice_total_cents'], 'confidence': None,
                       'mapping_evidence': 'elided' if 'elided' in grades else 'explicit',
                       'outcome_invariant_uncertainty': invariant,
                       'confidence_state': 'not_assigned_before_policy',
                       'interpretation_qualifications': sorted(qualifications),
                       'decision_basis': 'complete_audit', 'amount_basis': 'full_correction',
                       'amount_unchanged_reason': None, 'trace_key': invoice_id}
            if opinion['expected_total_cents'] != opinion['billed_total_cents']:
                opinion.update(flagged=1, error_category='invoice_amount_mismatch',
                               amount_unchanged_reason=None)
            opinions.append(opinion)
            trace.update(status='supported', opinion=opinion,
                         amount_contributions=[{'source': l['source'], 'source_row': l['row'],
                                                'line_id': l['line_id'],
                                                'contribution_cents': priced[line_key(l['source'], l['row'])]['expected_total_cents'],
                                                'basis': 'corrected'} for l in facts['lines']],
                         unresolved_facts=[])
        traces.append(trace)
    return {'hospital': data.hospital, 'opinions': opinions, 'abstentions': abstentions, 'traces': traces,
            'accounting': {'raw_records': len(data.dispositions), 'accepted_invoice_records': len(data.invoices),
                           'accepted_line_records': len(data.lines),
                           'quarantined_records': sum(d['status'] == 'quarantined' for d in data.dispositions),
                           'unique_invoice_ids': len(context.invoice_ids), 'opinions': len(opinions),
                           'abstentions': len(abstentions), 'context_records': len(context.items),
                           'orphan_line_count': sum(l.invoice_id not in context.invoice_ids for l in data.lines)}}
