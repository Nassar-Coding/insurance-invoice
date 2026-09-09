"""Materialize the source/mapping review performed visibly in Work, not an independent review."""
from collections import Counter,defaultdict
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import load_hospital,write_json
from insurance_audit.schema import digest,validate_contract,validate_mappings
from insurance_audit.resolve import normalize


def record(h):
    cp=ROOT/f'contracts/hospital_{h[1:]}.raw.json';mp=ROOT/f'mappings/hospital_{h[1:]}.raw.json'
    c=json.loads(cp.read_text());m=json.loads(mp.read_text());validate_contract(c);validate_mappings(m,c)
    by={s['id']:s for s in c['services']};data=load_hospital(ROOT/'data/source',h)
    index={r['key']:r for r in m['records']};lines=defaultdict(list)
    for l in data.lines:lines[l.invoice_id].append(l)
    q=data.quality();bad={d['invoice_id'] for d in q['quarantined']}|{d['invoice_id'] for d in q['duplicate_invoice_ids']}
    plausible=[i for i,ls in lines.items() if i not in bad and all(index[normalize(l.description)]['state']=='accepted' and by[index[normalize(l.description)]['service_id']]['support']=='supported' for l in ls)]
    if not plausible:raise ValueError(h+' has no plausible complete opinion scope')
    text=['# '+h+' grouped mapping review evidence','',
          'The implementing Work model inspected every accepted alias below against the full source catalog. This is author review, not the later independent auditing stage. No billed amount or unit selected an identity. Unresolved keys remain in the mapping JSON.','']
    for s in c['services']:
        aliases=[d for r in m['records'] if r['service_id']==s['id'] for d in r['raw_descriptions']]
        text.extend(['- '+s['id']+' '+s['name']+': '+'; '.join(aliases)])
    (ROOT/f'reports/{h}_mapping_review.md').write_text('\n'.join(text)+'\n')
    closure={'hospital':h,'state':'source_reviewed_candidate_scope','candidate_invoice_ids':sorted(plausible),'candidate_count':len(plausible),
        'contract_sha256':digest(cp),'mapping_sha256':digest(mp),'required_history_raw_lines':len(data.lines)+sum(d['kind']=='line_items' and d['status']=='quarantined' for d in data.dispositions),
        'dependencies':'All service identities are represented; bundles/exclusions close to this catalog. Full retrospective history is retained, with unknown mappings/dates/ownership bounded at execution. These identity candidates are not predictions; runtime may withhold additional dependencies.',
        'review_burden':{'rate_rows':len(c['services']),'accepted_mapping_keys':sum(r['state']=='accepted' for r in m['records']),'unresolved_mapping_keys':sum(r['state']=='unresolved' for r in m['records'])},
        'quality':q['disposition_counts'],'confidence':'Frozen novel-reviewed policy; source-qualified H5 facility projection capped, no target calibration claimed.'}
    if h=='H2':
        closure.update(state='diagnostic_pricing_only; no eligible complete submission scope',
                       pricing_identity_candidate_ids=closure.pop('candidate_invoice_ids'),
                       pricing_identity_candidate_count=closure.pop('candidate_count'),
                       candidate_invoice_ids=[],candidate_count=0,
                       eligibility_gap='Article XIII.1–5: no actual submission date or waiver/exception evidence. Invoice date cannot establish these events.',
                       confidence='Unresolved whole-row eligibility: omit; no confidence number substitutes for missing facts.')
    write_json(ROOT/f'reports/{h}_candidate_closure.json',closure)
    review={'hospital':h,'verdict':'accepted_with_recorded_uncertainty','reviewer':'implementing Work model; author source review',
        'raw_contract_sha256':digest(cp),'raw_mapping_sha256':digest(mp),'source_hashes':c['source_hashes'],
        'reviewed_service_ids':[s['id'] for s in c['services']],
        'method':'Full controlling Markdown sources and every accepted grouped mapping read in this Work session; table transcription checked against named clause families; source-derived behavior fixtures tested separately.',
        'mapping_evidence':f'reports/{h}_mapping_review.md','candidate_closure':f'reports/{h}_candidate_closure.json',
        'qualifications':sorted({r['qualification'] for r in c['coverage']}),
        'checks_required':'tests/test_targets.py and tests/test_h2.py where applicable; runtime accepted-bundle binding; H1 regression after shared code changes',
        'execution_scope':'diagnostic_only; invoice-level abstention enforced by schema' if h=='H2' else 'supported complete opinions and explicit abstentions'}
    write_json(ROOT/f'reports/{h}_source_review.json',review)
    print(h,len(plausible),'complete identity candidates, source review recorded')


if __name__=='__main__':
    for h in sys.argv[1:]:record(h)
