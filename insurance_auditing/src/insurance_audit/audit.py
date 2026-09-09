"""Complete invoice opinions; no label or model access."""
from collections import defaultdict
from datetime import date,timedelta
from .context import Context
from .resolve import resolve
from .pricing import rate_for,Uncertain
from .checks import validate_line_facts,line_result


def audit(data,contract,mappings):
    context=Context(data,contract,mappings);by_invoice=defaultdict(list)
    for line in data.lines:by_invoice[line.invoice_id].append(line)
    opinions=[];abstentions=[];traces=[]
    for invoice_id in sorted(context.invoice_ids):
        headers=sorted(context.headers.get(invoice_id,[]),key=lambda h:(h.source,h.source_row))
        source_headers=context.header_evidence[invoice_id]
        trace={'invoice_id':invoice_id,'hospital':data.hospital,
               'source_headers':[{'source':h['source'],'row':h['row']} for h in source_headers],'lines':[]}
        if any(h['status']=='quarantined' for h in source_headers):trace['header_ownership_evidence']=source_headers
        reasons=[];categories=[]
        if not headers:reasons.append({'reason':'no_accepted_invoice_header'})
        elif len(headers)>1:
            reasons.append({'reason':'conflicting_reused_invoice_id','detail':{'patients':sorted({h.patient_id for h in headers}),'billed_totals':sorted({h.invoice_total_cents for h in headers})}})
        if context.unlinked_headers:
            reasons.append({'reason':'unlinked_quarantined_invoice_header','detail':context.unlinked_headers})
        if invoice_id in context.quarantined_invoices:reasons.append({'reason':'quarantined_required_source_record'})
        lines=sorted(by_invoice[invoice_id],key=lambda l:(l.line_no,l.line_id,l.source_row))
        if not lines:reasons.append({'reason':'invoice_without_accepted_lines'})
        if reasons:
            trace.update(status='abstained',reasons=reasons);abstentions.append({'invoice_id':invoice_id,'hospital':data.hospital,'reasons':reasons});traces.append(trace);continue
        invoice=headers[0]
        if contract['semantics']['invoice_eligibility']=='unobserved_submission_deadline_and_waiver':
            deadline=(date.fromisoformat(invoice.discharge_date)+timedelta(days=60)).isoformat() if invoice.discharge_date else None
            reasons.append({'reason':'unobserved_submission_deadline_and_waiver','detail':{
                'source':'H2 Articles II.5 and XIII.1–XIII.5','recorded_discharge_date':invoice.discharge_date,
                'provisional_60_day_deadline':deadline,'invoice_date':invoice.invoice_date,
                'missing':['actual submission date','applicable episode/leave evidence','written agreement or exception if late'],
                'effect':'Invoice date does not prove submission. Neither effectiveness nor a corrected payable total is established; service pricing below is diagnostic only.'}})
        if invoice.contract_number!=contract['contract_number']:categories.append('contract_reference_mismatch')
        if invoice.hospital_id!=data.hospital:categories.append('hospital_reference_mismatch')
        if sum(l.line_total_cents for l in lines)!=invoice.invoice_total_cents:categories.append('invoice_arithmetic_mismatch')
        expected=0;grades=set();invariant=False;qualifications=set()
        for line in lines:
            sid,possible,grade=resolve(line.description,context.index,context.services)
            entry={'line_id':line.line_id,'source':line.source,'source_row':line.source_row,'description':line.description,
                   'service_id':sid,'possible_service_ids':sorted(possible),'mapping_grade':grade,'quantity':line.quantity,
                   'billed_unit':line.unit_basis_as_billed,'billed_unit_price_cents':line.unit_price_cents,'billed_line_total_cents':line.line_total_cents}
            try:
                if sid is None:raise Uncertain('unresolved_service_mapping',{'description':line.description,'candidates':sorted(possible)})
                service=context.services[sid];entry['source_refs']=service['refs']
                entry['duplicate_check']=validate_line_facts(line,invoice,service,contract,context)
                priced=rate_for(line,invoice,service,contract,context);result=line_result(line,service,priced)
                entry.update(status='supported',pricing=priced,result=result)
                expected+=result['expected_total_cents'];categories.extend(result['error_categories']);grades.add(grade)
                invariant|=priced['outcome_invariant_uncertainty']
                qualifications.update(priced.get('qualifications',[]))
            except Uncertain as error:
                reason={'reason':error.reason,'line_id':line.line_id,'detail':error.detail};reasons.append(reason);entry.update(status='uncertain',reason=reason)
            trace['lines'].append(entry)
        if reasons:
            trace.update(status='abstained',reasons=reasons,definite_error_categories=sorted(set(categories)))
            abstentions.append({'invoice_id':invoice_id,'hospital':data.hospital,'reasons':reasons,'definite_error_categories':sorted(set(categories))})
        else:
            if invoice.invoice_total_cents!=expected:categories.append('invoice_amount_mismatch')
            categories=sorted(set(categories))
            opinion={'invoice_id':invoice_id,'hospital':data.hospital,'flagged':int(bool(categories)),
                     'error_category':';'.join(categories),'expected_total_cents':expected,'billed_total_cents':invoice.invoice_total_cents,
                     'confidence':None,'mapping_evidence':'elided' if 'elided' in grades else 'explicit',
                     'outcome_invariant_uncertainty':invariant,'confidence_state':'not_assigned_before_policy',
                     'interpretation_qualifications':sorted(qualifications),
                     'trace_key':invoice_id}
            opinions.append(opinion);trace.update(status='supported',opinion=opinion)
        traces.append(trace)
    return {'hospital':data.hospital,'opinions':opinions,'abstentions':abstentions,'traces':traces,
            'accounting':{'raw_records':len(data.dispositions),'accepted_invoice_records':len(data.invoices),
                          'accepted_line_records':len(data.lines),'quarantined_records':sum(d['status']=='quarantined' for d in data.dispositions),
                          'unique_invoice_ids':len(context.invoice_ids),'opinions':len(opinions),'abstentions':len(abstentions),
                          'context_records':len(context.items),'orphan_line_count':sum(l.invoice_id not in context.invoice_ids for l in data.lines)}}
