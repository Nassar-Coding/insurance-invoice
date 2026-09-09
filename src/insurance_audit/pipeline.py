"""One-command replay from frozen artifacts; no acquisition, fitting, or network."""
import contextlib
import io
import json
from pathlib import Path
import platform
import time
from .batch import run_audit
from .evaluation import evaluate_run
from .io import write_json
from .reporting import render_reports
from .submission import TARGETS, export_submission


def reproduce(root):
    root=Path(root).resolve();start=time.perf_counter()
    expected=(root/'.python-version').read_text().strip()
    if platform.python_version()!=expected:
        raise RuntimeError(f'Verified runtime is Python {expected}; current version is {platform.python_version()}')
    h1,h1_status=run_audit(root,['H1'])
    target,target_status=run_audit(root,TARGETS)
    manifest=export_submission(root)
    with contextlib.redirect_stdout(io.StringIO()):
        evaluations={group:evaluate_run(root,group) for group in ('development','check','full')}
    workload=render_reports(root,evaluations)
    execution={'status':'success','python':platform.python_version(),'elapsed_seconds':round(time.perf_counter()-start,6),
        'h1_attempt':h1_status['attempt'],'target_attempt':target_status['attempt'],
        'hospital_opinions':{h:w['opinions'] for h,w in workload.items()},
        'submission_rows':manifest['rows'],'submission_sha256':manifest['submission_sha256'],
        'network_calls':0,'model_calls':0,'scope':'prediction replay plus H1 evaluation; not fresh LLM extraction'}
    write_json(root/'reports/execution.json',execution)
    return execution
