"""Source-record check of actual bundle substitutions, before or after AUD-02."""
import json
from pathlib import Path


def verify_emitted_stages(root,result,data,contract,mappings):
    """Reconcile emitted bundle/base stages to accepted clauses and raw context.

    This checks source selection and applicability, not target-label accuracy.
    The patient context is recomputed by the corrected shared implementation.
    """
    from insurance_audit.context import Context
    context=Context(data,contract,mappings)
    services={s['id']:s for s in contract['services']}
    lines={(l.source,l.source_row):l for l in data.lines}
    checked=0;applied=0
    for trace in result['traces']:
        if trace['status']!='supported':continue
        headers=context.headers[trace['invoice_id']];assert len(headers)==1
        header=headers[0]
        for item in trace['lines']:
            raw=lines[(item['source'],item['source_row'])];price=item['pricing']
            for stage in price['stages']:
                if stage['operation']!='bundle':continue
                checked+=1
                assert stage['base_rate']==price['version']
                assert stage['before']==[price['version']['cents']]
                expected=[(i,b) for i,b in enumerate(contract['bundles']) if item['service_id'] in {b['a'],b['b']}]
                assert len(stage['rules'])==len(expected)
                sources=set();outcomes=None
                for entry,(index,bundle) in zip(stage['rules'],expected):
                    side='a' if item['service_id']==bundle['a'] else 'b'
                    partner=bundle['b' if side=='a' else 'a'];cents=bundle[side+'_cents']
                    assert entry['rule_index']==index and entry['source']==bundle['source']
                    assert entry['service_id']==item['service_id'] and entry['partner_service_id']==partner
                    assert entry['substituted_cents']==cents
                    state,evidence=context.presence(partner,header.patient_id,raw.service_date)
                    assert entry['presence'] is state
                    assert type(entry['context_index']) is int and entry['context_index']>=0
                    assert price['context'][entry['context_index']]==evidence
                    options={cents} if state is True else {price['version']['cents']} if state is False else {price['version']['cents'],cents}
                    assert outcomes is None or options==outcomes
                    outcomes=options
                    if state is not False:sources.add(bundle['source'])
                    if state is not True:sources.add(price['version']['source'])
                    if state is True:applied+=1
                    path,number=bundle['source'].split('#L');source=(root/path).read_text().splitlines()[int(number)-1]
                    assert services[bundle['a']]['name'] in source and services[bundle['b']]['name'] in source
                    for value in [bundle['a_cents'],bundle['b_cents']]:
                        assert f'{value//100:,}.{value%100:02}' in source or f'{value//100}.{value%100:02}' in source
                if not expected:sources.add(price['version']['source'])
                assert stage['source']==sorted(sources)
                assert stage['after']==sorted(outcomes if outcomes is not None else {price['version']['cents']})
    return {'base_or_bundle_stages_checked':checked,'applied_bundle_clauses_checked':applied}


def inspect(root,pointers):
    rows=[];counts={}
    for hospital in ['H1','H2','H3','H4','H5']:
        group='H1' if hospital=='H1' else 'H2-H3-H4-H5'
        directory=root/'runs'/pointers[group]['path']
        result=json.loads((directory/f'{hospital}.json').read_text())
        contract=json.loads((root/f'contracts/hospital_{hospital[1:]}.json').read_text())
        count=0;invoices=set()
        for trace in result['traces']:
            if trace['status']!='supported':continue
            for line in trace['lines']:
                price=line['pricing'];stage=next((s for s in price['stages'] if s['operation']=='bundle'),None)
                if stage is None:continue
                for index,rule in enumerate(contract['bundles']):
                    if line['service_id'] not in {rule['a'],rule['b']}:continue
                    side='a' if line['service_id']==rule['a'] else 'b';partner=rule['b' if side=='a' else 'a']
                    contexts=[d for d in price['context'] if d['query'].get('service_id')==partner and d['kind'] in {'patient_service_day','unobserved_service_day_envelope'}]
                    if stage['after']!=[rule[side+'_cents']] or not any(d['certain_records']>0 for d in contexts):continue
                    path,number=rule['source'].split('#L');source_line=(root/path).read_text().splitlines()[int(number)-1]
                    names={s['id']:s['name'] for s in contract['services']}
                    assert names[rule['a']] in source_line and names[rule['b']] in source_line
                    for cents in [rule['a_cents'],rule['b_cents']]:
                        assert f'{cents//100:,}.{cents%100:02}' in source_line or f'{cents//100}.{cents%100:02}' in source_line
                    row={'hospital':hospital,'invoice_id':trace['invoice_id'],'line_id':line['line_id'],
                         'service_id':line['service_id'],'bundle_index':index,'partner_service_id':partner,
                         'substituted_cents':rule[side+'_cents'],'source':stage['source'],
                         'required_source':rule['source'],'source_line':source_line,'stage':stage,'context':contexts}
                    rows.append(row);count+=1;invoices.add(trace['invoice_id'])
        counts[hospital]={'lines':count,'invoices':len(invoices)}
    return {'counts':counts,'rows':rows,'lines':len(rows),'invoices':len({r['invoice_id'] for r in rows}),
            'target_lines':sum(r['hospital']!='H1' for r in rows),'target_invoices':len({r['invoice_id'] for r in rows if r['hospital']!='H1'})}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('output');args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    pointers={g:json.loads((root/f'runs/current-{g}.json').read_text()) for g in ['H1','H2-H3-H4-H5']}
    result=inspect(root,pointers);(root/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
