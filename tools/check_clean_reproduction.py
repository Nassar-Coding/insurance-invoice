"""Clone the committed project, remove generated outputs, execute README commands."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.batch import current_run
from insurance_audit.schema import digest
from insurance_audit.submission import verify_submission

verify_submission(ROOT)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
comparison=['submission.csv','reports/metrics.json','reports/workload.json','reports/evaluation_report.md']
expected={p:digest(ROOT/p) for p in comparison};commands=[]
start=time.perf_counter()
with tempfile.TemporaryDirectory(prefix='insurance-clean-') as temp:
    clone=Path(temp)/'project'
    command=['git','clone','--quiet','--no-local',str(ROOT),str(clone)]
    result=subprocess.run(command,text=True,capture_output=True)
    commands.append({'argv':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    if result.returncode:raise RuntimeError(result.stderr)
    cloned_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=clone,text=True).strip()
    assert cloned_head==head
    removed=[]
    shutil.rmtree(clone/'runs');removed.append('runs/ (every historical/current result and release)')
    # Correction evidence also contains an old CSV and serialized before/after
    # results. Remove these comparison-only caches from the replay environment.
    correction_cache=clone/'reports/corrections'
    if correction_cache.exists():
        shutil.rmtree(correction_cache);removed.append('reports/corrections/ (audit before/after output caches)')
    for pattern in ('submission.csv','reports/metrics.json','reports/workload.json','reports/evaluation_*.json',
                    'reports/evaluation_report.md','reports/execution.json','reports/release_manifest.json'):
        for path in clone.glob(pattern):removed.append(str(path.relative_to(clone)));path.unlink()
    # No inherited credentials, model key, saved predictions,
    # system user site packages, or inherited PYTHONPATH are supplied.
    env={'PATH':str(Path(sys.executable).parent)+':/usr/bin:/bin','PYTHONPATH':'src',
         'PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'54321','LANG':'C.UTF-8'}
    for command in ([sys.executable,'-m','insurance_audit','reproduce'],
                    [sys.executable,'-m','insurance_audit','verify-submission'],
                    [sys.executable,'tools/run_checks.py','clean_clone']):
        run=subprocess.run(command,cwd=clone,env=env,text=True,capture_output=True)
        commands.append({'argv':command,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
        if run.returncode:
            write_json(ROOT/'reports/reproduction_check.json',{'status':'failed','tested_commit':head,'commands':commands})
            raise RuntimeError(run.stderr or run.stdout)
    actual={p:digest(clone/p) for p in comparison}
    matches={p:actual[p]==sha for p,sha in expected.items()}
    execution=json.loads((clone/'reports/execution.json').read_text())
    tests=json.loads((clone/'reports/tests_clean_clone.json').read_text())
    assert all(matches.values()),matches
    # The full deterministic release identity must agree; attempt IDs are separate.
    original_manifest=json.loads((ROOT/'reports/release_manifest.json').read_text())
    cloned_manifest=json.loads((clone/'reports/release_manifest.json').read_text())
    assert original_manifest==cloned_manifest,'Final manifest differs in clean clone'
    full_output_matches={};full_output_hashes={}
    for hospitals in [['H1'],['H2','H3','H4','H5']]:
        _,original_run=current_run(ROOT,hospitals);_,cloned_run=current_run(clone,hospitals)
        group='-'.join(hospitals)
        full_output_matches[group]=original_run['outputs']==cloned_run['outputs']
        full_output_hashes[group]={'expected':original_run['outputs'],'actual':cloned_run['outputs']}
    assert all(full_output_matches.values()),'Full trace/input-quality outputs differ in clean clone'
    report={'status':'passed','tested_commit':head,'clone_commit':cloned_head,
        'removed_outputs_before_execution':removed,'sanitized_environment_names':sorted(env),
        'inherited_credentials':False,'cached_predictions_available':False,'new_replay_attempts':execution,
        'checksums':{'expected':expected,'actual':actual},'matches':matches,'release_manifest_equal':True,
        'release_manifest_sha256':digest(clone/'reports/release_manifest.json'),
        'full_hospital_outputs_equal':full_output_matches,'full_hospital_output_hashes':full_output_hashes,
        'tests':tests,'commands':commands,'elapsed_seconds':round(time.perf_counter()-start,6),
        'scope':'Isolated local-clone reproduction with cached predictions removed.'}
    write_json(ROOT/'reports/reproduction_check.json',report)
    (ROOT/'reports/reproduction_commands.txt').write_text('\n\n'.join('COMMAND '+repr(c['argv'])+'\nEXIT '+str(c['returncode'])+'\n'+c['stdout']+c['stderr'] for c in commands))
print(json.dumps({'status':'passed','tested_commit':head,'checksums_equal':matches,'tests_passed':tests['tests_run']},indent=2))
