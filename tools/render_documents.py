"""Optional rendering of the retained page-limited challenge documents.

Requires only requirements-docs.txt; prediction/evaluation replay does not import it.
"""
import hashlib
import json
from pathlib import Path
import re
from xml.sax.saxutils import escape
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1];REPORTS=ROOT/'reports'
m=json.loads((REPORTS/'metrics.json').read_text());w=json.loads((REPORTS/'workload.json').read_text())
full=m['full'];development=m['development'];check=m['check']

decision="""# Insurance auditing - decision log
Implementation candidate | Source commit 6fee1da60b74512156637a22be15d996a36627e1

## Evidence and execution boundary
The Work-session assistant extracted and source-reviewed finite JSON rules and frozen service mappings. This acquisition was author review. Python replays saved records without an LLM/API. Accepted bundles bind source, schema, mapping and review identities. Bundle traces identify the controlling clause and partner context. Unknown operators and incompatible packages fail before pricing.

## Service identity and incomplete opinions
Contract catalogs are not proof that an incomplete description identifies their only similar service. H1 development exposed one wrong specialty assignment (INV-H1-000236, 43,650 cents); all 39 analogous mapping keys were withdrawn. Essential qualifiers need independent description evidence; only generic noun elision retains a lower evidence grade. Billed rates/units never select service identity. If any necessary fact is unresolved, withhold the complete row; a known error alone does not establish the corrected total.

## Quantities, history and allocation
Use supplied billed quantities under the contracts' pricing rules; a wrong unit label does not authorize a guessed conversion. Composite hour/item quantities lack a second dimension and remain unsupported. Prior usage is strictly ordered by service date and line ID, over the supplied term; quarantined headers retain patient candidates, and missing identity stays uncertain. Conflicting ownership and duplicate service/day allocation have no invented split. A supported single capped line can be limited to the contractual maximum. Round integer cents half-up after each adjustment.

## Exclusions and amendments
H1/H2/H4 explicitly support bidirectional exclusions; H3/H5 direction is unresolved at nonzero distances. Use same-patient scope as the recorded contextual reading and withhold exactly-N-day boundary cases. H3 A1.1 applies seven repricings and two additions from service date 2025-01-01 despite the broad amendment header. A1.4.2 settlement protection uses the explicit interpretation that a valid invoice cannot settle before issue/service; no settlement field is fabricated.

## Hospital-specific missing facts
H4 section 1.4 defines instance as unit, but section 8 leaves patient aggregation unclear: bound same-patient through all-patient usage and emit only invariant outcomes. H5 line facility is absent; adopt invoice facility from the supplied relational shape and section 10.1, as an explicit assumption. Outcome-relevant opinions are capped at .65 confidence. H2 supplies admission/discharge dates but lacks actual submission, detailed episode/leave and possible exception evidence; invoice date is not submission. All H2 full opinions are withheld. Its 07:00 Service Day is not established by calendar dates; day-dependent diagnostics remain bounded or uncertain.

## Confidence, evaluation and remaining work
H1 patient groups were fixed before label development; the reserved check is now exposed and later checks are regressions. H1 sparse-error and target confidence are policy judgments, not demonstrated target calibration. Missing necessary facts cannot be repaired by a low score. Final mappings/rules, error history and omissions are retained. See evaluation_report.md and docs/implementation_changes.md. The independent audit's two findings are corrected; closure re-audit and external delivery remain pending.
"""
writeup=f"""# Insurance auditing - implementation write-up
LLM contract-to-schema with deterministic pricing | Local implementation candidate

## What was implemented
All five supplied contract sources were inspected and represented in finite, source-referenced JSON: H1 108 services, H2 76, H3 120, H4 98 and H5 84. The Work-session assistant interpreted definitions and conditions, proposed mappings, wrote code and tests, and performed author source review. Deterministic transcription aided extraction. Versioned instructions, raw candidates, revisions and accepted artifacts are retained. No programmatic model/API, local GPU or external compute was used.

One fixed Python interpreter selects service-date versions, assembles retrospective usage and executes bundles, facility/tier multipliers, premiums, weekend uplifts, deepest qualifying discounts and caps with exact staged half-up cents. It checks supported unit, arithmetic, contract-reference and eligibility faults. It emits a complete invoice opinion only when all necessary lines and context support the amount. Other invoices remain explicit omissions with source and reason traces.

## How results were measured
H1 has 913 unique invoice IDs, partitioned into 622 development and 291 check IDs using frozen patient-connected groups. Shared legitimate global usage remains in context across groups. Labels were used for development and evaluation, never as prediction inputs or answer-key mappings. The check was first opened after mapping revision 2 and confidence freeze. Current check results are regression evidence after that exposure; full H1 is development-inclusive.

Development emits {development['covered']}/622 opinions with {development['whole_row_success_count']} correct flags and exact amounts. Check emits {check['covered']}/291 with {check['whole_row_success_count']} joint successes. Full H1 emits {full['covered']}/913 ({full['coverage']*100:.2f}% coverage), with {full['whole_row_success_count']} joint successes, five true error flags and zero false flags. Error recall across all 58 erroneous IDs is {full['flag_metrics_all']['recall']*100:.2f}% and F1 is {full['flag_metrics_all']['f1']:.4f}. The other 53 errors are withheld. High conditional accuracy therefore accompanies low recall; it is not a claim of broad accuracy.

The separate evaluation report gives every original label's support/detection and per-family precision, recall and F1 through an explicit crosswalk. Abstentions are missed positives for population recall and excluded from conditional accuracy; they are never correct negatives. Joint success means flag plus exact expected cents, with billed totals and complete traces separately verified. Free-text diagnostic correctness is measured separately. Undefined denominators are not filled with perfect scores.

## Target output
The validated six-column submission has 340 opinions: H3 148/932 (five flagged), H4 64/835 (one flagged) and H5 128/1,050 (none flagged). H2 has zero/1,125. Every source occurrence and unique opinion identity is accounted for. All source services were attempted; remaining omissions reflect missing evidence and unsupported corrections. There are no H2-H5 labels, so target accuracy is unknown.

<!-- PAGEBREAK -->

# Uncertainty, reproducibility and next work

## Where uncertainty matters
An initial mapping accepted generic outpatient radiotherapy as a metabolic service. Development invoice INV-H1-000236 exposed a 43,650-cent over-correction. The correction withdrew all 39 analogous missing-essential-qualifier keys, rather than patching that invoice or learning a billed price as identity. Coverage fell substantially. Current systemic omissions arise from insufficient description evidence, conflicting identities or damaged dates, and uncertain cross-invoice context or allocation. The report gives actual examples; these omissions are distinguished from observed emitted errors.

H3 service-date amendment precedence is explicit; settlement protection uses a recorded valid-invoice chronology interpretation. H3/H5 exclusion direction and exactly-N-day boundaries remain uncertain. H4 instance-to-unit equivalence is explicit, but patient scope of cumulative usage is bounded. H5 line facility is unavailable, so invoice facility is an explicit contextual projection, never a claimed observed line field. All 128 emitted H5 rows have an outcome-relevant projection and .65 confidence.

H2 was fully inspected, including definitions and all 76 rate clauses. Article XIII conditions invoice effectiveness on actual submission within 60 days of episode discharge, with possible written exceptions. Admission/discharge dates are supplied; actual submission, detailed episode/leave and possible written-exception evidence are absent. The CSV invoice date cannot prove submission. Its 07:00 Service Day also lacks timestamps or qualifying duration evidence. Pricing is available diagnostically, but no complete payable H2 opinion is claimed.

## Confidence and verification
Development supported correct-row tiers use conservative .95/.90 scores; sparse error tiers use .65 judgment. Novel reviewed target rows use .80/.70; relevant interpretation or invariant-uncertainty qualifications cap .65. These are explicitly limited scores, not proven target probability calibration. No number substitutes for missing necessary facts.

The 75 tests cover schema rejection, dates/amendments, exact arithmetic, thresholds, cross-invoice rules, uncertainty, metrics and failed/stale export. The first independent audit required two corrections: quarantined-header patient ownership now remains uncertain context, and applied bundles cite their controlling clause and partner evidence. Author regressions preserve the failing fixtures and compare all hospitals before/after; no submission, metric or confidence value changed. All 352 emitted bundle substitutions were checked against source/context. Full permutation, label isolation and clean replay were rerun. Independent closure re-audit remains pending.

## Reproduction and further work
Clone the project, select Python 3.12.13, and run the README's reproduce command. It recomputes the source CSVs through retained accepted schemas/mappings, then exports and evaluates. Core execution/tests use only the standard library, without model keys or Work state. Outputs can be removed before replay; historical attempts are not required. PDF rendering alone has separately pinned optional dependencies. Fresh LLM acquisition is a distinct process and is not promised to regenerate identical schemas.

For further development, first obtain authoritative service aliases and the absent H2 submission/episode facts; resolve H3/H5 direction and H4 scope with the contract owner. Then expand source-derived fixtures and validate the changed mappings/rules on new labelled examples, including withheld invoices. Evaluate confidence on independent target evidence and measure the unresolved review workload before scaling. More compute alone does not resolve missing source facts. External publishing, assessor access, final presentation and actual email delivery remain separate, unperformed stages.
"""

font_dir=Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('AuditSans',str(font_dir/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('AuditSansBold',str(font_dir/'VeraBd.ttf')))
styles={
    'body':ParagraphStyle('body',fontName='AuditSans',fontSize=9.5,leading=12.8,spaceAfter=7,textColor=colors.HexColor('#253247')),
    'h1':ParagraphStyle('h1',fontName='AuditSansBold',fontSize=16,leading=20,spaceAfter=13,textColor=colors.HexColor('#17324d')),
    'h2':ParagraphStyle('h2',fontName='AuditSansBold',fontSize=10.3,leading=13.7,spaceBefore=5,spaceAfter=5,textColor=colors.HexColor('#17324d'))}


def render(name,text,limit):
    text=text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('\u2019',"'")
    (REPORTS/f'{name}.md').write_text(text,encoding='utf-8')
    pdf=REPORTS/f'{name}.pdf';flow=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        if block=='<!-- PAGEBREAK -->':flow.append(PageBreak());continue
        for paragraph in block.split('\n'):
            kind='h1' if paragraph.startswith('# ') else 'h2' if paragraph.startswith('## ') else 'body'
            content=paragraph[2:] if kind=='h1' else paragraph[3:] if kind=='h2' else paragraph
            flow.append(Paragraph(escape(content),styles[kind]))
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#b9c5d0'));canvas.line(42,35,A4[0]-42,35)
        canvas.setFillColor(colors.HexColor('#58677b'));canvas.setFont('AuditSans',8)
        canvas.drawString(42,23,'Insurance auditing | implementation evidence')
        canvas.drawRightString(A4[0]-42,23,str(doc.page))
    SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=45,
        title=name.replace('_',' '),author='Work-assisted implementation',invariant=1).build(flow,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(pdf);pages=len(reader.pages)
    if pages>limit:raise ValueError(f'{name}: {pages} pages exceeds {limit}')
    extracted='\n'.join(page.extract_text() for page in reader.pages)
    if not extracted.strip():raise ValueError('Empty rendered document')
    return {'file':str(pdf.relative_to(ROOT)),'pages':pages,'limit':limit,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'text_characters':len(extracted),'markdown_sha256':hashlib.sha256((REPORTS/f'{name}.md').read_bytes()).hexdigest()}


result={'decision_log':render('decision_log',decision,1),'submission_writeup':render('submission_writeup',writeup,2),
        'visual_inspection':'pending; page count/text extraction are not visual layout proof'}
(REPORTS/'document_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
