"""Frozen whole-row confidence policy; no labels accessed during replay."""
import math


def choose(row,policy):
    if row.get('unresolved') or row.get('expected_total_cents') is None:return None,'unresolved'
    grade=row['mapping_evidence'];flag=row['flagged']
    if grade not in {'explicit','elided'}:raise ValueError('Unknown confidence evidence tier')
    if row['hospital']=='H1':
        group=policy['h1_groups'][f'{grade}:{flag}']
        value=group['confidence'];tier='h1_supported' if group['n']>=policy['minimum_empirical_n'] else 'sparse'
        tier+=':'+grade+':'+str(flag)
    else:value=policy['target_judgment'][grade];tier='novel_reviewed:'+grade
    if row.get('outcome_invariant_uncertainty'):
        value=min(value,policy['outcome_invariant_cap']);tier+=':invariant'
    if row.get('interpretation_qualifications'):
        value=min(value,policy['interpretation_cap']);tier+=':qualified'
    if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value) or not 0<=value<=1:
        raise ValueError('Confidence must be finite and in [0,1]')
    return value,tier


def assign_confidence(result,policy):
    if policy.get('version')!='1':raise ValueError('Unsupported confidence policy')
    for row in result['opinions']:
        value,tier=choose(row,policy)
        if value is None:raise ValueError('Unresolved row leaked into complete opinions')
        row.update(confidence=value,confidence_tier=tier,
                   confidence_state='development_supported_or_policy_judgment; not target-calibrated')
    by_id={r['invoice_id']:r for r in result['opinions']}
    for trace in result['traces']:
        if trace['status']=='supported':trace['opinion']=by_id[trace['invoice_id']]
