"""Work-authored prose-to-record transcription, preserving all clause sources."""
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest,validate_contract,validate_mappings
from acquire_targets import new_service,mappings

SOURCE='data/source/contracts/hospital_2/master_services_agreement.md'


def acquire():
    text=(ROOT/SOURCE).read_text();services=[];clauses=[]
    for n,line in enumerate(text.splitlines(),1):
        m=re.match(r'(\d+\.\d+) In respect of (.+?), the Provider shall invoice the Payer at the rate of (GBP [\d,]+\.\d\d) (per [^.]+)\.',line)
        if not m:continue
        clause,name,money,unit=m.groups();ref=f'{SOURCE}#L{n}'
        s=new_service('H2',len(services)+1,[name,unit,money],ref)
        cap=re.search(r'not bill more than [a-z -]+\((\d+)\) .+? of this Service for a Patient on a single Service Day\.',line)
        if cap:s['daily_cap']=int(cap[1])
        premium=re.search(r'Where the aggregate quantity.+?exceeds [a-z -]+\((\d+)\) .+?increased by [a-z -]+\((\d+)%\)',line)
        if premium:s['daily_premium']={'exceeds':int(premium[1]),'multiplier':[100+int(premium[2]),100],'source':ref}
        weekend=re.search(r'Where the Service Date.+?Business Day, .+?increased by [a-z -]+\((\d+)%\)',line)
        if weekend:s['weekend_multiplier']=[100+int(weekend[1]),100]
        for d in re.finditer(r'Where cumulative utilisation.+?exceeds [a-z -]+\((\d+)\) .+?a discount of [a-z -]+\((\d+)%\)',line):
            s['volume_discounts'].append({'exceeds':int(d[1]),'multiplier':[100-int(d[2]),100],'source':ref})
        services.append(s);clauses.append((ref,line,s,clause))
    by={s['name']:s for s in services};bundles={};exclusions=[]
    from acquire_h1 import cents
    for ref,line,s,clause in clauses:
        b=re.search(r'Where this Service and (.+?) are both delivered.+?this Service at (GBP [\d,]+\.\d\d) (per .+?) and (.+?) at (GBP [\d,]+\.\d\d) (per .+?), in substitution',line)
        if b:
            partner,a_money,a_unit,partner2,b_money,b_unit=b.groups();assert partner==partner2
            assert partner in by and by[partner]['unit']==new_service('H2',0,[partner,b_unit,b_money],ref)['unit']
            assert s['unit']==new_service('H2',0,[s['name'],a_unit,a_money],ref)['unit']
            pair=tuple(sorted([s['id'],by[partner]['id']]));amounts={s['id']:cents(a_money),by[partner]['id']:cents(b_money)}
            if pair in bundles:
                prev=bundles[pair];assert (prev['a_cents'],prev['b_cents'])==(amounts[pair[0]],amounts[pair[1]]),'Repeated bundle disagrees'
                prev['source']+='; '+ref
            else:bundles[pair]={'a':pair[0],'b':pair[1],'a_cents':amounts[pair[0]],'b_cents':amounts[pair[1]],'source':ref}
        e=re.search(r'This Service is not billable where (.+?) has been delivered to the same Patient within [a-z -]+\((\d+)\) days of the Service Date\.',line)
        if e:exclusions.append({'service':s['id'],'anchor':by[e[1]]['id'],'days':int(e[2]),'source':ref})
    c={'schema_version':'2','semantics_version':'2','hospital':'H2','contract_number':'INS-H2-2024-1183',
       'term':['2024-01-01','2025-12-31'],'review_state':'candidate','source_hashes':{SOURCE:digest(ROOT/SOURCE)},
       'semantics':{'rounding':'half_up_cent','adjustment_order':['bundle','facility','tier','daily_premium','weekend_uplift','volume_discount'],
           'service_day':'seven_am_unobserved','exclusion_direction':'both','exclusion_boundary':'uncertain_at_equal',
           'duplicate_policy':'no_explicit_service_date_prohibition','cap_policy':'single_line_cap_otherwise_abstain',
           'facility_source':'none','volume_basis':'contract_term_all_patients_strict_prior_billed_units','version_precedence':'single',
           'service_date_not_after_invoice':False,'invoice_eligibility':'unobserved_submission_deadline_and_waiver',
           'refs':[f'{SOURCE} Articles I–III, XIII, XXIII']},
       'services':services,'bundles':list(bundles.values()),'exclusions':exclusions,'coverage':[]}
    for n,line in enumerate(text.splitlines(),1):
        if not line.startswith('## Article'):continue
        m=re.search(r'Article ([IVXL]+)',line);roman=m[1]
        if 'Contracted Services' in line:
            state='accepted';rep='Each rate/rule sentence transcribed with clause references; repeated unit/description/inclusive-cost requirements retained in reading ledger.'
        elif roman in {'I','III','XXIII'}:
            state='accepted';rep='Term, identity facility/tier, exact calculation, explicit prior utilisation and bidirectional Service Date exclusions, service identification.'
        elif roman in {'II','XIII'}:
            state='unresolved';rep='07:00 Service Day and single-calendar-day qualification lack timestamps/duration; clinical episode/leave and actual submission deadline effectiveness lack observations.'
        else:
            state='outside_scope';rep='Administrative workflow/records/legal governance; no supplied evidence of event activation or calculable alternative rate. No claim of contractual workflow compliance.'
        c['coverage'].append({'source':f'{SOURCE}#L{n}','state':state,'representation':line.lstrip('# ')+' — '+rep,
            'qualification':'Entire H2 invoice opinions withheld by Article XIII eligibility uncertainty; line-level calculations are diagnostic. No H1 service-date-after-invoice or repeated-service prohibition is imported into H2. No episode index is fabricated from dates without leave evidence.'})
    for ref,line,s,clause in clauses:
        c['coverage'].append({'source':ref,'state':'unresolved' if s['support']!='supported' else 'accepted',
            'representation':clause+' '+s['name'],'qualification':'Dependent day rules use uncertainty envelopes, not invented times; per-hour/per-item is unsupported without a second dimension. All six standard repeated sentences are retained in reports/H2_reading_index.json.'})
    validate_contract(c);m=mappings(c);validate_mappings(m,c)
    write_json(ROOT/'contracts/hospital_2.raw.json',c);write_json(ROOT/'mappings/hospital_2.raw.json',m)
    write_json(ROOT/'reports/H2_acquisition_manifest.json',{'mode':'Work-session model interpretation with deterministic prose transcription, no model API',
        'sources':c['source_hashes'],'raw_contract_sha256':digest(ROOT/'contracts/hospital_2.raw.json'),
        'raw_mapping_sha256':digest(ROOT/'mappings/hospital_2.raw.json'),
        'prompts':{p:digest(ROOT/p) for p in ['prompts/extract_v1.md','prompts/review_v1.md','prompts/map_v2.md']},
        'full_reading_evidence':['reports/H2_reading_index.json','reports/H2_reading_remaining.txt'],
        'rate_clause_count':len(services),'numeric_rule_counts':{'premiums':sum(s['daily_premium'] is not None for s in services),
          'weekend':sum(s['weekend_multiplier']!=[1,1] for s in services),'discount_tiers':sum(len(s['volume_discounts']) for s in services),
          'caps':sum(s['daily_cap'] is not None for s in services),'bundles':len(bundles),'exclusions':len(exclusions)},
        'eligibility':'No final H2 opinion without actual submission/exception facts; diagnostic package only.'})
    print(json.dumps({'services':len(services),'mappings':len(m['records']),'accepted_keys':sum(r['state']=='accepted' for r in m['records'])}))


if __name__=='__main__':acquire()
