"""Render reports/decision_log.md to a one-page PDF.

Packaging only: no acquisition or prediction imports, and nothing here can
affect a prediction. Optional — `requirements-docs.txt` carries the rendering
dependencies and the prediction runtime needs none of them.

    python -m pip install -r requirements-docs.txt
    python tools/render_decision_log.py

The markdown is authoritative. This asserts the rendering still fits one page,
checks the extracted text where `pypdf` imports cleanly, and records the hash of
both files so a reader can tell whether the PDF matches the markdown it was made
from.
"""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

try:  # optional: only used for the extractable-text check
    from pypdf import PdfReader
except BaseException:  # a broken crypto backend panics rather than raising Exception
    PdfReader = None

ROOT = Path(__file__).resolve().parents[1]
PAGE_LIMIT = 1


def main():
    fonts = Path(reportlab.__file__).parent/'fonts'
    pdfmetrics.registerFont(TTFont('AuditSans', str(fonts/'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('AuditSansBold', str(fonts/'VeraBd.ttf')))
    styles = {
        'body': ParagraphStyle('body', fontName='AuditSans', fontSize=9.5, leading=12.8,
                               spaceAfter=7, textColor=colors.HexColor('#253247')),
        'h1': ParagraphStyle('h1', fontName='AuditSansBold', fontSize=16, leading=20,
                             spaceAfter=13, textColor=colors.HexColor('#17324d')),
        'h2': ParagraphStyle('h2', fontName='AuditSansBold', fontSize=10.3, leading=13.7,
                             spaceBefore=5, spaceAfter=5, textColor=colors.HexColor('#17324d'))}

    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor('#b9c5d0'))
        canvas.line(42, 35, A4[0]-42, 35)
        canvas.setFillColor(colors.HexColor('#58677b'))
        canvas.setFont('AuditSans', 8)
        canvas.drawString(42, 23, 'Insurance invoice auditing | decision log')
        canvas.drawRightString(A4[0]-42, 23, str(doc.page))

    source = ROOT/'reports/decision_log.md'
    text = source.read_text()
    flow = []
    for block in re.split(r'\n\s*\n', text.strip()):
        if block == '<!-- PAGEBREAK -->':
            flow.append(PageBreak())
            continue
        for paragraph in block.split('\n'):
            kind = 'h1' if paragraph.startswith('# ') else 'h2' if paragraph.startswith('## ') else 'body'
            content = paragraph[2:] if kind == 'h1' else paragraph[3:] if kind == 'h2' else paragraph
            flow.append(Paragraph(escape(content), styles[kind]))
    pdf = ROOT/'reports/decision_log.pdf'
    document = SimpleDocTemplate(str(pdf), pagesize=A4, rightMargin=42, leftMargin=42,
                                 topMargin=38, bottomMargin=45, title='decision log',
                                 author='Insurance invoice auditing', invariant=1)
    document.build(flow, onFirstPage=footer, onLaterPages=footer)
    pages = document.page
    assert pages <= PAGE_LIMIT, f'page limit exceeded: {pages} pages'
    if PdfReader is None:
        text_check = 'skipped: pypdf did not import'
        characters = None
    else:
        extracted = '\n'.join(page.extract_text() for page in PdfReader(pdf).pages)
        assert extracted.strip(), 'rendered PDF carries no extractable text'
        text_check = 'passed'
        characters = len(extracted)
    report = {'status': 'page-count check passed', 'extracted_text_check': text_check,
              'document': {'path': str(pdf.relative_to(ROOT)), 'pages': pages,
                           'page_limit': PAGE_LIMIT,
                           'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
                           'markdown_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                           'extracted_text_characters': characters},
              'dependencies': {n: importlib.metadata.version(n) for n in
                               ['reportlab', 'pillow', 'charset-normalizer', 'pypdf']}}
    (ROOT/'reports/decision_log_render.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
