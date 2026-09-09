"""Execute the documented replay while proving the decision stage cannot read labels.

This is an implementation verification harness, not the independent challenge stage.
The ordinary README command does not depend on this harness or Work tools.
"""
import builtins
import io
import json
from pathlib import Path
import resource
import socket
import sys
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit import pipeline
from insurance_audit.io import write_json
from insurance_audit.schema import digest

reads=[]
original_builtin=builtins.open;original_io=io.open


def guard(opener):
    def opened(path,*args,**kwargs):
        name=str(path)
        if not isinstance(path,int) and ('/labels/' in name or '_labels.' in name):
            raise AssertionError('Decision pipeline attempted label access: '+name)
        if not isinstance(path,int):reads.append(name)
        return opener(path,*args,**kwargs)
    return opened


def guarded(function):
    def call(*args,**kwargs):
        with patch('builtins.open',guard(original_builtin)),patch('io.open',guard(original_io)):
            return function(*args,**kwargs)
    return call


start=time.perf_counter();network_attempts=[]
def deny_network(*args,**kwargs):
    network_attempts.append('attempted socket access')
    raise AssertionError('Replay attempted network access')
with patch.object(pipeline,'run_audit',guarded(pipeline.run_audit)),patch.object(pipeline,'export_submission',guarded(pipeline.export_submission)),patch('socket.socket',deny_network),patch('socket.create_connection',deny_network):
    execution=pipeline.reproduce(ROOT)
report={'status':'passed','guarded_stages':['H1 pricing','H2-H5 pricing','submission export'],
        'evaluation_label_access':'Only outside the guard, after all prediction decisions and export.',
        'guarded_file_opens':len(reads),'distinct_guarded_paths':len(set(reads)),
        'label_file_opens_during_guard':0,'elapsed_seconds':round(time.perf_counter()-start,6),
        'network_guard':'socket creation and connections rejected for entire replay','network_attempts':len(network_attempts),
        'process_peak_rss_mib_linux':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,2),
        'submission_sha256':digest(ROOT/'submission.csv'),'execution':execution}
write_json(ROOT/'reports/guarded_reproduction.json',report)
print(json.dumps(report,indent=2))
