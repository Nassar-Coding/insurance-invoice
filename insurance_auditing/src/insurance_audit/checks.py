"""Supported non-price checks and explicit correction/abstention boundaries."""
from .pricing import Uncertain


def validate_line_facts(line,invoice,service,contract,context):
    if line.quantity<=0:raise Uncertain('unsupported_nonpositive_quantity',{'line_id':line.line_id,'quantity':line.quantity})
    if not contract['term'][0]<=line.service_date<=contract['term'][1]:raise Uncertain('service_date_outside_term',{'line_id':line.line_id,'date':line.service_date})
    if contract['semantics']['service_date_not_after_invoice'] and line.service_date>invoice.invoice_date:raise Uncertain('service_date_after_invoice',{'line_id':line.line_id,'date':line.service_date,'invoice_date':invoice.invoice_date})
    if line.line_id in context.duplicate_line_ids:raise Uncertain('reused_line_identity',line.line_id)
    if service['daily_cap'] is not None and contract['semantics']['service_day']=='seven_am_unobserved':
        interval=context.daily(service['id'],invoice.patient_id,line.service_date)
        if interval['upper'] is None or interval['upper']>service['daily_cap']:
            raise Uncertain('unobserved_service_day_cap_allocation',interval)
    if contract['semantics']['duplicate_policy']=='no_explicit_service_date_prohibition':
        return {'kind':'no_explicit_service_date_prohibition','certain_records':0,'possible_records':0}
    other=context.competitors(service['id'],invoice.patient_id,line.service_date,line.line_id)
    if other['certain_records']:raise Uncertain('duplicate_service_day_allocation',other)
    if other['possible_records']:raise Uncertain('possible_duplicate_service_day',other)
    return other


def line_result(line,service,price):
    quantity=line.quantity
    categories=[]
    if line.unit_basis_as_billed!=service['unit']:categories.append('unit_basis_mismatch')
    if line.line_total_cents!=line.quantity*line.unit_price_cents:categories.append('line_arithmetic_mismatch')
    if service['daily_cap'] is not None and quantity>service['daily_cap']:
        quantity=service['daily_cap'];categories.append('daily_quantity_cap')
    expected=price['rate']*quantity
    if line.unit_price_cents!=price['rate']:categories.append('effective_rate_mismatch')
    if line.line_total_cents!=expected:categories.append('line_amount_mismatch')
    if price['excluded'] and (line.unit_price_cents!=0 or line.line_total_cents!=0):categories.append('nonbillable_service')
    return {'expected_total_cents':expected,'expected_unit_rate_cents':price['rate'],'billable_quantity':quantity,
            'error_categories':sorted(set(categories))}
