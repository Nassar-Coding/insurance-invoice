"""Bind the governing tasks to real implementation evidence, preserving the workbook."""
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.batch import current_run,canonical_hash
from insurance_audit.schema import digest
from insurance_audit.submission import verify_submission

tests=json.loads((ROOT/'reports/tests_final.json').read_text())
assert tests['success'] and not tests['failures'] and not tests['errors']
assert all((ROOT/p).is_file() and digest(ROOT/p)==sha for p,sha in tests['tested_files'].items()),'Tested code changed'
assert set(tests['tested_files'])=={str(p.relative_to(ROOT)) for base in ['src','tests'] for p in (ROOT/base).rglob('*.py')},'Untested file added'
regression=json.loads((ROOT/'reports/final_regression.json').read_text());assert regression['status']=='passed'
assert json.loads((ROOT/'reports/provenance_check.json').read_text())['status']=='passed'
guard=json.loads((ROOT/'reports/guarded_reproduction.json').read_text());assert guard['status']=='passed'
corrections=json.loads((ROOT/'reports/corrections/audit_1/correction_verification.json').read_text())
assert corrections['status']=='passed' and set(corrections['findings'])=={'AUD-01','AUD-02'}
assert all(digest(ROOT/p)==sha for p,sha in corrections['verified_tool_hashes'].items()),'Correction verifier changed'
for group,hospitals in [('H1',['H1']),('H2-H3-H4-H5',['H2','H3','H4','H5'])]:
    directory,current=current_run(ROOT,hospitals)
    verified=corrections['current_runs'][group]
    assert verified['identity']==current['identity'] and verified['attempt']==current['attempt'],'Correction evidence is stale'
    assert guard['execution']['h1_attempt' if group=='H1' else 'target_attempt']==current['attempt'],'Guarded replay is stale'
    for h in hospitals:
        result=json.loads((directory/f'{h}.json').read_text())
        assert regression['shuffle_checks'][h]['result_sha256_canonical']==canonical_hash(result),'Permutation evidence is stale'
docs=json.loads((ROOT/'reports/document_checks.json').read_text());assert docs['visual_inspection']['status']=='passed'
for name in ['decision_log','submission_writeup']:
    assert digest(ROOT/docs[name]['file'])==docs[name]['sha256'],'Rendered document changed'
    assert digest(ROOT/f'reports/{name}.md')==docs[name]['markdown_sha256'],'Document text changed'
submission=verify_submission(ROOT)
clean_path=ROOT/'reports/reproduction_check.json'
clean=json.loads(clean_path.read_text()) if clean_path.exists() else {'status':'not_started'}
clean_pass=(clean['status']=='passed' and clean['tests']['tested_files']==tests['tested_files']
            and clean.get('release_manifest_sha256')==digest(ROOT/'reports/release_manifest.json')
            and all(digest(ROOT/p)==sha for p,sha in clean['checksums']['actual'].items()))

evidence={
'ST01.01':['governance/overrides.md','docs/budget.json','docs/work_log.md'],
'ST01.02':['docs/source_manifest.json','docs/architecture.md','governance/Insurance_Auditing_Implementation_Ready.xlsx'],
'ST01.03':['docs/scope.md','docs/external_readiness.md','reports/current_candidate_closure.json'],
'ST01.04':['docs/decision_register.md','docs/implementation_changes.md','docs/ai_usage.md','prompts/README.md'],
'ST02.01':['reports/recovery_initial.json','reports/recovery_latest.json','docs/source_manifest.json'],
'ST02.02':['.python-version','requirements.txt','src/insurance_audit/__main__.py','docs/cli_contract.md','reports/guarded_reproduction.json'],
'ST02.03':['src/insurance_audit/io.py','tests/test_inputs.py','reports/input_quality.json','reports/tests_final.json'],
'ST02.04':['docs/input_contract.md','reports/input_quality.json','src/insurance_audit/context.py','reports/workload.json'],
'ST02.05':['reports/inventory_H1.json','reports/inventory_H2.json','reports/inventory_H3.json','reports/inventory_H4.json','reports/inventory_H5.json','reports/viability_H1.json','reports/viability_H3.json'],
'ST02.06':['evaluation/split_manifest.json','tests/test_inputs.py','reports/guarded_reproduction.json'],
'ST03.01':['docs/contract_schema.md','src/insurance_audit/schema.py'],
'ST03.02':['src/insurance_audit/schema.py','tests/test_schema.py','reports/tests_final.json','reports/provenance_check.json'],
'ST03.03':['src/insurance_audit/resolve.py','mappings/lexicon_v1.json','tests/test_schema.py','reports/H1_mapping_change_v2.json'],
'ST03.04':['prompts/extract_v1.md','prompts/review_v1.md','prompts/map_v1.md','prompts/map_v2.md','tests/test_schema.py'],
'ST03.05':['docs/contract_review_protocol.md','reports/provenance_check.json'],
'ST04.01':['contracts/hospital_1.raw.json','reports/h1_acquisition_manifest.json'],
'ST04.02':['contracts/hospital_1.json','reports/H1_source_review.json','reports/provenance_check.json'],
'ST04.03':['mappings/hospital_1.json','reports/H1_mapping_change_v2.json','mappings/archive/H1.accepted.v1.json'],
'ST04.04':['tests/fixtures/h1_contract_examples.json','tests/test_pricing.py'],
'ST04.05':['contracts/H1.bundle.json','reports/H1_candidate_closure.json','reports/current_candidate_closure.json'],
'ST05.01':['src/insurance_audit/resolve.py','src/insurance_audit/schema.py','tests/test_schema.py','tests/test_targets.py'],
'ST05.02':['src/insurance_audit/context.py','tests/test_pricing.py','reports/final_regression.json','docs/snapshot_revisions.md'],
'ST05.03':['src/insurance_audit/pricing.py','tests/test_pricing.py','tests/test_targets.py','tests/test_h2.py','reports/tests_final.json'],
'ST05.04':['src/insurance_audit/checks.py','tests/test_pricing.py','tests/test_targets.py','tests/test_h2.py'],
'ST05.05':['src/insurance_audit/audit.py','src/insurance_audit/submission.py','reports/current_candidate_closure.json','runs/current-H1.json','runs/current-H2-H3-H4-H5.json'],
'ST05.06':['reports/tests_final.json','reports/tests_final.txt','reports/regression_initial_failure.json','docs/implementation_changes.md'],
'ST05.07':['src/insurance_audit/batch.py','tests/test_batch.py','tests/test_submission.py','reports/final_regression.json','reports/tests_final.txt'],
'ST06.01':['src/insurance_audit/evaluation.py','tests/test_evaluation.py','reports/evaluation_report.md'],
'ST06.02':['runs/attempts/d0804aaa2af64ce2a8991289a9af941b/H1.evaluation.development.json','reports/evaluation_development.json'],
'ST06.03':['reports/H1_mapping_change_v2.json','docs/implementation_changes.md','reports/evaluation_report.md','tests/test_schema.py'],
'ST06.04':['evaluation/confidence_policy.json','evaluation/development_policy_evidence.json','src/insurance_audit/confidence.py','tests/test_confidence.py'],
'ST06.05':['reports/baseline_h1.json','runs/attempts/b62dc53945c74386b17c3279636d94c6/H1.evaluation.check.json','reports/evaluation_check.json','reports/evaluation_full.json'],
'ST06.06':['reports/baseline_h1.json','reports/final_regression.json'],
'ST07.01':['contracts/hospital_3.raw.json','reports/H3_acquisition_manifest.json'],
'ST07.02':['contracts/hospital_3.json','reports/H3_source_review.json','docs/implementation_changes.md'],
'ST07.03':['contracts/H3.bundle.json','reports/H3_source_review.json','reports/provenance_check.json'],
'ST07.04':['mappings/hospital_3.json','reports/H3_mapping_review.md'],
'ST07.05':['tests/test_targets.py','reports/tests_final.json','reports/final_regression.json'],
'ST07.06':['contracts/H3.bundle.json','reports/H3_candidate_closure.json','reports/current_candidate_closure.json','reports/workload.json'],
'ST08.01':['governance/overrides.md','docs/scope.md'],
'ST08.02':['contracts/hospital_5.raw.json','reports/H5_acquisition_manifest.json'],
'ST08.03':['contracts/hospital_5.json','reports/H5_source_review.json','docs/implementation_changes.md'],
'ST08.04':['mappings/hospital_5.json','reports/H5_mapping_review.md'],
'ST08.05':['contracts/H5.bundle.json','tests/test_targets.py','reports/current_candidate_closure.json','reports/workload.json'],
'ST08.06':['contracts/hospital_4.raw.json','reports/H4_acquisition_manifest.json'],
'ST08.07':['contracts/hospital_4.json','reports/H4_source_review.json','docs/implementation_changes.md'],
'ST08.08':['mappings/hospital_4.json','reports/H4_mapping_review.md'],
'ST08.09':['contracts/H4.bundle.json','tests/test_targets.py','reports/current_candidate_closure.json','reports/workload.json'],
'ST08.10':['contracts/hospital_2.raw.json','reports/H2_acquisition_manifest.json','reports/H2_reading_index.json','reports/H2_reading_remaining.txt'],
'ST08.11':['contracts/hospital_2.json','reports/H2_source_review.json','docs/implementation_changes.md'],
'ST08.12':['mappings/hospital_2.json','reports/H2_mapping_review.md'],
'ST08.13':['contracts/H2.bundle.json','tests/test_h2.py','reports/H2_candidate_closure.json','reports/current_candidate_closure.json'],
'ST08.14':['docs/scope.md','reports/workload.json','reports/current_candidate_closure.json'],
'ST09.01':['reports/final_regression.json','reports/provenance_check.json','reports/metrics.json','evaluation/confidence_policy.json'],
'ST09.02':['runs/current-H2-H3-H4-H5.json','reports/workload.json','reports/execution.json'],
'ST09.03':['submission.csv','src/insurance_audit/submission.py','runs/current-submission.json'],
'ST09.04':['runs/current-submission.json','tests/test_submission.py','reports/guarded_reproduction.json','reports/final_regression.json'],
'ST09.05':['reports/release_manifest.json','reports/workload.json','reports/current_candidate_closure.json'],
'ST10.01':['reports/evaluation_report.md','reports/metrics.json'],
'ST10.02':['reports/decision_log.md','reports/decision_log.pdf','reports/document_checks.json'],
'ST10.03':['reports/submission_writeup.md','reports/submission_writeup.pdf','reports/document_checks.json'],
'ST10.04':['prompts/README.md','docs/ai_usage.md','reports/provenance_check.json','reports/h1_acquisition_manifest.json','reports/H2_acquisition_manifest.json','reports/H3_acquisition_manifest.json','reports/H4_acquisition_manifest.json','reports/H5_acquisition_manifest.json'],
'ST10.05':['README.md','docs/cli_contract.md','.python-version','requirements.txt','requirements-docs.txt'],
'ST10.06':['reports/reproduction_check.json','reports/reproduction_commands.txt'],
'ST10.07':['reports/release_manifest.json','reports/implementation_completion.json','governance/overrides.md'],
'ST11.01':['docs/external_readiness.md'],
'ST11.02':['docs/external_readiness.md'],
'ST11.03':['docs/external_readiness.md'],
'ST11.04':['docs/external_readiness.md']}
notes={
'ST01.01':'Original effort control is superseded by the explicit user override OVR-001; verified closure records the override, not compliance with an inactive limit.',
'ST02.05':'Original inventory/viability evidence is historical pre-engine evidence; final complete closures are separate. No effort-based scope limit remains.',
'ST04.03':'Initial mapping v1 is retained; v2 withdrew 39 missing-essential-qualifier keys after one observed development error. Final accepted keys=407; unresolved=63.',
'ST05.07':'Initial full permutation failure affected only duplicate-header trace order. D015 and a targeted test retain the cause; all five full results now agree after permutation.',
'ST06.02':'First development result and final development result are both preserved. Later regression does not retroactively claim that the check is unexposed.',
'ST06.05':'First check followed policy/mapping freeze. The current check is explicitly a regression after exposure; full H1 is development-inclusive.',
'ST08.01':'All additional hospitals activated by OVR-001; no timing or effort condition limits work.',
'ST08.05':'H5 accepted subset=128 complete opinions. All 128 have outcome-relevant invoice-facility projection and disclosed .65 policy confidence; no target accuracy claim.',
'ST08.09':'H4 accepted subset=64 complete opinions; patient-scope ambiguity is bounded, and outcome-dependent cases are omitted.',
'ST08.13':'Scope-disposition task completed: H2 diagnostic rules/mappings are implemented and tested, but no complete payable scope is accepted. Admission/discharge dates are present; missing actual submission, detailed episode/leave and possible exception evidence enforce 1,125 omissions. This does not claim full H2 pricing coverage or require user action for the implemented omission route.',
'ST08.14':'H2 is processed for diagnostics/omissions but inactive for submission; H3/H4/H5 accepted subsets supply 340 rows. D014 explains this precise batch/scope distinction.',
'ST10.04':'Authentic retained instruction files, historical raw outputs and author review are disclosed. No fabricated external model transcript, independent review, exact proprietary endpoint or hidden-session replay dependency.',
'ST10.07':'The first independent implementation audit is retained. Its two findings are corrected and author regression-verified; independent closure re-audit and BT11 external publication/delivery remain pending. No original-effort compliance claim.'}
affected=['ST02.03','ST02.04','ST05.02','ST05.05','ST05.06','ST05.07','ST06.05',
          'ST09.01','ST09.02','ST09.03','ST09.04','ST09.05','ST10.01','ST10.02','ST10.03','ST10.04','ST10.06','ST10.07']
for ident in affected:
    evidence[ident]+=['tests/test_audit_corrections.py','reports/corrections/audit_1/correction_verification.json']
    notes[ident]=notes.get(ident,'')+' AUD-01/AUD-02 reopened this task. Closure is bound to corrected tests, current-run before/after evidence and affected regression checks, not the historical pass.'
plan=json.loads((ROOT/'governance/plan.json').read_text());status=[]
for row in plan:
    ident=row['Subtask ID'];state='Not started' if ident.startswith('ST11.') else 'Completed and verified'
    if ident in {'ST10.06','ST10.07'} and not clean_pass:state='In progress'
    available=[p for p in evidence[ident] if (ROOT/p).exists()]
    if state=='Completed and verified' and ident!='ST10.07':assert len(available)==len(evidence[ident]),(ident,set(evidence[ident])-set(available))
    status.append({'subtask_id':ident,'big_task_id':row['Big Task ID'],'name':row['Subtask Name'],'status':state,
        'governing_completion_condition':row['Completion Condition'],'evidence':available,
        'notes':notes.get(ident,'Later publishing/delivery action; outside this authorized implementation stage and not a local blocker.' if ident.startswith('ST11.') else 'Completed against the cited source, executed artifacts and current verification evidence. Provisional evidence filenames are mapped to actual project paths.')})
assert len(status)==69
write_json(ROOT/'reports/implementation_status.json',status)

gates=json.loads((ROOT/'governance/gates.json').read_text());big=[];quality=[]
for r in gates['Big Task Gates']:
    if not (isinstance(r[0],str) and r[0].startswith('BT')):continue
    children=[s for s in status if s['big_task_id']==r[0]]
    state='Completed and verified' if all(s['status']=='Completed and verified' for s in children) else 'Not started' if r[0]=='BT11' else 'In progress'
    big.append({'id':r[0],'name':r[1],'governing_final_gate':r[-2],'status':state,
                'subtasks':[s['subtask_id'] for s in children],
                'qualification':'OVR-001 supersedes effort constraints. H2 closure is explicit inactive submission scope. First independent audit completed; corrected state awaits independent closure re-audit. External publication remains later.'})
q_evidence={1:['reports/provenance_check.json','tests/test_schema.py'],2:['reports/workload.json','tests/test_inputs.py'],3:['reports/workload.json','tests/test_pricing.py'],
4:['reports/H1_mapping_change_v2.json','tests/test_schema.py','tests/test_targets.py'],5:['reports/provenance_check.json','docs/implementation_changes.md'],
6:['tests/test_targets.py','tests/test_h2.py','docs/implementation_changes.md'],7:['tests/test_pricing.py','reports/final_regression.json'],
8:['tests/test_pricing.py','tests/test_targets.py','runs/current-submission.json'],9:['tests/test_batch.py','tests/test_submission.py','reports/guarded_reproduction.json'],
10:['reports/metrics.json','reports/baseline_h1.json','reports/final_regression.json','reports/guarded_reproduction.json'],11:['reports/document_checks.json','runs/current-submission.json','docs/implementation_changes.md'],
12:['reports/reproduction_check.json','reports/reproduction_commands.txt'],13:['reports/final_regression.json','reports/release_manifest.json'],14:['reports/recovery_initial.json','reports/recovery_latest.json'],
15:['reports/workload.json','reports/guarded_reproduction.json'],16:['docs/snapshot_revisions.md','tests/test_pricing.py'],17:['prompts/extract_v1.md','tests/test_schema.py'],
18:['docs/external_readiness.md'],19:['README.md','docs/input_contract.md'],20:['README.md','docs/snapshot_revisions.md'],21:['docs/implementation_changes.md'],22:['README.md','data/source/README.md']}
for n in [2,3,7,9,10,11,12,13,16]:
    q_evidence[n]+=['tests/test_audit_corrections.py','reports/corrections/audit_1/correction_verification.json']
for r in gates['Real-World Quality Gates']:
    if not (isinstance(r[0],str) and r[0].startswith('QG')):continue
    n=int(r[0][2:4]);applicable=n<=17
    state='Completed and verified' if applicable else 'Not started'
    if n==12 and not clean_pass:state='In progress'
    quality.append({'id':f'QG{n:02}','name':r[0],'governing_final_check':r[-3],
        'applicability':'implementation' if applicable else 'later submission' if n==18 else 'excluded mandatory production/alternate-pipeline requirement',
        'status':state,'evidence':[p for p in q_evidence[n] if (ROOT/p).exists()],
        'qualification':'No certification or unperformed operational capability is implied; see recorded source and confidence limitations.'})
write_json(ROOT/'reports/gate_status.json',{'big_tasks':big,'quality_gates':quality,
    'targeted_corrections':{'C01':['ST01.03','ST02.05'],'C02':['ST02.01'],'C03':['ST02.03'],'C04':['ST02.05','ST04.05'],'C05':['ST03.02'],'C06':['ST05.01'],'C07':['ST05.07','ST09.04'],'C08':['ST06.04'],'C09':['ST09.01'],'C10':['ST09.04']},
    'implementation_audit_corrections':{'AUD-01':{'decision':'Accept','author_status':'corrected and regression verified','gates':['QG02','QG03','QG07','QG09','QG16']},
                                      'AUD-02':{'decision':'Accept','author_status':'corrected and source/context verified','gates':['QG11','QG13']}},
    'external_prerequisites':'E01-E03 remain later publishing/access/sending tasks with original-message verification qualification; none is an implementation blocker.'})
completion={'state':'CORRECTIONS COMPLETE - READY FOR INDEPENDENT CLOSURE RE-AUDIT' if clean_pass else 'AUDIT CORRECTION REGRESSION VERIFICATION IN PROGRESS',
    'subtask_counts':dict(Counter(s['status'] for s in status)),'tests':{'run':tests['tests_run'],'failures':0,'errors':0,'skips':tests['skipped']},
    'submission_rows':submission['rows'],'submission_sha256':submission['submission_sha256'],
    'implementation_blockers_requiring_user_action':[],
    'coverage_limits':['H2 admission/discharge dates are present; complete opinions withheld for unobserved actual submission, detailed episode/leave and possible exception facts.','Other necessary service/context/correction uncertainties are explicit omissions.','Target accuracy/calibration is not established.'],
    'independent_audit':{'verdict':'PASS WITH CORRECTIONS','report':'governance/audits/independent_implementation_1/Insurance_Auditing_Independent_Implementation_Audit.md'},
    'author_correction_evidence':'reports/corrections/audit_1/correction_verification.json',
    'remaining_audit_findings':[],
    'not_started':['Independent closure re-audit','BT11 repository publication, assessor access, actual sending'],
    'clean_reproduction_tested_commit':clean.get('tested_commit'),
    'current_local_commit_at_recording':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'history_note':'Evidence/status/report-only commits after the replay do not imply the same commit ID. Decision-input and stable-output hashes are verified separately.'}
write_json(ROOT/'reports/implementation_completion.json',completion)
print(json.dumps(completion,indent=2))
