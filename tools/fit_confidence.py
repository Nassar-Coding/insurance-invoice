"""Fit confidence to development accuracy per evidence tier. Read-only."""
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from insurance_audit.audit import audit
from insurance_audit.io import load_hospital
from insurance_audit.schema import load_bundle

# Ordered weakest to strongest; the fitted confidence must not fall as the tier
# strengthens, so a reader can trust the ordering even where a tier is sparse.
ORDER = ('ambiguous', 'partial_amount', 'no_match', 'match_fully_priced', 'structural', 'clean')


def wilson_lower(successes, total, z=1.96):
    """Conservative lower bound on the success rate; 0 when nothing was seen."""
    if not total:
        return 0.0
    phat = successes / total
    denominator = 1 + z * z / total
    centre = phat + z * z / (2 * total)
    spread = z * ((phat * (1 - phat) / total + z * z / (4 * total * total)) ** 0.5)
    return max(0.0, (centre - spread) / denominator)


def fit(project):
    project = Path(project).resolve()
    with (project / 'data/source/labels/hospital_1_labels.csv').open(newline='', encoding='utf-8-sig') as stream:
        labels = {r['invoice_id']: r for r in csv.DictReader(stream)}
    split = json.loads((project / 'tests/evaluation/split_manifest.json').read_text())['invoice_partitions']
    contract, mappings, _ = load_bundle(project, 'H1')
    result = audit(load_hospital(project / 'data/source', 'H1'), contract, mappings)
    seen = defaultdict(lambda: [0, 0])
    for row in result['opinions']:
        ident = row['invoice_id']
        if split.get(ident) != 'development':
            continue
        truth = labels[ident]
        correct = (int(truth['is_erroneous']) == row['flagged']
                   and row['expected_total_cents'] == int(truth['expected_total_cents']))
        bucket = seen[row['evidence_tier']]
        bucket[1] += 1
        bucket[0] += int(correct)
    tiers = {}
    floor = 0.0
    for name in ORDER:
        successes, total = seen.get(name, [0, 0])
        bound = wilson_lower(successes, total)
        # Round down to a hundredth so the published figure is never above the
        # evidence, and never let a stronger tier score below a weaker one.
        value = max(floor, int(bound * 100) / 100 if total else 0.50)
        tiers[name] = {'confidence': round(min(value, 0.99), 2), 'n': total, 'successes': successes,
                       'development_accuracy': round(successes / total, 6) if total else None,
                       'wilson_95_lower': round(bound, 6) if total else None,
                       'basis': ('fitted to development accuracy' if total >= 30
                                 else 'sparse: held at the level of the weaker tier, not fitted')}
        floor = tiers[name]['confidence']
    return tiers, seen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    tiers, _ = fit(args.project)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(tiers, indent=2, sort_keys=True) + '\n')
    for name in ORDER:
        row = tiers[name]
        print(f"{name:20} n={row['n']:>4} acc={row['development_accuracy']} -> {row['confidence']}")


if __name__ == '__main__':
    main()
