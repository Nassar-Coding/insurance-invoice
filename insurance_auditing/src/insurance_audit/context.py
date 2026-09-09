"""Retrospective context with explicit lower/upper bounds for unknown evidence."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
import hashlib
import json
from .io import INVOICE_COLUMNS, LINE_COLUMNS, integer, iso_date
from .resolve import mapping_index,resolve


@dataclass(frozen=True)
class Item:
    key: str
    line_id: str
    invoice_id: str
    service_id: str | None
    candidates: frozenset[str]
    patients: frozenset[str]
    day: str | None
    quantity: int | None
    ownership_unknown: bool


class Context:
    def __init__(self,data,contract,mappings):
        self.contract=contract
        self.services={s['id']:s for s in contract['services']}
        self.index=mapping_index(mappings)
        self.headers=defaultdict(list)
        for row in data.invoices:self.headers[row.invoice_id].append(row)
        # Typed headers determine whether their own invoice can be audited. Raw
        # header ownership is a separate evidence set: an invalid date/amount
        # cannot prove that another conflicting patient identifier is false.
        self.invoice_ids=data.invoice_identities()
        self.header_evidence=defaultdict(list);self.unlinked_headers=[]
        for row in data.invoices:
            self.header_evidence[row.invoice_id].append({'source':row.source,'row':row.source_row,
                'patient_id':row.patient_id,'status':'accepted'})
        for record in data.quarantined_headers():
            raw=record.get('raw_named',dict(zip(INVOICE_COLUMNS,record['raw'])))
            patient=raw.get('patient_id')
            evidence={'source':record['source'],'row':record['source_row'],
                'patient_id':patient if isinstance(patient,str) and patient.strip() else None,
                'status':'quarantined','reason':record.get('reason')}
            ident=record.get('invoice_id')
            if isinstance(ident,str) and ident.strip():self.header_evidence[ident].append(evidence)
            else:self.unlinked_headers.append(evidence)
        for entries in [*self.header_evidence.values(),self.unlinked_headers]:
            entries.sort(key=lambda h:(h['source'],h['row']))
        self.items=[];self.by_service=defaultdict(list)
        self.duplicate_line_ids=set(data.quality()['duplicate_line_ids'])
        self.quarantined_invoices={x['invoice_id'] for x in data.dispositions if x['status']=='quarantined'}
        for line in data.lines:
            self.add(line.line_id,line.invoice_id,line.description,line.service_date,line.quantity,f'{line.source}:{line.source_row}')
        # Retain recoverable pieces of quarantined rows for dependency uncertainty.
        for record in data.dispositions:
            if record['status']!='quarantined' or record['kind']!='line_items':continue
            raw=dict(zip(LINE_COLUMNS,record['raw']))
            # Headers can be reordered, so use retained named fields when present.
            raw=record.get('raw_named',raw)
            try:day=iso_date(raw.get('service_date',''),'service_date')
            except ValueError:day=None
            try:quantity=integer(raw.get('quantity',''),'quantity',10**9)
            except ValueError:quantity=None
            self.add(raw.get('line_id',f"unknown:{record['source_row']}"),raw.get('invoice_id',''),raw.get('description',''),day,quantity,
                     f"{record['source']}:{record['source_row']}")
        for entries in self.by_service.values():entries.sort(key=lambda x:(x.day or '',x.line_id,x.key))

    def add(self,line_id,invoice_id,description,day,quantity,key):
        sid,candidates,_=resolve(description,self.index,self.services)
        headers=self.header_evidence.get(invoice_id,[])
        patients=frozenset(h['patient_id'] for h in headers if h['patient_id'] is not None)
        unknown=not headers or any(h['patient_id'] is None for h in headers) or bool(self.unlinked_headers)
        item=Item(key,line_id,invoice_id,sid,frozenset(candidates),patients,day,quantity,unknown)
        self.items.append(item)
        for service in candidates:self.by_service[service].append(item)

    @staticmethod
    def possibly_owned(item,patient):
        return item.ownership_unknown or patient in item.patients

    @staticmethod
    def certainly_owned(item,patient):
        return not item.ownership_unknown and item.patients==frozenset([patient])

    def evidence(self,kind,query,known,possible,lower,upper):
        identities=sorted([('certain',x.line_id,x.key) for x in known]+[('possible',x.line_id,x.key) for x in possible])
        detail={'kind':kind,'query':query,'lower':lower,'upper':upper,
                'certain_records':len(known),'possible_records':len(possible),
                'member_digest':hashlib.sha256(json.dumps(identities,separators=(',',':')).encode()).hexdigest(),
                'possible_examples':[x.line_id for x in possible[:8]]}
        ownership=[]
        for item in sorted(known+possible,key=lambda x:(x.line_id,x.key)):
            headers=self.header_evidence.get(item.invoice_id,[])
            if item.ownership_unknown or any(h['status']=='quarantined' for h in headers):
                ownership.append({'line_id':item.line_id,'line_source':item.key,'invoice_id':item.invoice_id,
                    'candidate_patients':sorted(item.patients),'unbounded_patient_identity':item.ownership_unknown,
                    'headers':headers,'unlinked_headers':self.unlinked_headers})
        if ownership:detail['header_ownership_evidence']=ownership
        return detail

    def prior(self,service_id,day,line_id,patient=None):
        known=[];possible=[];low=0;high=0
        for item in self.by_service[service_id]:
            if item.line_id==line_id and item.line_id not in self.duplicate_line_ids:continue
            if item.day is not None:
                if not self.contract['term'][0]<=item.day<=self.contract['term'][1]:continue
                if (item.day,item.line_id)>=(day,line_id) and item.line_id not in self.duplicate_line_ids:continue
            certain=item.service_id==service_id and item.day is not None and item.line_id not in self.duplicate_line_ids
            if self.contract['semantics']['volume_basis']=='contract_term_patient_scope_unspecified':
                certain=certain and self.certainly_owned(item,patient)
            if item.quantity is None or item.quantity<=0:
                possible.append(item);return self.evidence('strict_prior',{'service_id':service_id,'day':day,'line_id':line_id},known,possible,None,None)
            if certain:
                known.append(item);low+=item.quantity;high+=item.quantity
            else:possible.append(item);high+=item.quantity
        return self.evidence('strict_prior',{'service_id':service_id,'day':day,'line_id':line_id},known,possible,low,high)

    def daily(self,service_id,patient,day):
        known=[];possible=[];low=0;high=0
        unobserved=self.contract['semantics']['service_day']=='seven_am_unobserved'
        for item in self.by_service[service_id]:
            if not self.possibly_owned(item,patient):continue
            if not unobserved and item.day is not None and item.day!=day:continue
            certain=not unobserved and item.service_id==service_id and self.certainly_owned(item,patient) and item.day==day
            if item.quantity is None or item.quantity<=0:
                possible.append(item);return self.evidence('patient_service_day',{'service_id':service_id,'patient':patient,'day':day},known,possible,None,None)
            if certain:known.append(item);low+=item.quantity;high+=item.quantity
            else:possible.append(item);high+=item.quantity
        return self.evidence('unobserved_service_day_envelope' if unobserved else 'patient_service_day',{'service_id':service_id,'patient':patient,'day':day},known,possible,low,high)

    def presence(self,service_id,patient,day):
        detail=self.daily(service_id,patient,day)
        state=True if detail['certain_records'] else None if detail['possible_records'] else False
        return state,detail

    def competitors(self,service_id,patient,day,line_id):
        known=[];possible=[]
        for item in self.by_service[service_id]:
            if item.line_id==line_id and line_id not in self.duplicate_line_ids:continue
            if not self.possibly_owned(item,patient):continue
            if item.day is not None and item.day!=day:continue
            certain=item.service_id==service_id and self.certainly_owned(item,patient) and item.day==day
            (known if certain else possible).append(item)
        return self.evidence('same_service_day_other_billing',{'service_id':service_id,'patient':patient,'day':day,'excluding_line_id':line_id},known,possible,len(known),len(known)+len(possible))

    def exclusion(self,rule,patient,day):
        known=[];possible=[]
        direction=self.contract['semantics']['exclusion_direction'];window=rule['days']
        for item in self.by_service[rule['anchor']]:
            if not self.possibly_owned(item,patient):continue
            if item.day is None:possible.append(item);continue
            delta=(date.fromisoformat(day)-date.fromisoformat(item.day)).days
            if abs(delta)>window:continue
            is_certain=(item.service_id==rule['anchor'] and self.certainly_owned(item,patient)
                        and item.quantity is not None and item.quantity>0 and abs(delta)<window)
            if direction=='uncertain_before_or_both' and delta<0:is_certain=False
            if direction=='uncertain_direction' and delta!=0:is_certain=False
            (known if is_certain else possible).append(item)
        detail=self.evidence('exclusion_window',{'anchor':rule['anchor'],'patient':patient,'day':day,'days':window,'direction':direction},known,possible,len(known),len(known)+len(possible))
        return (True if known else None if possible else False),detail
