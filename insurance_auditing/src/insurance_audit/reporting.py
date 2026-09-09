"""Evidence-derived working reports; no fitting or alteration of decisions."""
from collections import Counter
import json
from pathlib import Path
from .batch import current_run
from .io import write_json
from .schema import digest
from .submission import TARGETS, verify_submission


def pct(value):return 'undefined' if value is None else f'{value*100:.2f}%'
def score(value):return 'undefined' if value is None else f'{value:.4f}'


def render_reports(root,evaluations):
    root=Path(root);h1,_=current_run(root,['H1']);targets,_=current_run(root,TARGETS)
    metrics={group:{k:v for k,v in report.items() if k not in {'details','provenance'}} for group,report in evaluations.items()}
    write_json(root/'reports/metrics.json',metrics)
    workload={}
    for hospital,directory in [('H1',h1)]+[(h,targets) for h in TARGETS]:
        result=json.loads((directory/f'{hospital}.json').read_text())
        reason_counts=Counter(reason for row in result['abstentions'] for reason in {v['reason'] for v in row['reasons']})
        maps=json.loads((root/f'mappings/hospital_{hospital[1:]}.json').read_text())['records']
        workload[hospital]={**result['accounting'],
            'flagged_opinions':sum(r['flagged'] for r in result['opinions']),
            'correct_opinions':sum(r['flagged']==0 for r in result['opinions']),
            'coverage':len(result['opinions'])/result['accounting']['unique_invoice_ids'],
            'abstention_invoice_counts_by_reason':dict(sorted(reason_counts.items())),
            'confidence_tiers':dict(sorted(Counter(r['confidence_tier'] for r in result['opinions']).items())),
            'qualified_opinions':sum(bool(r['interpretation_qualifications']) for r in result['opinions']),
            'distinct_mapping_keys':len(maps),'unresolved_mapping_keys':sum(r['state']=='unresolved' for r in maps),
            'review_scope':'all source services and all observed distinct keys examined; unresolved keys retained',
            'reason_count_note':'An invoice may have several reasons; cause counts do not sum to omissions.'}
    write_json(root/'reports/workload.json',workload)
    lines=['# Hospital 1 evaluation and implementation limitations','',
        'These are executed results from the current deterministic pipeline. Hospital 1 is development data. '
        'The patient-group check was first opened after the mapping and confidence freeze; the current check '
        'is a regression after that exposure, not a new holdout. Full H1 includes development. '
        'No target labels or target accuracy estimates exist.','',
        '| Partition | All IDs | Opinions | Coverage | Flag + exact cents on opinions | Error precision | Error recall, all IDs | F1 |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for group,m in metrics.items():
        b=m['flag_metrics_all']
        lines.append(f"| {group} | {m['population']} | {m['covered']} | {pct(m['coverage'])} | {m['whole_row_success_count']}/{m['covered']} | {pct(b['precision'])} | {pct(b['recall'])} | {score(b['f1'])} |")
    lines+=['','Abstentions are excluded from conditional accuracy and counted as missed positives in population recall. '
        'They are never correct negatives. The joint event is a correct binary flag and exact corrected cents; '
        'billed cents, identity, and complete line provenance are separately validated. Free-text category '
        'correctness is measured by a disclosed many-to-one family crosswalk, not folded into that joint event. '
        'Undefined denominators remain undefined. High conditional accuracy with low recall is a substantial limitation.','',
        '## Per-category development performance','',
        'Family precision/recall use the explicit crosswalk in `src/insurance_audit/evaluation.py`. '
        'Broad pricing diagnostics do not establish which particular premium or discount caused a rate mismatch.','',
        '| Family | Positive labels | TP | FP | Misses incl. abstentions | Precision | Recall | F1 |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for family,b in metrics['development']['per_category_family'].items():
        lines.append(f"| {family} | {b['support']} | {b['tp']} | {b['fp']} | {b['fn_including_abstentions']} | {pct(b['precision'])} | {pct(b['recall'])} | {score(b['f1'])} |")
    lines+=['','Original-label detection is also reported below. This table measures detection on invoices carrying '
        'each label, not category-specific precision. An invoice can carry multiple labels.','',
        '| Original label | Support | Covered | Flagged | Exact amount | Joint successes | Detection recall |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for label,b in metrics['development']['per_original_label_detection'].items():
        lines.append(f"| {label} | {b['support']} | {b['covered']} | {b['flagged']} | {b['amount_exact']} | {b['whole_row_success']} | {pct(b['detection_recall_all'])} |")
    lines+=['','## Confidence support','',
        'Confidence scores were frozen from development evidence before check exposure. Correct-row groups '
        'use conservative bounded scores; sparse error groups use .65 policy judgment. Targets use .80 '
        '(explicit) or .70 (generic noun elision); outcome-invariant uncertainty and outcome-relevant invoice '
        'facility projection are capped at .65. These are conservative judgments, not demonstrated target '
        'probability calibration. Missing necessary facts cause whole-invoice omission.','',
        '| Development tier | n | Joint successes | Mean confidence | Brier score |',
        '|---|---:|---:|---:|---:|']
    for tier,b in metrics['development']['confidence_groups'].items():
        lines.append(f"| {tier} | {b['n']} | {b['successes']} | {score(b['mean_confidence'])} | {score(b['brier_score'])} |")
    result=json.loads((h1/'H1.json').read_text());development=evaluations['development']
    details={d['invoice_id']:d for d in development['details']}
    def example(reasons):
        candidates=[a for a in result['abstentions'] if a['invoice_id'] in details and any(r['reason'] in reasons for r in a['reasons'])]
        candidates.sort(key=lambda a:(not details[a['invoice_id']]['truth']['flagged'],a['invoice_id']))
        if not candidates:return 'No matching development example was observed; no example is fabricated.'
        a=candidates[0];why=next(r['reason'] for r in a['reasons'] if r['reason'] in reasons)
        return f"Example `{a['invoice_id']}` was withheld for `{why}`; its development truth is flagged={details[a['invoice_id']]['truth']['flagged']}. See that invoice's current trace."
    lines+=['','## Four systematic failure mechanisms','',
        '1. **Overconfident service identity (observed and corrected).** Initial mapping assigned generic '
        '`Fract Outpatient Radiotherapy` to a metabolic service without evidence of the specialty. '
        'Development invoice INV-H1-000236 had a corrected amount overstated by 43,650 cents. '
        'All 39 analogous missing-essential-qualifier keys were withdrawn, with initial results preserved. '
        'This fixed an observed emitted error at a substantial coverage cost; it is not an invoice-specific answer patch.','',
        '2. **Insufficient description evidence (current abstention mechanism).** Unknown, ambiguous, or '
        'essentially incomplete descriptions prevent a complete invoice opinion and can also make related usage uncertain. '+example({'unresolved_service_mapping'}),'',
        '3. **Damaged source identity or dates (current abstention mechanism).** Conflicting reused invoice '
        'IDs and malformed dates cannot be corrected into a unique supported invoice total. '+example({'conflicting_reused_invoice_id','quarantined_required_source_record'}),'',
        '4. **Unobservable rule context (current abstention mechanism and target applicability risk).** '
        'Unresolved related rows, exclusion boundary/direction, or duplicate allocation can change the result. '+
        example({'multiple_supported_rate_outcomes','unresolved_exclusion','duplicate_service_day_allocation'})+
        ' H2 supplies admission/discharge dates, but actual submission dates, detailed episode/leave evidence '
        'and possible written exceptions remain unobserved under Articles II and XIII, so all its full opinions '
        'are withheld. H4 patient scope is bounded; H5 invoice facility projection is explicitly qualified.','',
        'Only the first mechanism is an observed emitted wrong amount during development. The others explain '
        'observed omissions or unlabelled target risks, not invented scored failures. After the correction the '
        'current emitted H1 joint event has no observed errors; that does not establish accuracy outside the covered subset.','',
        '## Target coverage and unresolved workload','',
        '| Hospital | Unique IDs | Opinions | Flagged | Withheld | Coverage | Unresolved mapping keys |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for h in TARGETS:
        w=workload[h];lines.append(f"| {h} | {w['unique_invoice_ids']} | {w['opinions']} | {w['flagged_opinions']} | {w['abstentions']} | {pct(w['coverage'])} | {w['unresolved_mapping_keys']} |")
    lines+=['','Every raw CSV occurrence is accounted for. All five source contracts and all observed mapping keys '
        'were examined; complete invoice coverage remains limited by evidence. `workload.json` records overlapping '
        'omission causes and review items. The system audits the supplied historical snapshot, not an unseen complete '
        'claims feed. Late or corrected records require a new run and context recomputation.','',
        'Replay uses retained reviewed schemas/mappings and standard-library Python. Repeating fresh LLM extraction '
        'is a different activity and is not claimed bit-reproducible. The first independent implementation audit '
        'returned PASS WITH CORRECTIONS. This revision corrects quarantined-header ownership propagation '
        '(AUD-01) and controlling bundle citations (AUD-02); before/after and author regression evidence are '
        'retained under reports/corrections/audit_1. Independent closure re-audit and external publishing '
        'have not been performed.']
    (root/'reports/evaluation_report.md').write_text('\n'.join(lines)+'\n')
    manifest=verify_submission(root)
    source_files=list((root/'src').rglob('*.py'))+list((root/'tests').rglob('*.py'))+list((root/'tests/fixtures').glob('*.json'))
    source_files+=list((root/'prompts').glob('*.md'))+[root/'evaluation/split_manifest.json',root/'evaluation/confidence_policy.json',root/'data/source/labels/hospital_1_labels.csv',root/'.python-version',root/'requirements.txt']
    evidence_files=[root/'submission.csv',root/'reports/metrics.json',root/'reports/workload.json',root/'reports/evaluation_report.md']
    release={'target_release_id':manifest['release_id'],
        'run_ids':{'H1':current_run(root,['H1'])[1]['run_id'],'targets':current_run(root,TARGETS)[1]['run_id']},
        'prediction_inputs':{'H1':current_run(root,['H1'])[1]['identity'],'targets':current_run(root,TARGETS)[1]['identity']},
        'evaluation_testing_and_documentation_inputs':{str(p.relative_to(root)):digest(p) for p in sorted(set(source_files))},
        'stable_outputs':{str(p.relative_to(root)):digest(p) for p in evidence_files},
        'scope':'local corrected implementation candidate after first independent audit; author regression only, independent closure re-audit and publication pending'}
    write_json(root/'reports/release_manifest.json',release)
    return workload
