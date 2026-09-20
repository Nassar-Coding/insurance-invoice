"""Materialize a documented author-reviewed package; does not perform source review."""
import argparse
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest,validate_contract,validate_mappings,load_bundle


def accept(hospital):
    number=int(hospital[1:]);cp=f'contracts/hospital_{number}.raw.json';mp=f'mappings/hospital_{number}.raw.json'
    rp=f'reports/{hospital}_source_review.json';review=json.loads((ROOT/rp).read_text())
    assert review['verdict']=='accepted_with_recorded_uncertainty'
    assert review['raw_contract_sha256']==digest(ROOT/cp) and review['raw_mapping_sha256']==digest(ROOT/mp)
    c=copy.deepcopy(json.loads((ROOT/cp).read_text()));m=copy.deepcopy(json.loads((ROOT/mp).read_text()))
    assert review['source_hashes']==c['source_hashes']
    assert set(review['reviewed_service_ids'])=={s['id'] for s in c['services']}
    c['review_state']=m['review_state']='accepted';validate_contract(c);validate_mappings(m,c)
    accepted_c=cp.replace('.raw','');accepted_m=mp.replace('.raw','')
    write_json(ROOT/accepted_c,c);write_json(ROOT/accepted_m,m)
    artifacts=[accepted_c,accepted_m,'mappings/lexicon_v1.json',rp]
    bundle={'hospital':hospital,'schema_version':c['schema_version'],'semantics_version':c['semantics_version'],
            'review_state':'accepted','contract_path':accepted_c,'mapping_path':accepted_m,
            'artifacts':{p:digest(ROOT/p) for p in artifacts},'source_hashes':c['source_hashes'],
            'review_evidence':[rp,f'reports/{hospital}_candidate_closure.json','docs/decision_register.md']}
    write_json(ROOT/f'contracts/{hospital}.bundle.json',bundle);load_bundle(ROOT,hospital)
    print(json.dumps({'hospital':hospital,'bundle':f'contracts/{hospital}.bundle.json','services':len(c['services']),
                      'accepted_mapping_keys':sum(r['state']=='accepted' for r in m['records']),
                      'unresolved_mapping_keys':sum(r['state']=='unresolved' for r in m['records'])}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('hospital',choices=['H1','H2','H3','H4','H5']);args=parser.parse_args();accept(args.hospital)
