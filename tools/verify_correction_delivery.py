"""Verify one corrected artifact state; optional ZIP check performs no writes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest
from insurance_audit.submission import verify_submission


def read(path):return json.loads((ROOT/path).read_text())


parser=argparse.ArgumentParser();parser.add_argument('--archive',type=Path);args=parser.parse_args()
release=read('reports/release_manifest.json');clean=read('reports/reproduction_check.json')
completion=read('reports/implementation_completion.json');consistency=read('reports/corrections/audit_1/report_consistency.json')
tests=read('reports/tests_final.json');manifest=verify_submission(ROOT)
assert completion['state']=='CORRECTIONS COMPLETE - READY FOR INDEPENDENT CLOSURE RE-AUDIT'
assert completion['subtask_counts']=={'Completed and verified':65,'Not started':4}
assert consistency['report_sha256']==digest(ROOT/'reports/implementation_report.md')
assert consistency['submission_sha256']==manifest['submission_sha256']==digest(ROOT/'submission.csv')
assert consistency['release_manifest_sha256']==clean['release_manifest_sha256']==digest(ROOT/'reports/release_manifest.json')
assert clean['status']=='passed' and all(clean['full_hospital_outputs_equal'].values())
assert tests['success'] and tests['tests_run']==clean['tests']['tests_run']
assert tests['tested_files']==clean['tests']['tested_files']
for path,sha in tests['tested_files'].items():assert digest(ROOT/path)==sha,path
for path,sha in release['evaluation_testing_and_documentation_inputs'].items():assert digest(ROOT/path)==sha,path
for path,sha in release['stable_outputs'].items():assert digest(ROOT/path)==sha,path
for role in ['H1','targets']:
    for path,sha in release['prediction_inputs'][role]['files'].items():assert digest(ROOT/path)==sha,path
changed=subprocess.check_output(['git','diff','--name-only',clean['tested_commit']],cwd=ROOT,text=True).splitlines()
protected=('src/','tests/','contracts/','mappings/','evaluation/','data/source/','prompts/')
assert not [p for p in changed if p.startswith(protected) or p in {'.python-version','requirements.txt'}],changed
quality=read('reports/gate_status.json')['quality_gates']
assert sum(g['applicability']=='implementation' and g['status']=='Completed and verified' for g in quality)==17
report={'status':'passed','stage':'author audit correction; independent closure re-audit and publishing pending',
    'clean_replay_commit':clean['tested_commit'],'current_local_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'test_count':tests['tests_run'],'subtasks_verified':65,'later_tasks_not_started':4,'implementation_quality_gates_verified':17,
    'current_submission_sha256':manifest['submission_sha256'],'implementation_report_sha256':consistency['report_sha256'],
    'release_input_and_output_hashes':'all matched','post_replay_tracked_changes':changed,
    'change_class':'evidence/status/report and checkpoint packaging changes only after clean replay; decision inputs and tests unchanged'}
if args.archive:
    with zipfile.ZipFile(args.archive) as archive:
        proof=json.loads(archive.read('CHECKPOINT_VERIFICATION.json'))
        archived=json.loads(archive.read('CHECKPOINT_MANIFEST.json'))
        assert proof['status']=='passed' and not proof['mismatches']
        assert proof['manifest_sha256']==hashlib.sha256(archive.read('CHECKPOINT_MANIFEST.json')).hexdigest()
        assert proof['restored_git_head']==report['current_local_commit']
        for path in ['submission.csv','reports/implementation_report.md','reports/release_manifest.json',
                     'reports/implementation_completion.json','reports/final_delivery_check.json']:
            payload=archive.read('insurance_audit_project/'+path)
            assert payload==(ROOT/path).read_bytes(),path+' differs between ZIP and current project'
            assert archived[path]==hashlib.sha256(payload).hexdigest()
        assert proof['report_sha256']==report['implementation_report_sha256']
        assert proof['submission_sha256']==report['current_submission_sha256']
        report['archive']={'sha256':digest(args.archive),'bytes':args.archive.stat().st_size,
                           'restored_project_files':proof['files_verified'],'standalone_report_and_csv_match_zip':True}
else:
    write_json(ROOT/'reports/final_delivery_check.json',report)
print(json.dumps(report,indent=2))
