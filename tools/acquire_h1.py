"""Retained transcription aid for Work-authored declarative H1 interpretation.

This is NOT a model API call. The model read the complete source, authored the
finite semantics below, reviewed candidate aliases and retains all outputs.
The default writes raw candidates only; acceptance is a separate explicit step.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest,validate_contract,validate_mappings
from prepare_inventory import words,LEXICON

SOURCE='data/source/contracts/hospital_1/provider_services_agreement.md'


def tables(text):
    section=None;result=defaultdict(list)
    for lineno,line in enumerate(text.splitlines(),1):
        match=re.match(r'## (\d+)\.',line)
        if match:section=int(match[1])
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if cells[0] not in ['Service','Service A'] and not cells[0].startswith('---'):
                result[section].append((lineno,cells))
    return result


def cents(text):
    match=re.fullmatch(r'GBP ([\d,]+)\.(\d{2})',text)
    if not match:raise ValueError(f'Not exact GBP table amount: {text}')
    return int(match[1].replace(',',''))*100+int(match[2])


UNIT={'per hour':'per_hour','per day of service':'per_day','per night of occupancy':'per_night',
      'per visit':'per_visit','per test':'per_test','per procedure':'per_procedure','per item supplied':'per_item',
      'per unit dispensed':'per_unit_dispensed'}


def acquire():
    text=(ROOT/SOURCE).read_text();t=tables(text)
    services=[]
    for i,(line,r) in enumerate(t[4],1):
        services.append({'id':f'H1-S{i:03d}','name':r[0],'unit':UNIT[r[1]],
                         'versions':[{'start':'2024-01-01','end':'2025-12-31','cents':cents(r[2]),'priority':0,'source':f'{SOURCE}#L{line}'}],
                         'daily_premium':None,'weekend_multiplier':[1,1],'volume_discounts':[],
                         'daily_cap':None if r[3]=='—' else int(r[3].split()[0]),
                         'facility_multipliers':{},'tier_multipliers':{},'support':'supported','refs':[f'{SOURCE}#L{line}']})
    by_name={s['name']:s for s in services}
    for line,r in t[5]:
        s=by_name[r[0]];s['daily_premium']={'exceeds':int(r[1].split()[0]),'multiplier':[100+int(r[2].strip('+%')),100],'source':f'{SOURCE}#L{line}'};s['refs'].append(f'{SOURCE}#L{line}')
    for line,r in t[6]:
        s=by_name[r[0]];s['weekend_multiplier']=[100+int(r[1].strip('+%')),100];s['refs'].append(f'{SOURCE}#L{line}')
    for line,r in t[7]:
        s=by_name[r[0]];s['volume_discounts'].append({'exceeds':int(r[1].split()[0]),'multiplier':[100-int(r[2].strip('%')),100],'source':f'{SOURCE}#L{line}'});s['refs'].append(f'{SOURCE}#L{line}')
    for line,r in t[8]:
        assert by_name[r[0]]['daily_cap']==int(r[1].split()[0]),'Conflicting cap tables'
        by_name[r[0]]['refs'].append(f'{SOURCE}#L{line}')
    bundles=[{'a':by_name[r[0]]['id'],'b':by_name[r[1]]['id'],'a_cents':cents(r[2]),'b_cents':cents(r[3]),'source':f'{SOURCE}#L{ln}'} for ln,r in t[9]]
    exclusions=[{'service':by_name[r[0]]['id'],'anchor':by_name[r[2]]['id'],'days':int(r[1].split()[0]),'source':f'{SOURCE}#L{ln}'} for ln,r in t[10]]
    c={'schema_version':'2','semantics_version':'2','hospital':'H1','contract_number':'INS-H1-2024-0417','term':['2024-01-01','2025-12-31'],
       'review_state':'candidate','source_hashes':{SOURCE:digest(ROOT/SOURCE)},
       'semantics':{'rounding':'half_up_cent','adjustment_order':['bundle','facility','tier','daily_premium','weekend_uplift','volume_discount'],
                    'service_day':'calendar','exclusion_direction':'both','exclusion_boundary':'uncertain_at_equal',
                    'duplicate_policy':'abstain_repeated_service_day','cap_policy':'single_line_cap_otherwise_abstain',
                    'invoice_eligibility':'supplied_invoice_facts','service_date_not_after_invoice':True,'facility_source':'none','volume_basis':'contract_term_all_patients_strict_prior_billed_units','version_precedence':'single',
                    'refs':[f'{SOURCE} §§1–3, 5.1, 7.1–7.2, 9.1, 10.1, 11']},
       'services':services,'bundles':bundles,'exclusions':exclusions,
       'coverage':[
           {'source':f'{SOURCE} §1','state':'accepted','representation':'contract identity/term, identity facility and tier multipliers','qualification':'No external clinical eligibility inferred.'},
           {'source':f'{SOURCE} §2','state':'accepted','representation':'calendar service day; weekend; stated units; prior-only billed usage','qualification':'Invalid dates remain unknown, never repaired.'},
           {'source':f'{SOURCE} §3','state':'accepted','representation':'ordered exact half-up adjustments then billed quantity; invoice sum','qualification':'A wrong billed unit label does not authorize an invented quantity conversion.'},
           {'source':f'{SOURCE} §4','state':'accepted','representation':'all 108 transcribed names, unit bases, rates and table caps','qualification':'Mapping identity is reviewed separately.'},
           {'source':f'{SOURCE} §5','state':'accepted','representation':'9 strict daily aggregate threshold premiums','qualification':'Unknown same-patient/service/day quantities propagate.'},
           {'source':f'{SOURCE} §6','state':'accepted','representation':'7 weekend uplifts','qualification':'Service date required.'},
           {'source':f'{SOURCE} §7','state':'accepted','representation':'11 discount thresholds; deepest qualifying tier; all-patient/term strict-prior date/line-ID order','qualification':'Known billed quantities remain in history even for omitted invoices; uncertain identity/date has bounded/unbounded possible contribution.'},
           {'source':f'{SOURCE} §8','state':'accepted','representation':'7 daily caps','qualification':'Only single-line allocation is claimed; repeated service/day billing is withheld.'},
           {'source':f'{SOURCE} §9','state':'accepted','representation':'3 patient-day bundle pairs before further adjustments','qualification':'Unknown partner presence is propagated.'},
           {'source':f'{SOURCE} §10','state':'unresolved','representation':'6 exclusions, explicitly both temporal directions','qualification':'Same-patient scope is the adopted contractual-context interpretation; exact “within N days” equality is withheld. Missing date/anchor facts block only relevant opinions.'},
           {'source':f'{SOURCE} §11','state':'accepted','representation':'contract quote, unique invoice ID, service/term/invoice dates, repeated service/patient/day check','qualification':'Conflicting-ID totals, missing corrected dates and duplicate allocation are withheld rather than guessed.'}
       ]}
    proposals=json.loads((ROOT/'mappings/H1.candidates.raw.json').read_text())['proposals']
    from insurance_audit.resolve import normalize
    combined={}
    for description,candidates in proposals.items():
        key=normalize(description);sid=by_name[candidates[0]]['id'] if len(candidates)==1 else None
        ids=[by_name[n]['id'] for n in candidates]
        grade='unresolved'
        if sid:
            full=set(words(candidates[0]));expanded=set().union(*(set(LEXICON.get(w,[w])) for w in words(description)))
            grade='explicit' if full<=expanded else 'elided'
        row={'key':key,'raw_descriptions':[description],'state':'accepted' if sid else 'unresolved','service_id':sid,'candidates':ids,'grade':grade,
             'evidence':['Work model reviewed grouped H1 proposals against complete §4 catalog and lexicon_v1.json; no label, billed rate or unit used.',
                         'Unique semantic token candidate within the supplied hospital catalog.' if sid else 'Multiple or no defensible catalog candidates; identity remains unresolved.']}
        if key in combined:
            assert combined[key]['service_id']==sid and combined[key]['candidates']==ids,'Normalization collision'
            combined[key]['raw_descriptions'].append(description)
        else:combined[key]=row
    m={'schema_version':'2','hospital':'H1','review_state':'candidate','normalizer_version':'2','records':[combined[k] for k in sorted(combined)]}
    validate_contract(c);validate_mappings(m,c)
    write_json(ROOT/'contracts/hospital_1.raw.json',c);write_json(ROOT/'mappings/hospital_1.raw.json',m)
    write_json(ROOT/'reports/h1_acquisition_manifest.json',{'mode':'Work-session model-authored interpretation with deterministic table transcription aid; not a model API call',
               'sources':c['source_hashes'],'prompts':{p:digest(ROOT/p) for p in ['prompts/extract_v1.md','prompts/review_v1.md','prompts/map_v1.md']},
               'raw_contract_sha256':digest(ROOT/'contracts/hospital_1.raw.json'),'raw_mapping_sha256':digest(ROOT/'mappings/hospital_1.raw.json'),
               'semantics_authoring':'tools/acquire_h1.py contains the visible finite data interpretation, not generated per-contract pricing functions.',
               'mapping_review_input':'mappings/H1.candidates.raw.json'} )
    print(json.dumps({'services':len(services),'premiums':len(t[5]),'weekend':len(t[6]),'discount_tiers':len(t[7]),'caps':len(t[8]),'bundles':len(bundles),'exclusions':len(exclusions),'mapping_records':len(m['records'])}))


if __name__=='__main__':acquire()
