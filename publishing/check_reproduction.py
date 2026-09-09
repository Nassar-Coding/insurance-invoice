"""Publication-only clean-clone verification; never modifies prediction logic.

The comparison reference stays in this parent process. The child clone loses
saved predictions, result history and report caches before the documented run.
"""
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def canonical_evaluation(path):
    value = json.loads(path.read_text())
    value['provenance'].pop('attempt')
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    started = time.perf_counter()
    if platform.python_version() != '3.12.13':
        raise RuntimeError('Use the audited CPython 3.12.13 runtime.')
    baseline = json.loads((ROOT/'evidence/publishing/baseline.json').read_text())
    reference_csv = (ROOT/'evidence/audited_baseline/submission.csv').read_bytes()
    if hashlib.sha256(reference_csv).hexdigest() != baseline['submission_sha256']:
        raise RuntimeError('The audited submission reference changed.')
    out = ROOT/'evidence/publishing/latest_reproduction'
    out.mkdir(parents=True, exist_ok=True)
    report = {'status': 'in progress', 'utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'commands': [],
              'scope': 'Publishing preparation verification; no new independent technical audit.'}

    def save():
        (out/'result.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')

    def run(label, command, cwd, env):
        t = time.perf_counter()
        p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
        (out/f'{label}.log').write_text(p.stdout+p.stderr)
        report['commands'].append({'name': label, 'argv': [str(v) for v in command],
                                   'returncode': p.returncode,
                                   'elapsed_seconds': round(time.perf_counter()-t, 6),
                                   'log': f'{label}.log'})
        save()
        if p.returncode:
            raise RuntimeError(f'{label} failed with exit {p.returncode}; see {out/label}.log')
        return p.stdout

    env = {'PATH': str(Path(sys.executable).parent)+os.pathsep+'/usr/bin:/bin',
           'PYTHONNOUSERSITE': '1', 'PYTHONDONTWRITEBYTECODE': '1',
           'PYTHONHASHSEED': '54321', 'LANG': 'C.UTF-8', 'PIP_DISABLE_PIP_VERSION_CHECK': '1',
           'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull}
    try:
        head = run('source_commit', ['git', 'rev-parse', 'HEAD'], ROOT, env).strip()
        report['tested_commit'] = head
        report['frozen_file_matches'] = {p: digest(ROOT/p) == sha for p, sha in baseline['frozen_files'].items()}
        assert all(report['frozen_file_matches'].values()), 'Protected original file changed'
        report['release_bound_file_matches'] = {p: digest(ROOT/p) == sha for p, sha in baseline['release_bound_files'].items()}
        assert all(report['release_bound_file_matches'].values()), 'Release-bound original file changed'
        with tempfile.TemporaryDirectory(prefix='insurance-publication-') as temp:
            temp = Path(temp)
            clone = temp/'project'
            run('clone', ['git', 'clone', '--quiet', '--no-local', str(ROOT), str(clone)], ROOT, env)
            report['clone_commit'] = run('clone_commit', ['git', 'rev-parse', 'HEAD'], clone, env).strip()
            assert report['clone_commit'] == head
            assert all(digest(clone/p) == sha for p, sha in baseline['frozen_files'].items())
            # Reviewed source evidence is a genuine accepted-package input.
            required_reports = {f'H{h}_{kind}.json' for h in range(1, 6)
                                for kind in ('source_review', 'candidate_closure')}
            removed = []
            for child in list((clone/'reports').iterdir()):
                if child.name not in required_reports:
                    removed.append(str(child.relative_to(clone)))
                    if child.is_dir():
                        shutil.rmtree(child)
                    else:
                        child.unlink()
            for name in ['runs', 'evidence', 'governance/audits', '.git']:
                path = clone/name
                if path.exists():
                    shutil.rmtree(path)
                    removed.append(name+'/')
            (clone/'submission.csv').unlink()
            removed.append('submission.csv')
            report['removed_before_execution'] = sorted(removed)
            report['retained_report_inputs'] = sorted(required_reports)
            report['saved_predictions_available_to_pipeline'] = False
            report['inherited_credentials_or_work_environment'] = False
            report['sanitized_environment_names'] = sorted(env)
            # A fresh venv proves that globally installed packages are unnecessary.
            run('venv', [sys.executable, '-m', 'venv', str(temp/'venv')], clone, env)
            python = temp/'venv'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
            env['PATH'] = str(python.parent)+os.pathsep+'/usr/bin:/bin'
            env['PYTHONPATH'] = 'src'
            run('version', [str(python), '--version'], clone, env)
            run('dependency_install', [str(python), '-m', 'pip', 'install', '--no-index', '-r', 'requirements.txt'], clone, env)
            run('dependency_check', [str(python), '-m', 'pip', 'check'], clone, env)
            report['installed_packages'] = json.loads(run('dependency_list', [str(python), '-m', 'pip', 'list', '--format=json'], clone, env))
            assert {p['name'].lower() for p in report['installed_packages']} <= {'pip', 'setuptools'}, 'Unexpected third-party packages in clean runtime'
            run('reproduce', [str(python), '-m', 'insurance_audit', 'reproduce'], clone, env)
            run('verify_submission', [str(python), '-m', 'insurance_audit', 'verify-submission'], clone, env)
            run('tests', [str(python), 'tools/run_checks.py', 'local'], clone, env)
            tests = json.loads((clone/'reports/tests_local.json').read_text())
            assert tests['success'] and tests['tests_run'] == 75 and tests['skipped'] == 0
            report['tests'] = tests
            for part in ['development', 'check', 'full']:
                run(f'evaluate_{part}', [str(python), '-m', 'insurance_audit', 'evaluate', '--partition', part], clone, env)
            report['stable_output_hashes'] = {p: digest(clone/p) for p in baseline['stable_outputs']}
            report['stable_output_matches'] = {p: sha == baseline['stable_outputs'][p] for p, sha in report['stable_output_hashes'].items()}
            assert all(report['stable_output_matches'].values())
            report['release_manifest_sha256'] = digest(clone/'reports/release_manifest.json')
            assert report['release_manifest_sha256'] == baseline['release_manifest_sha256']
            report['detailed_evaluation_matches_except_attempt'] = {
                part: canonical_evaluation(clone/f'reports/evaluation_{part}.json') == sha
                for part, sha in baseline['detailed_evaluation_canonical_sha256'].items()}
            assert all(report['detailed_evaluation_matches_except_attempt'].values())
            report['hospital_output_matches'] = {}
            report['hospital_output_hashes'] = {}
            report['hospital_results'] = {}
            report['new_attempt_status'] = {}
            for group, expected in baseline['audited_runs'].items():
                pointer = json.loads((clone/f'runs/current-{group}.json').read_text())
                directory = clone/'runs'/pointer['path']
                status = json.loads((directory/'status.json').read_text())
                report['new_attempt_status'][group] = status
                assert status['run_id'] == expected['run_id'] and status['identity'] == expected['identity']
                actual = {p: digest(directory/p) for p in expected['outputs']}
                report['hospital_output_hashes'][group] = actual
                report['hospital_output_matches'][group] = actual == expected['outputs'] == status['outputs']
                for h in group.split('-'):
                    value = json.loads((directory/f'{h}.json').read_text())
                    report['hospital_results'][h] = {**value['accounting'],
                        'flagged': sum(p['flagged'] for p in value['opinions']),
                        'confidence_counts': dict(sorted(Counter(str(p['confidence']) for p in value['opinions']).items()))}
            assert all(report['hospital_output_matches'].values()), 'Hospital result/trace/input-quality difference'
            actual_csv = (clone/'submission.csv').read_bytes()
            assert actual_csv == reference_csv, 'Audited submission byte identity changed'
            rows = list(csv.DictReader(actual_csv.decode().splitlines()))
            columns = list(rows[0])
            template = next((clone/'data/source').rglob('submission_template.csv'))
            with template.open(newline='') as stream:
                expected_columns = next(csv.reader(stream))
            assert columns == expected_columns
            assert len(rows) == 340 and len({r['invoice_id'] for r in rows}) == 340
            assert sum(int(r['flagged']) for r in rows) == 6
            assert all(r['flagged'] in {'0', '1'} and 0 <= float(r['confidence']) <= 1
                       and str(int(r['expected_total_cents'])) == r['expected_total_cents']
                       and str(int(r['billed_total_cents'])) == r['billed_total_cents'] for r in rows)
            by_id = {}
            for h in range(2, 6):
                with (clone/f'data/source/invoices/hospital_{h}_invoices.csv').open(newline='') as stream:
                    by_id.update({r['invoice_id']:f'H{h}' for r in csv.DictReader(stream)})
            assert all(r['invoice_id'] in by_id for r in rows)
            hospital_counts = dict(sorted(Counter(by_id[r['invoice_id']] for r in rows).items()))
            assert hospital_counts == {'H3':148, 'H4':64, 'H5':128}
            report['submission'] = {'rows': len(rows), 'unique_ids': 340, 'columns': columns,
                'flagged': 6, 'predicted_correct': 334, 'hospital_counts': hospital_counts,
                'bytes_and_order_equal_attached_reference': True, 'sha256': digest(clone/'submission.csv')}
            report['execution'] = json.loads((clone/'reports/execution.json').read_text())
            report['metrics'] = json.loads((clone/'reports/metrics.json').read_text())
            report['generated_run_disk_bytes'] = sum(p.stat().st_size for p in (clone/'runs').rglob('*') if p.is_file())
            # Only small evidence leaves the disposable clone; full results are
            # content-identical to the already retained audited history.
            retained = ['submission.csv', 'reports/metrics.json', 'reports/workload.json',
                        'reports/evaluation_report.md', 'reports/release_manifest.json',
                        'reports/execution.json', 'reports/tests_local.json', 'reports/tests_local.txt']
            for name in retained:
                destination = out/'generated'/name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(clone/name, destination)
        report['status'] = 'passed'
        report['elapsed_seconds'] = round(time.perf_counter()-started, 6)
        if sys.platform.startswith('linux'):
            import resource
            report['peak_child_process_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            report['memory_measurement_scope'] = 'Maximum child-process RSS across clone, install, replay, tests and partition evaluations; Linux KiB.'
        save()
        print(json.dumps({'status':report['status'], 'tested_commit':head, 'tests_passed':75,
                          'submission_sha256':report['submission']['sha256'],
                          'all_hospital_outputs_equal':True, 'report':str(out/'result.json')}, indent=2))
    except Exception as exc:
        report['status'] = 'failed'
        report['error'] = f'{type(exc).__name__}: {exc}'
        report['elapsed_seconds'] = round(time.perf_counter()-started, 6)
        save()
        raise


if __name__ == '__main__':
    main()
