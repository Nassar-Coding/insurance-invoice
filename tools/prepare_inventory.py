"""Acquisition aid: provisional name candidates, not accepted mapping or pricing."""
import json
import re
import sys
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import load_hospital,write_json

LEXICON=json.loads((ROOT/'mappings/lexicon_v1.json').read_text())


def words(description):
    text=re.sub(r'\s*/(?:NG|SA|RM|CW|PH)-\d+\s*$','',description,flags=re.I).lower()
    return re.findall(r'[a-z0-9]+',text)


def names(hospital):
    paths={'H1':['hospital_1/provider_services_agreement.md'],
           'H3':['hospital_3/appendix_b_rate_schedule.md','hospital_3/amendment_no_1.md']}[hospital]
    result=set()
    for relative in paths:
        text=(ROOT/'data/source/contracts'/relative).read_text()
        if hospital=='H1':text=text.split('## 4. Rate Schedule')[1].split('## 5.')[0]
        for line in text.splitlines():
            cells=[v.strip() for v in line.strip('|').split('|')]
            if line.startswith('|') and len(cells)>=3 and cells[1].startswith('per ') and 'GBP ' in cells[2]:result.add(cells[0])
    return sorted(result)


def candidates(description,catalog):
    tokens=words(description)
    options=[set(LEXICON.get(w,[w])) for w in tokens]
    return [name for name in catalog if options and all(set(words(name))&opt for opt in options)]


def prepare(hospital):
    data=load_hospital(ROOT/'data/source',hospital);catalog=names(hospital)
    # Include quarantined descriptions in mapping/context review too.
    descs={l.description for l in data.lines}
    for d in data.dispositions:
        if d['kind']=='line_items' and len(d['raw'])==9:descs.add(d['raw'][4])
    proposed={d:candidates(d,catalog) for d in sorted(descs)}
    by_invoice=defaultdict(list)
    for l in data.lines:by_invoice[l.invoice_id].append(l)
    quality=data.quality();bad={r['invoice_id'] for r in quality['duplicate_invoice_ids']}
    bad.update(d['invoice_id'] for d in quality['quarantined'])
    plausible=[key for key,rows in by_invoice.items() if key not in bad and all(len(proposed[r.description])==1 for r in rows)]
    report={'hospital':hospital,'catalog_services':len(catalog),'distinct_descriptions_including_quarantine':len(proposed),
            'description_candidate_counts':dict(Counter(len(v) for v in proposed.values())),
            'provisional_complete_identity_candidate_ids':sorted(plausible),'provisional_complete_identity_count':len(plausible),
            'required_history_line_count':len(data.lines)+sum(d['kind']=='line_items' and d['status']=='quarantined' for d in data.dispositions),
            'root_causes':['ambiguous/unknown service description','conflicting invoice ownership/total','invalid dates',
                           'daily duplicate/cap allocation','exclusion direction/boundary','history tier uncertainty'],
            'review_work':{'catalog_rows':len(catalog),'unique_description_decisions':len(proposed),
                           'unresolved_descriptions':sum(len(v)!=1 for v in proposed.values())},
            'qualification':'These are provisional lexical candidates, not approved mappings or opinions. All general rules and relevant context must be reviewed. No labels or billed prices/units choose a service.'}
    write_json(ROOT/f'reports/viability_{hospital}.json',report)
    write_json(ROOT/f'mappings/{hospital}.candidates.raw.json',{'hospital':hospital,'lexicon':'lexicon_v1.json','catalog':catalog,'proposals':proposed})
    compact={k:v for k,v in report.items() if not k.endswith('_ids')}
    print(json.dumps(compact,indent=2))


if __name__=='__main__':
    for hospital in ['H1','H3']:prepare(hospital)
