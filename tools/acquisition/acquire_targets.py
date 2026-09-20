"""Work-authored H3/H4/H5 interpretations, with lossless table transcription.

Finite records only: the pricing interpreter is shared and contains no per-
hospital generated function. This script creates candidates, not acceptance.
"""
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import load_hospital,write_json
from insurance_audit.resolve import normalize
from insurance_audit.schema import digest,validate_contract,validate_mappings
from acquire_h1 import cents,UNIT
from prepare_inventory import candidates
from mapping_policy import evidence_grade


def document(path):
    result=defaultdict(list);section='';paragraphs=[]
    for n,line in enumerate((ROOT/path).read_text().splitlines(),1):
        if line.startswith('#'):
            section=line.lstrip('# ').strip();paragraphs.append((n,section))
        if line.startswith('|'):
            cells=[v.strip() for v in line.strip('|').split('|')]
            if cells[0] not in ['Service','Service A','Facility code'] and not cells[0].startswith('---'):
                result[section].append((f'{path}#L{n}',cells))
    return result,paragraphs


def section(doc,prefix):
    matches=[rows for heading,rows in doc.items() if heading.startswith(prefix)]
    assert len(matches)==1,(prefix,list(doc))
    return matches[0]


def number(text):
    values=re.findall(r'\d+',text);assert len(values)==1,text
    return int(values[0])


def multiplier(text):
    f=Fraction(text);return [f.numerator,f.denominator]


def new_service(hospital,i,row,source,start='2024-01-01'):
    unit=UNIT.get(row[1],'per_hour_per_item' if row[1]=='per hour, per item' else None)
    assert unit,row
    return {'id':f'{hospital}-S{i:03d}','name':row[0],'unit':unit,
        'versions':[{'start':start,'end':'2025-12-31','cents':cents(row[2]),'priority':0,'source':source}],
        'daily_premium':None,'weekend_multiplier':[1,1],'volume_discounts':[],
        'daily_cap':number(row[3]) if len(row)==4 and row[3]!='—' else None,
        'facility_multipliers':{},'tier_multipliers':{},
        'support':'composite_dimension_unobserved' if unit=='per_hour_per_item' else 'supported','refs':[source]}


def add_adjustments(c,doc,premium,weekend,discount,caps,bundles,exclusions,alternate_bundle=False):
    by={s['name']:s for s in c['services']}
    for key,typ in [(premium,'premium'),(weekend,'weekend'),(discount,'discount'),(caps,'cap')]:
        if key is None:continue
        for ref,r in section(doc,key):
            s=by[r[0]];s['refs'].append(ref)
            if typ=='premium':s['daily_premium']={'exceeds':number(r[1]),'multiplier':[100+number(r[2]),100],'source':ref}
            elif typ=='weekend':s['weekend_multiplier']=[100+number(r[1]),100]
            elif typ=='discount':s['volume_discounts'].append({'exceeds':number(r[1]),'multiplier':[100-number(r[2]),100],'source':ref})
            elif typ=='cap':
                q=number(r[1]);assert s['daily_cap'] in {None,q},'Contradictory cap';s['daily_cap']=q
    for ref,r in section(doc,bundles):
        a,ar,b,br=r if alternate_bundle else [r[0],r[2],r[1],r[3]]
        c['bundles'].append({'a':by[a]['id'],'b':by[b]['id'],'a_cents':cents(ar),'b_cents':cents(br),'source':ref})
    for ref,r in section(doc,exclusions):
        c['exclusions'].append({'service':by[r[0]]['id'],'anchor':by[r[2]]['id'],'days':number(r[1]),'source':ref})


def mappings(c):
    data=load_hospital(ROOT/'data/source',c['hospital']);by={s['name']:s['id'] for s in c['services']}
    descriptions={l.description for l in data.lines}
    descriptions.update(d['raw_named']['description'] for d in data.dispositions if d['kind']=='line_items' and d['status']=='quarantined')
    proposed={d:candidates(d,sorted(by)) for d in sorted(descriptions)};records={}
    for d,options in proposed.items():
        key=normalize(d);grade=evidence_grade(d,options[0]) if len(options)==1 else 'unresolved'
        sid=by[options[0]] if grade!='unresolved' else None;ids=[by[n] for n in options]
        row={'key':key,'raw_descriptions':[d],'state':'accepted' if sid else 'unresolved','service_id':sid,'candidates':ids,'grade':grade,
             'evidence':['Candidate acquisition under prompts/map_v2.md. Essential concepts must have distinct supporting tokens; no billed prices or units select service.',
                         'Source-qualified catalog and abbreviation lexicon; group review is required before package acceptance.']}
        if key in records:
            assert (records[key]['service_id'],records[key]['candidates'])==(sid,ids),'Collision'
            records[key]['raw_descriptions'].append(d)
        else:records[key]=row
    h=c['hospital'];write_json(ROOT/f'mappings/{h}.candidates.raw.json',{'hospital':h,'catalog':sorted(by),'proposals':proposed})
    return {'schema_version':'2','hospital':h,'review_state':'candidate','normalizer_version':'2','records':[records[k] for k in sorted(records)]}


def acquire(h):
    paths={
       'H3':['hospital_3/base_agreement.md','hospital_3/appendix_b_rate_schedule.md','hospital_3/amendment_no_1.md'],
       'H4':['hospital_4/conditional_reimbursement_agreement.md'],
       'H5':['hospital_5/network_reimbursement_agreement.md']}[h]
    paths=['data/source/contracts/'+p for p in paths];docs=[document(p) for p in paths]
    semantics={'rounding':'half_up_cent','adjustment_order':['bundle','facility','tier','daily_premium','weekend_uplift','volume_discount'],
       'invoice_eligibility':'supplied_invoice_facts','service_date_not_after_invoice':True,'service_day':'calendar','exclusion_direction':'both' if h=='H4' else 'uncertain_direction','exclusion_boundary':'uncertain_at_equal',
       'duplicate_policy':'abstain_repeated_service_day','cap_policy':'single_line_cap_otherwise_abstain',
       'facility_source':'invoice_projection_reviewed' if h=='H5' else 'none',
       'volume_basis':'contract_term_patient_scope_unspecified' if h=='H4' else 'contract_term_all_patients_strict_prior_billed_units',
       'version_precedence':'amendment_over_base' if h=='H3' else 'single','refs':paths}
    c={'schema_version':'2','semantics_version':'2','hospital':h,'contract_number':{'H3':'INS-H3-2024-0562','H4':'INS-H4-2024-2049','H5':'INS-H5-2024-0731'}[h],
       'term':['2024-01-01','2025-12-31'],'review_state':'candidate','source_hashes':{p:digest(ROOT/p) for p in paths},
       'semantics':semantics,'services':[],'bundles':[],'exclusions':[],'coverage':[]}
    rates=section(docs[1][0],'B.1') if h=='H3' else section(docs[0][0],'3.' if h=='H4' else '4.')
    c['services']=[new_service(h,i,r,ref) for i,(ref,r) in enumerate(rates,1)]
    if h=='H3':
        add_adjustments(c,docs[0][0],'4.','5.','6.','7.','8.','9.')
        by={s['name']:s for s in c['services']}
        for ref,r in section(docs[2][0],'A1.2'):
            s=by[r[0]];assert s['versions'][0]['cents']==cents(r[2]) and s['unit']==UNIT[r[1]],'Amendment prior rate/unit conflict'
            s['versions'].append({'start':'2025-01-01','end':'2025-12-31','cents':cents(r[3]),'priority':1,'source':ref});s['refs'].append(ref)
        for ref,r in section(docs[2][0],'A1.3'):
            c['services'].append(new_service(h,len(c['services'])+1,r,ref,'2025-01-01'))
    elif h=='H4':add_adjustments(c,docs[0][0],'5.',None,'8.','6.','7.','9.',True)
    else:
        add_adjustments(c,docs[0][0],'5.','6.','8.',None,'7.','9.',True)
        by={s['name']:s for s in c['services']}
        for prefix,field,cols in [('Table 2','facility_multipliers',['F-MAIN','F-NORTH','F-COAST']),('Table 3','tier_multipliers',['BRONZE','SILVER','GOLD'])]:
            for ref,r in section(docs[0][0],prefix):
                by[r[0]][field]={col:multiplier(v) for col,v in zip(cols,r[1:])};by[r[0]]['refs'].append(ref)
            assert all(s[field] for s in c['services']),f'Missing {field}'
    qualifications={
      'H3':'§9 temporal direction and boundary are not explicit: only same-day definite anchors or proven no reachable anchor permit a result; absent compound-unit dimension is withheld. A1.4.2 settlement is unobserved, but valid pre-effective service is unchanged and valid post-effective service cannot be on an invoice issued/settled before that service. This chronological interpretation is recorded, not a measured settlement fact.',
      'H4':'§1.4 instance equals one unit. §8 does not explicitly state patient aggregation scope: retain bounds from known patient-specific to all-patient prior usage; emit only invariant rates. §9 explicitly both directions; equality withheld. Compound unit unobserved.',
      'H5':'§1.2/Table2 refer to line facility, absent in CSV. Adopt invoice facility as each line facility from supplied relational shape and §10.1; this is a recorded projection assumption, with confidence capped at .65 when outcome-relevant. §9 direction/equality unresolved. §8 subsequent units interpreted as strictly prior whole-term billed units without facility/tier resets. Compound unit unobserved.'}[h]
    for path,(_,headings) in zip(paths,docs):
        for n,heading in headings:
            uncertain=(h in {'H3','H5'} and heading.startswith('9.')) or (h=='H4' and heading.startswith('8.')) or (h=='H5' and (heading.startswith('1.') or heading.startswith('Table 2'))) or (h=='H3' and heading.startswith('A1.4'))
            c['coverage'].append({'source':f'{path}#L{n}','state':'unresolved' if uncertain else 'accepted','representation':heading,
                'qualification':qualifications+' See finite records for exact rule applicability; missing essential mappings and disputed dependencies withhold the entire invoice.'})
    for s in c['services']:
        if s['support']!='supported':c['coverage'].append({'source':s['refs'][0],'state':'unresolved','representation':s['name'],'qualification':'per hour, per item supplies no independent second quantity dimension; no invented conversion.'})
    validate_contract(c);m=mappings(c);validate_mappings(m,c)
    write_json(ROOT/f'contracts/hospital_{h[1:]}.raw.json',c);write_json(ROOT/f'mappings/hospital_{h[1:]}.raw.json',m)
    write_json(ROOT/f'reports/{h}_acquisition_manifest.json',{'mode':'Work model source interpretation and deterministic table transcription, no programmatic model calls',
        'sources':c['source_hashes'],'raw_contract_sha256':digest(ROOT/f'contracts/hospital_{h[1:]}.raw.json'),
        'raw_mapping_sha256':digest(ROOT/f'mappings/hospital_{h[1:]}.raw.json'),
        'prompts':{p:digest(ROOT/p) for p in ['prompts/extract_v1.md','prompts/review_v1.md','prompts/map_v2.md']},
        'interpretation':qualifications,'source_review_state':'candidate, not accepted'})
    print(json.dumps({'hospital':h,'services':len(c['services']),'mapping_keys':len(m['records']),
        'accepted_candidates':sum(r['state']=='accepted' for r in m['records']),'unresolved':sum(r['state']=='unresolved' for r in m['records']),
        'premiums':sum(s['daily_premium'] is not None for s in c['services']),'volume_tiers':sum(len(s['volume_discounts']) for s in c['services']),
        'caps':sum(s['daily_cap'] is not None for s in c['services']),'bundles':len(c['bundles']),'exclusions':len(c['exclusions'])}))


if __name__=='__main__':
    for hospital in sys.argv[1:]:acquire(hospital)
