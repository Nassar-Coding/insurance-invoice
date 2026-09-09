"""Explicit development-only policy derivation; not part of prediction replay."""
import json
import math
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest

r=json.loads((ROOT/'reports/evaluation_development.json').read_text())
assert r['provenance']['group']=='development'
groups={}
for grade in ['explicit','elided']:
    for flag in [0,1]:
        rows=[d for d in r['details'] if d['prediction'] and d['prediction']['mapping_evidence']==grade and d['prediction']['flagged']==flag]
        n=len(rows);success=sum(d['whole_row_success'] for d in rows)
        lower=None
        if n:
            p=success/n;z=1.96
            lower=(p+z*z/(2*n)-z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)
        value=min(.95 if grade=='explicit' else .9,lower) if n>=30 else .65
        groups[f'{grade}:{flag}']={'n':n,'successes':success,'wilson_95_lower':lower,'confidence':round(value,6),
                                 'basis':'conservative lower-bound score, not a proven probability calibration' if n>=30 else 'sparse policy judgment, not empirically calibrated'}
policy={'version':'1','minimum_empirical_n':30,'h1_groups':groups,'target_judgment':{'explicit':.8,'elided':.7},
        'outcome_invariant_cap':.65,'unresolved':'omit entire row','check_labels_used':False,
        'development_report_sha256':digest(ROOT/'reports/evaluation_development.json'),
        'development_run_id':r['provenance']['run_id'],
        'event':'flag correct and expected cents exact, with separately verified source billed total and traceable free-text diagnostics',
        'limitations':['No H2–5 labels exist; novel confidence values are policy judgments, never transferred empirical accuracy.',
                      'H1 patient groups share legitimate global utilisation; the check is not an independent external test.',
                      'Rare errors and explicit ambiguity are weakly supported even when emitted-row accuracy is high.']}
write_json(ROOT/'evaluation/confidence_policy.json',policy)
write_json(ROOT/'evaluation/development_policy_evidence.json',r)
print(json.dumps(policy,indent=2))
