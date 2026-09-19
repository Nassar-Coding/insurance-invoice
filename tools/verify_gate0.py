"""Gate 0 clean-clone verification; never opens real H1 labels or check reports."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def verify(root,interpreters,out):
    out.mkdir(parents=True,exist_ok=True)
    report={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
            'status':'in_progress','scope':'Prediction-only replay and tests on two Python 3.12 patch versions; real labels and split removed before execution.','runs':[]}
    reference=(root/'submission.csv').read_bytes();versions=[]
    for index,executable in enumerate(interpreters):
        record={'interpreter':executable,'commands':[]};report['runs'].append(record)
        with tempfile.TemporaryDirectory(prefix='insurance-gate0-clone-') as temporary:
            temp=Path(temporary);clone=temp/'repo'
            env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':str(index+100),'PIP_DISABLE_PIP_VERSION_CHECK':'1'}
            def command(name,args,cwd):
                t=time.perf_counter();p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
                log=out/f'python{index+1}_{name}.log';log.write_text(p.stdout+p.stderr)
                record['commands'].append({'name':name,'returncode':p.returncode,'elapsed_seconds':round(time.perf_counter()-t,3),'log':log.name})
                (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
                if p.returncode:raise RuntimeError(f'{name} failed: {log}')
                return p.stdout.strip()
            command('clone',['git','clone','--quiet','--no-local',str(root),str(clone)],root)
            record['clone_commit']=command('commit',['git','rev-parse','HEAD'],clone)
            assert record['clone_commit']==report['source_commit']
            for path in ['reports','runs','evidence','governance','data/source/labels','tests/evaluation','.git']:
                if (clone/path).exists():shutil.rmtree(clone/path)
            (clone/'submission.csv').unlink()
            record['labels_manifest_archives_saved_outputs_removed']=True
            command('venv',[executable,'-m','venv',str(temp/'venv')],clone)
            python=str(temp/'venv/bin/python');env['PATH']=str(temp/'venv/bin')+os.pathsep+env['PATH'];env['PYTHONPATH']='src'
            version=command('version',[python,'-c','import platform; print(platform.python_version())'],clone);versions.append(version);record['python_version']=version
            assert version.startswith('3.12.')
            command('install',[python,'-m','pip','install','--no-index','-r','requirements.txt'],clone)
            command('pip_check',[python,'-m','pip','check'],clone)
            command('reproduce',[python,'-m','insurance_audit','reproduce'],clone)
            command('verify_submission',[python,'-m','insurance_audit','verify-submission'],clone)
            command('tests',[python,'tools/run_checks.py','gate0_clean'],clone)
            record['tests']=json.loads((clone/'reports/tests_gate0_clean.json').read_text())
            assert record['tests']['success'] and record['tests']['skipped']==0
            record['submission_sha256']=digest(clone/'submission.csv')
            record['matches_fallback_bytes']=(clone/'submission.csv').read_bytes()==reference
            assert record['matches_fallback_bytes']
            record['execution']=json.loads((clone/'reports/execution.json').read_text())
            assert record['execution']['evaluation']['status']=='not_requested'
            record['hospital_results']={};record['hospital_output_hashes']={}
            for group in ['H1','H2-H3-H4-H5']:
                pointer=json.loads((clone/f'runs/current-{group}.json').read_text());folder=clone/'runs'/pointer['path']
                for h in group.split('-'):
                    value=json.loads((folder/f'{h}.json').read_text());a=value['accounting'];flags=sum(r['flagged'] for r in value['opinions'])
                    record['hospital_results'][h]={'unique_invoices':a['unique_invoice_ids'],'rows':len(value['opinions']),'flags':flags,'flag_rate_all_invoices':flags/a['unique_invoice_ids'] if a['unique_invoice_ids'] else None,'withheld':len(value['abstentions'])}
                    for suffix in ['json','input_quality.json']:record['hospital_output_hashes'][f'{h}.{suffix}']=digest(folder/f'{h}.{suffix}')
            record['status']='passed'
    assert len(set(versions))==2,'Two different patch versions are required'
    assert report['runs'][0]['submission_sha256']==report['runs'][1]['submission_sha256']
    assert report['runs'][0]['hospital_output_hashes']==report['runs'][1]['hospital_output_hashes']
    report.update(status='passed',two_distinct_patch_versions=True,submissions_byte_identical=True,all_five_hospital_results_and_quality_byte_identical=True)
    (out/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--python',action='append',required=True);parser.add_argument('--output',type=Path,default=ROOT/'evaluation/gate0/clean_reproduction')
    args=parser.parse_args()
    if len(args.python)!=2:parser.error('Specify exactly two --python executables')
    result=verify(ROOT,[str(Path(p).resolve()) for p in args.python],args.output.resolve())
    print(json.dumps({'status':result['status'],'source_commit':result['source_commit'],'versions':[r['python_version'] for r in result['runs']],'submission_sha256':result['runs'][0]['submission_sha256']},indent=2))
