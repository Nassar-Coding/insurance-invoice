"""Render current page-limited Markdown; no acquisition or prediction imports."""
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
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


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
        canvas.drawString(42, 23, 'Insurance auditing | audited implementation')
        canvas.drawRightString(A4[0]-42, 23, str(doc.page))

    results = {}
    for name, limit in [('decision_log', 1), ('submission_writeup', 2)]:
        source = ROOT/f'reports/{name}.md'
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
        pdf = ROOT/f'reports/{name}.pdf'
        SimpleDocTemplate(str(pdf), pagesize=A4, rightMargin=42, leftMargin=42,
                          topMargin=38, bottomMargin=45, title=name.replace('_', ' '),
                          author='Work-assisted implementation', invariant=1).build(
                              flow, onFirstPage=footer, onLaterPages=footer)
        reader = PdfReader(pdf)
        assert len(reader.pages) <= limit, f'{name}: page limit exceeded'
        extracted = '\n'.join(p.extract_text() for p in reader.pages)
        assert extracted.strip() and 'closure re-audit passed' in extracted
        results[name] = {'path':str(pdf.relative_to(ROOT)), 'pages':len(reader.pages),
                         'page_limit':limit, 'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
                         'markdown_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                         'extracted_text_characters':len(extracted)}
    report = {'status':'page-count and text checks passed', 'documents':results,
              'dependencies':{n:importlib.metadata.version(n) for n in
                              ['reportlab','pillow','charset-normalizer','pypdf']},
              'visual_inspection':'Separate page-image inspection required for a new rendering.'}
    out = ROOT/'evidence/publishing/document_checks_latest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
