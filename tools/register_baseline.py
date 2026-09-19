"""Register executed Gate 1 reports and the explicitly carried-forward generalization result."""
import json
from pathlib import Path
from cost_scorer import ROOT, save, sha


def register(project):
    out=project/'reports/gate1'
    h1={}
    for partition in ('development','check','full'):
        row=json.loads((out/f'cost_{partition}.json').read_text())
        h1[partition]={k:row[k] for k in ['population','erroneous','clean','emitted','withheld','tp','fn','fp','cost','recall','tp_amount','reliability','per_primary_family','per_category_detection']}
    expected={'development':(4,38,0,190),'full':(5,53,0,265),'check':(1,15,0,75)}
    for group,target in expected.items():
        if tuple(h1[group][k] for k in ['tp','fn','fp','cost'])!=target:
            raise ValueError('Measured baseline disagrees with the required '+group+' results')
    trace=json.loads((out/'trace_summary.json').read_text())
    hospitals=json.loads((out/'hospital_distributions.json').read_text())
    current_hash=sha(project/'submission.csv')
    if current_hash!=trace['submission_sha256'] or current_hash!='2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c':
        raise ValueError('Submission changed')
    baseline={'schema_version':1,'gate':'gate1','h1':h1,'hospitals':hospitals,
        'leaderboard_cost':1395,'leaderboard_scope':'Previously reported external H2-H5 score; target labels are unavailable locally.',
        'submission_sha256':current_hash,'submission_rows':340,
        'generalization_baseline':{
            'status':'carried_forward_prior_observation_not_rerun',
            'source':'Prior Gate 1 full-history description control, explicitly reaffirmed in the user instruction to rebuild Gate 1 lean.',
            'original_logs_status':'Original unpublished experiment logs were lost in workspace maintenance; values are preserved from the recorded conversation, not fabricated as new execution evidence.',
            'partition':'development','population':622,'erroneous':42,
            'unperturbed':{'tp':4,'fn':38,'fp':0,'recall':4/42},
            'perturbed':{'tp':1,'fn':41,'fp':0,'recall':1/42},
            'new_false_positives':0,'relative_recall_degradation':.75,
            'protocol':{'kind':'full_history_description_only_control','seed':20260919,
                'history':'Keep original H1 IDs, physical row order and all patients/history.',
                'descriptions':'Select round(0.30 * line_count) row indices with random.Random(seed).sample; first half preserve codes; apply existing tools/generalize.py perturb(description, keep_code, row_index).',
                'evaluation':'Development labels only; retain all unlabelled H1 context.',
                'distinction':'Not the 70%-patient re-ID stress test, whose sampling can change hospital-wide utilisation and invalidate original labels.'},
            'gate3_tolerance_met':False,'gate1_scope':'Record baseline only; the <=10% relative loss criterion begins at Gate 3.'},
        'decoy_proxy_flags':None,'decoy_proxy_status':'Not defined until Gate 2.6; zero clean-development FP is not a decoy measurement.',
        'reference_base_rates':{'scored_h2_h5':285/3942,'h1':58/913},
        'low_rate_investigation':{h:{'status':'investigated','histogram':'reports/gate1/withheld_reasons.json',
            'resolution':'Causes accounted for; prediction behavior remains unchanged in this measurement gate.'} for h in ['H2','H3','H4','H5']},
        'access_boundary':'Full/check baseline explicitly authorized in Gate 1. Do not read or report check again until Final Gate.',
        'verification_boundaries':{'generalization_rerun':False,'clean_checkout_run':False,'a3':'waived by user; Gate 0 closed','tags':'user-managed'},
        'evidence':{str(p.relative_to(project)):sha(p) for p in [out/'cost_development.json',out/'cost_full.json',out/'cost_check.json',out/'trace_summary.json',out/'withheld_reasons.json',out/'missed_development_crosstab.json',out/'hospital_distributions.json']},
        'entries':[{'gate':'gate1','development_cost':h1['development']['cost'],'clean_development_fp':h1['development']['fp'],
            'target_rows':{h:hospitals[h]['rows'] for h in ['H2','H3','H4','H5']},
            'target_flags':{h:hospitals[h]['flags'] for h in ['H2','H3','H4','H5']},
            'generalization_result_source':'carried_forward_prior_observation_not_rerun'}]}
    path=project/'evaluation/baseline_cost.json'
    if path.exists():
        previous=json.loads(path.read_text())
        if any(e['gate']!='gate1' for e in previous.get('entries',[])):
            raise ValueError('Later gate entries exist; refusing to overwrite history')
    save(path,baseline)
    print(json.dumps({'status':'PASS','development_cost':h1['development']['cost'],'full_cost':h1['full']['cost'],
        'generalization':'Carried forward 4 -> 1 detections, zero new FP; NOT rerun.','submission_sha256':current_hash}))


if __name__=='__main__':register(ROOT)
