"""Before/after regression evidence for the two independent audit corrections.

Requires the retained pre-correction attempts for comparison, unlike ordinary
README replay. No fitting, prediction alteration or independent re-audit occurs.
"""
from collections import Counter
import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tests'))
from insurance_audit.batch import current_run,canonical_hash
from insurance_audit.io import load_hospital,write_json
from insurance_audit.schema import load_bundle,digest
from insurance_audit.submission import TARGETS,validate_result,verify_submission
from inspect_bundle_traces import inspect,verify_emitted_stages
from test_audit_corrections import Snapshot

OUT=ROOT/'reports/corrections/audit_1';BEFORE=OUT/'before';AFTER=OUT/'after'
AFTER.mkdir(exist_ok=True)
baseline=json.loads((BEFORE/'baseline_manifest.json').read_text())
policy=json.loads((ROOT/'evaluation/confidence_policy.json').read_text())
for path,sha in baseline['retained_files'].items():
    # Keys are repository-relative paths into the preserved before/ folder.
    assert digest(ROOT/path)==sha,(path,'baseline evidence changed')

# Preserve the exact auditor-supplied probe's stdout on corrected code.
probe=subprocess.run([sys.executable,str(BEFORE/'auditor_aud01_reproduction.py')],cwd=ROOT,text=True,capture_output=True)
(AFTER/'auditor_aud01_reproduction.txt').write_text(probe.stdout+probe.stderr)
assert probe.returncode==0
fixture=Snapshot();cases=[]
for malformed in [False,True]:
    changes={'invoice_date':'2024-02-30'} if malformed else {}
    data,result,validation=fixture.run(*fixture.exclusion_fixture(**changes))
    assert not result['opinions']
    assert {a['invoice_id'] for a in result['abstentions']}=={'I1','I2'}
    assert result['abstentions'][0]['reasons'][0]['reason']=='unresolved_exclusion'
    record={'malformed_header':malformed,'result':result,'validation':validation,'input_quality':data.quality()}
    write_json(AFTER/f'aud01_{"malformed" if malformed else "valid"}_conflict.json',record)
    cases.append({'malformed_header':malformed,'I1_opinion':None,'I1_reason':'unresolved_exclusion',
                  'I2_disposition':'abstained','validation':validation})


def remove_bundle_metadata(value):
    """Ignore exactly AUD-02 metadata changes, including in uncertain diagnostics."""
    if isinstance(value,dict):
        if value.get('operation')=='bundle':return {'operation':'bundle','after':value['after']}
        return {k:remove_bundle_metadata(v) for k,v in value.items()}
    if isinstance(value,list):return [remove_bundle_metadata(v) for v in value]
    return value


def bundle_stages(value):
    if isinstance(value,dict):
        if value.get('operation')=='bundle':yield value
        for child in value.values():yield from bundle_stages(child)
    elif isinstance(value,list):
        for child in value:yield from bundle_stages(child)


def reason_names(result):
    return {a['invoice_id']:[(r['reason'],r.get('line_id')) for r in a['reasons']] for a in result['abstentions']}


pointers={};runs={};comparisons={};trace_checks={};tamper_checks=[]
for group,hospitals in [('H1',['H1']),('H2-H3-H4-H5',TARGETS)]:
    directory,status=current_run(ROOT,hospitals)
    pointers[group]=json.loads((ROOT/f'runs/current-{group}.json').read_text())
    runs[group]={'run_id':status['run_id'],'attempt':status['attempt'],'identity':status['identity'],
                 'outputs':status['outputs']}
    assert pointers[group]['attempt']!=baseline['current_pointers'][group]['attempt']
    for hospital in hospitals:
        old_directory=ROOT/'runs'/baseline['current_pointers'][group]['path']
        old=json.loads((old_directory/f'{hospital}.json').read_text())
        new=json.loads((directory/f'{hospital}.json').read_text())
        contract,maps,bundle=load_bundle(ROOT,hospital);data=load_hospital(ROOT/'data/source',hospital)
        validate_result(new,data,policy)
        assert old['opinions']==new['opinions'],hospital+' opinion/amount/category/confidence changed'
        assert old['accounting']==new['accounting'],hospital+' count changed'
        assert reason_names(old)==reason_names(new),hospital+' omission reason changed'
        stripped_old=remove_bundle_metadata(old);stripped_new=remove_bundle_metadata(new)
        assert stripped_old==stripped_new,hospital+' unexpected non-bundle-trace change'
        old_stages=list(bundle_stages(old));new_stages=list(bundle_stages(new))
        assert len(old_stages)==len(new_stages)
        comparisons[hospital]={'before_attempt':baseline['current_pointers'][group]['attempt'],
            'after_attempt':status['attempt'],'opinion_records_identical':True,
            'omitted_ids_and_reason_categories_identical':True,'accounting_identical':True,
            'all_result_fields_except_declared_bundle_metadata_identical':True,
            'semantic_result_sha256':canonical_hash(stripped_new),
            'opinion_records_sha256':canonical_hash(new['opinions']),
            'confidence_counts':dict(sorted(Counter(str(r['confidence']) for r in new['opinions']).items())),
            'changed_trace_invoices':sum(a!=b for a,b in zip(old['traces'],new['traces'])),
            'changed_abstention_detail_records':sum(a!=b for a,b in zip(old['abstentions'],new['abstentions'])),
            'bundle_stage_occurrences_with_new_metadata':sum(a!=b for a,b in zip(old_stages,new_stages)),
            'occurrence_note':'Counts include nested stages in uncertain diagnostics; the same diagnostic can appear in trace and abstention records.',
            'quarantined_invoice_headers':len(data.quarantined_headers()),'counts':new['accounting']}
        trace_checks[hospital]=verify_emitted_stages(ROOT,new,data,contract,maps)
        if hospital=='H4':
            example=next(t for t in new['traces'] if t['invoice_id']=='INV-H4-000583')
            write_json(AFTER/'aud02_H4_example.json',example)
            for mutation in ['wrong_source','wrong_context','wrong_bundle_cents']:
                fake={'traces':[copy.deepcopy(example)]}
                item=next(l for l in fake['traces'][0]['lines'] if l['line_id']=='H4-L00583-03')
                stage=next(s for s in item['pricing']['stages'] if s['operation']=='bundle')
                if mutation=='wrong_source':stage['source']=item['source_refs']
                elif mutation=='wrong_context':stage['rules'][0]['context_index']=99999
                else:stage['rules'][0]['substituted_cents']+=1
                try:verify_emitted_stages(ROOT,fake,data,contract,maps)
                except (AssertionError,IndexError):tamper_checks.append({'mutation':mutation,'rejected':True})
                else:raise AssertionError('Trace verification accepted '+mutation)

inventory=inspect(ROOT,pointers)
old_inventory=json.loads((BEFORE/'bundle_trace_inventory.json').read_text())
assert inventory['counts']==old_inventory['counts']
assert (inventory['lines'],inventory['invoices'],inventory['target_lines'],inventory['target_invoices'])==(352,151,252,103)
for row in inventory['rows']:
    assert row['required_source'] in row['source']
    assert any(e['rule_index']==row['bundle_index'] and e['source']==row['required_source'] and e['presence'] is True for e in row['stage']['rules'])
write_json(AFTER/'bundle_trace_inventory.json',inventory)

stable={}
for name in ['submission.csv','metrics.json','workload.json']:
    current=ROOT/name if name=='submission.csv' else ROOT/'reports'/name
    stable[name]={'before':digest(BEFORE/name),'after':digest(current),'byte_identical':(BEFORE/name).read_bytes()==current.read_bytes()}
    assert stable[name]['byte_identical'],name+' unexpectedly changed'
release=verify_submission(ROOT)
report={'status':'passed','role':'author correction and regression verification; not independent closure re-audit',
    'audit_sha256':baseline['audit_sha256'],'before_git_commit':baseline['git_head'],
    'findings':{'AUD-01':{'decision':'Accept','status':'corrected and regression verified','counterexamples':cases},
                'AUD-02':{'decision':'Accept','status':'corrected and source/context verified',
                          **{k:v for k,v in inventory.items() if k!='rows'}}},
    'current_runs':runs,'hospital_comparisons':comparisons,'bundle_stage_checks':trace_checks,
    'trace_tamper_checks':tamper_checks,'stable_outputs':stable,'submission_rows':release['rows'],
    'evaluation_report_change':'H2 admission/discharge dates clarified; independent audit/correction stage history refreshed. Metrics unchanged.',
    'remaining_limitations':['No target labels or target accuracy claim.','No quarantined headers in supplied snapshot: AUD-01 behavior change is demonstrated with source-rule fixtures.',
        'Focused regressions are not proof for every arbitrary malformed input or rule combination.',
        'Source/context checks are author verification and do not replace independent closure re-audit.'],
    'verified_tool_hashes':{str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),ROOT/'tools/inspect_bundle_traces.py']}}
write_json(OUT/'correction_verification.json',report)
print(json.dumps({'status':report['status'],'findings':report['findings'],'byte_identical_outputs':stable,
                  'bundle_stage_checks':trace_checks,'trace_tamper_checks':tamper_checks},indent=2))
