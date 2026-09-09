"""Create and actually restore a self-contained implementation checkpoint."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
destination=Path(sys.argv[1]);destination.parent.mkdir(parents=True,exist_ok=True)
files=[p for p in ROOT.rglob('*') if p.is_file() and not any(s in {'__pycache__','.venv'} for s in p.parts) and p.suffix!='.pyc']
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
manifest_payload=json.dumps(manifest,sort_keys=True,indent=2)+'\n'
with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for p in sorted(files):archive.write(p,'insurance_audit_project/'+str(p.relative_to(ROOT)))
    archive.writestr('CHECKPOINT_MANIFEST.json',manifest_payload)
with tempfile.TemporaryDirectory() as d:
    with zipfile.ZipFile(destination) as archive:archive.extractall(d)
    restored=Path(d)/'insurance_audit_project'
    errors=[p for p,sha in manifest.items() if hashlib.sha256((restored/p).read_bytes()).hexdigest()!=sha]
    assert not errors,errors
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=restored,text=True).strip()
    # Nonrecursive evidence can travel inside the archive without pretending
    # that an archive contains its own final checksum. The project files listed
    # by the manifest were all actually restored and checked before this append.
    verification={'status':'passed','files_verified':len(files),'mismatches':errors,
        'restored_git_head':head,'manifest_sha256':hashlib.sha256(manifest_payload.encode()).hexdigest(),
        'report_sha256':manifest['reports/implementation_report.md'],
        'submission_sha256':manifest['submission.csv'],
        'verification_scope':'All manifest-listed project files actually extracted and hash-checked; Git HEAD resolved. Author recovery check, not independent closure re-audit.',
        'historical_recovery_note':'The project recovery_latest.json describes the preceding checkpoint. This top-level verification describes the manifest in this archive.'}
    with zipfile.ZipFile(destination,'a',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        archive.writestr('CHECKPOINT_VERIFICATION.json',json.dumps(verification,sort_keys=True,indent=2)+'\n')
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None,'Archive integrity failure after adding verification'
        assert json.loads(archive.read('CHECKPOINT_VERIFICATION.json'))==verification
        assert hashlib.sha256(archive.read('CHECKPOINT_MANIFEST.json')).hexdigest()==verification['manifest_sha256']
        for relative in ['reports/implementation_report.md','submission.csv']:
            assert hashlib.sha256(archive.read('insurance_audit_project/'+relative)).hexdigest()==manifest[relative]
    report={'files_verified':len(files),'mismatches':errors,'restored_git_head':head,
            'archive_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'archive_bytes':destination.stat().st_size,
            'embedded_verification':'CHECKPOINT_VERIFICATION.json',
            'embedded_manifest_sha256':verification['manifest_sha256']}
    (ROOT/'reports/recovery_latest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
