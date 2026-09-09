"""Materialize the model's recorded revised H1 mapping decision, preserving v1."""
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from insurance_audit.io import write_json
from insurance_audit.schema import digest,validate_mappings
from mapping_policy import evidence_grade

archive=ROOT/'mappings/archive';archive.mkdir(exist_ok=True)
for old,new in [('mappings/hospital_1.raw.json','H1.raw.v1.json'),('mappings/hospital_1.json','H1.accepted.v1.json'),
                ('reports/H1_source_review.json','H1.source_review.v1.json'),('contracts/H1.bundle.json','H1.bundle.v1.json')]:
    if not (archive/new).exists():shutil.copy2(ROOT/old,archive/new)
m=json.loads((archive/'H1.raw.v1.json').read_text());m['normalizer_version']='2';m['schema_version']='2';c=json.loads((ROOT/'contracts/hospital_1.raw.json').read_text())
ss={s['id']:s['name'] for s in c['services']};changes=[]
for r in m['records']:
    if r['state']!='accepted':continue
    grades=[evidence_grade(d,ss[r['service_id']]) for d in r['raw_descriptions']]
    if 'unresolved' in grades:
        changes.append({'key':r['key'],'previous_service_id':r['service_id'],'candidate_name':ss[r['service_id']],
                        'reason':'Essential name concepts are missing or conflated; catalog uniqueness does not establish identity.'})
        r.update(state='unresolved',service_id=None,grade='unresolved')
    else:r['grade']='elided' if 'elided' in grades else 'explicit'
    r['evidence'].append('Revision 2: independent essential concepts required; only supported generic trailing noun elision accepted. See prompts/map_v2.md and reports/H1_mapping_change_v2.json.')
validate_mappings(m,c);write_json(ROOT/'mappings/hospital_1.raw.json',m)
write_json(ROOT/'reports/H1_mapping_change_v2.json',{'decision':'D007','development_exposure':True,'check_exposure':False,
    'previous_expectation':'Unique in-catalog lexical candidates with elided qualifiers were accepted.',
    'observation':'INV-H1-000236 mapped Fract Outpatient Radiotherapy to Outpatient Metabolic Radiotherapy Fraction without evidence for Metabolic. H1 development label says unknown_service; corrected total differed by 43650 cents.',
    'source_evidence':'README: descriptions must be mapped; no assertion that every service is contracted. H1 rate table has a qualified name, not a generic outpatient radiotherapy rate.',
    'resolution':'Apply the stricter semantic policy to all H1 mappings and every subsequent hospital; no invoice-specific price correction or target labels.',
    'changes':changes,'new_raw_sha256':digest(ROOT/'mappings/hospital_1.raw.json')})
print(json.dumps({'changed':len(changes),'accepted':sum(r['state']=='accepted' for r in m['records']),
                  'unresolved':sum(r['state']=='unresolved' for r in m['records'])}))
