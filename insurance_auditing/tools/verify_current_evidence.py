"""Current-input regression, source lineage, and full snapshot order checks."""
from collections import Counter
import json
from pathlib import Path
import random
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.audit import audit
from insurance_audit.batch import current_run, canonical_hash
from insurance_audit.confidence import assign_confidence
from insurance_audit.io import load_hospital,write_json
from insurance_audit.schema import load_bundle,digest
from insurance_audit.submission import FIELDS,TARGETS,validate_result,verify_submission

start=time.perf_counter();policy=json.loads((ROOT/'evaluation/confidence_policy.json').read_text())
baseline=json.loads((ROOT/'reports/baseline_h1.json').read_text())
old_dir=ROOT/'runs/attempts'/baseline['attempt'];h1,status=current_run(ROOT,['H1'])
old=json.loads((old_dir/'H1.json').read_text());current=json.loads((h1/'H1.json').read_text())
def projection(result):return [{k:r[k] for k in FIELDS} for r in result['opinions']]
if projection(old)!=projection(current):raise AssertionError('H1 decisions changed from the frozen evaluated baseline; investigate before claiming closure')
changed={p:{'before':baseline['decision_inputs']['files'].get(p),'after':sha} for p,sha in status['identity']['files'].items() if baseline['decision_inputs']['files'].get(p)!=sha}
metrics_equal={}
for group in ('development','check','full'):
    a=json.loads((old_dir/f'H1.evaluation.{group}.json').read_text())
    b=json.loads((ROOT/f'reports/evaluation_{group}.json').read_text())
    select=lambda r:{k:v for k,v in r.items() if k not in {'details','provenance'}}
    metrics_equal[group]=select(a)==select(b)
    assert metrics_equal[group],group
targets,_=current_run(ROOT,TARGETS);shuffle_checks={};closures={};provenance={}
for h in ['H1']+TARGETS:
    directory=h1 if h=='H1' else targets;result=json.loads((directory/f'{h}.json').read_text())
    c,m,b=load_bundle(ROOT,h);data=load_hospital(ROOT/'data/source',h)
    checked=validate_result(result,data,policy)
    random.Random(901+int(h[1:])).shuffle(data.invoices);random.Random(1107).shuffle(data.lines);random.Random(223).shuffle(data.dispositions)
    shuffled=audit(data,c,m);assign_confidence(shuffled,policy)
    if canonical_hash(result)!=canonical_hash(shuffled):
        differences=[]
        def compare(a,b,path=''):
            if len(differences)>=30:return
            if type(a)!=type(b):differences.append({'path':path,'before':a,'after':b});return
            if isinstance(a,dict):
                for k in sorted(set(a)|set(b)):
                    if k not in a or k not in b:differences.append({'path':path+'/'+k,'missing_key':True})
                    else:compare(a[k],b[k],path+'/'+k)
            elif isinstance(a,list):
                if len(a)!=len(b):differences.append({'path':path,'lengths':[len(a),len(b)]})
                else:
                    for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
            elif a!=b:differences.append({'path':path,'before':a,'after':b})
        compare(result,shuffled)
        failure={'status':'failed','hospital':h,'six_opinion_fields_equal':projection(result)==projection(shuffled),'first_differences':differences}
        write_json(ROOT/'reports/regression_initial_failure.json',failure)
        raise AssertionError(json.dumps(failure))
    shuffle_checks[h]={'status':'passed','result_sha256_canonical':canonical_hash(result),'all_result_fields_equal':True,**checked}
    review=json.loads((ROOT/f'reports/{h}_source_review.json').read_text())
    rawc=ROOT/f'contracts/hospital_{h[1:]}.raw.json';rawm=ROOT/f'mappings/hospital_{h[1:]}.raw.json'
    matches={'raw_contract':review['raw_contract_sha256']==digest(rawc),'raw_mapping':review['raw_mapping_sha256']==digest(rawm)}
    assert all(matches.values()),(h,matches)
    provenance[h]={'accepted_bundle_sha256':digest(ROOT/f'contracts/{h}.bundle.json'),'review_to_current_raw_hashes':matches,
                   'source_hashes':c['source_hashes'],'services':len(c['services']),
                   'clause_dispositions':dict(Counter(v['state'] for v in c['coverage'])),
                   'accepted_mapping_keys':sum(r['state']=='accepted' for r in m['records']),
                   'unresolved_mapping_keys':sum(r['state']=='unresolved' for r in m['records'])}
    closures[h]={'status':'diagnostic-only; all complete opinions withheld' if h=='H2' else 'accepted complete-opinion subset',
        'complete_opinions':len(result['opinions']),'opinion_ids':[r['invoice_id'] for r in result['opinions']],
        'omissions':len(result['abstentions']),'raw_context_occurrences':len(data.lines)+sum(d['kind']=='line_items' and d['status']=='quarantined' for d in data.dispositions),
        'run_id':json.loads((directory/'status.json').read_text())['run_id'],
        'schema_sha256':digest(ROOT/b['contract_path']),'mapping_sha256':digest(ROOT/b['mapping_path']),
        'interpretation':'See source review and docs/implementation_changes.md. H2 has no eligible submission scope; diagnostic processing is explicitly separated.'}
write_json(ROOT/'reports/final_regression.json',{'status':'passed','h1_six_fields_unchanged':True,'h1_metrics_equal':metrics_equal,
    'changed_decision_inputs':changed,'check_role':'Regression after previous reserved-check exposure, no refit or fresh holdout claim.',
    'confidence_impact':'H1 scores/support unchanged. Explicit .65 interpretation cap formalizes H5 D012; target scores remain judgment-based.',
    'shuffle_checks':shuffle_checks,'submission':verify_submission(ROOT)['submission_sha256'],'elapsed_seconds':round(time.perf_counter()-start,6)})
write_json(ROOT/'reports/current_candidate_closure.json',closures)
write_json(ROOT/'reports/provenance_check.json',{'status':'passed','hospitals':provenance,
    'historical_note':'Initial acquisition/viability reports retain their original hashes and counts. This report and current_candidate_closure bind final accepted packages; raw drafts and schema1 history are preserved.'})
print(json.dumps({'h1_baseline_equal':True,'h1_metrics_equal':metrics_equal,'shuffled_full_results_equal':list(shuffle_checks),'source_raw_bindings':'passed'},indent=2))
