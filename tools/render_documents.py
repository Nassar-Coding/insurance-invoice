"""Render the page-limited Markdown deliverables to PDF.

Packaging only: no acquisition or prediction imports, and nothing here can
affect a prediction. Optional — `requirements-docs.txt` carries the rendering
dependencies and the prediction runtime needs none of them.

    python -m pip install -r requirements-docs.txt
    python tools/render_documents.py

`reports/decision_log.md` must fit one page and `reports/submission_writeup.md`
two, which is the brief's limit for each. The markdown is authoritative. This
asserts each rendering still fits its limit, checks the extracted text where
`pypdf` imports cleanly, and records the hash of every markdown and PDF so a
reader can tell whether a PDF matches the markdown it was made from.
"""
import hashlib
import html
import importlib.metadata
import json
import re
from pathlib import Path

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

try:  # optional: only used for the extractable-text check
    from pypdf import PdfReader
except BaseException:  # a broken crypto backend panics rather than raising Exception
    PdfReader = None

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {'decision_log': (1, 'decision log'),
             'submission_writeup': (2, 'write-up')}

INK = colors.HexColor('#253247')
HEAD = colors.HexColor('#17324d')
RULE = colors.HexColor('#b9c5d0')
BAND = colors.HexColor('#eef2f6')


def styles(body_size, leading):
    """Body size is the knob a page limit is met with; it never goes below 10pt."""
    assert body_size >= 10, 'body text must stay at least 10pt to be readable'
    return {
        'body': ParagraphStyle('body', fontName='AuditSans', fontSize=body_size,
                               leading=leading, spaceAfter=leading*0.42, textColor=INK),
        'h1': ParagraphStyle('h1', fontName='AuditSansBold', fontSize=body_size+5.5,
                             leading=leading+6, spaceAfter=leading*0.55, textColor=HEAD),
        'h2': ParagraphStyle('h2', fontName='AuditSansBold', fontSize=body_size+0.9,
                             leading=leading+1.4, spaceBefore=leading*0.62,
                             spaceAfter=leading*0.26, textColor=HEAD),
        'cell': ParagraphStyle('cell', fontName='AuditSans', fontSize=body_size-0.6,
                               leading=leading-1.3, textColor=INK),
        'cellhead': ParagraphStyle('cellhead', fontName='AuditSansBold', fontSize=body_size-0.6,
                                   leading=leading-1.3, textColor=HEAD),
    }


def inline(text, size):
    """Markdown inline spans to reportlab markup, escaping everything else."""
    guard = {}

    def stash(markup):
        key = f'\x00{len(guard)}\x00'
        guard[key] = markup
        return key

    out = re.sub(r'\[([^\]]+)\]\([^)]+\)', lambda m: m.group(1), text)
    out = re.sub(r'`([^`]+)`',
                 lambda m: stash(f'<font name="Courier" size="{size-0.7:.1f}">'
                                 f'{html.escape(m.group(1))}</font>'), out)
    out = re.sub(r'\*\*([^*]+)\*\*', lambda m: stash(f'<b>{html.escape(m.group(1))}</b>'), out)
    out = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])',
                 lambda m: stash(f'<i>{html.escape(m.group(1))}</i>'), out)
    out = html.escape(out)
    for key, markup in guard.items():
        out = out.replace(html.escape(key), markup)
    return out


def table(rows, width, style, size):
    data = [[Paragraph(inline(c, size), style['cellhead']) for c in rows[0]]]
    data += [[Paragraph(inline(c, size), style['cell']) for c in row] for row in rows[1:]]
    columns = len(rows[0])
    first = width * (0.46 if columns <= 3 else 0.32)
    widths = [width] if columns == 1 else [first] + [(width-first)/(columns-1)]*(columns-1)
    built = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    built.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BAND),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, RULE),
        ('LINEBELOW', (0, 1), (-1, -2), 0.25, colors.HexColor('#dde4ea')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6)]))
    return built


def flowables(text, width, style, size):
    flow, lines, i, paragraph = [], text.split('\n'), 0, []

    def flush():
        if paragraph:
            flow.append(Paragraph(inline(' '.join(paragraph), size), style['body']))
            paragraph.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i+1].strip()):
            flush()
            rows = [[c.strip() for c in line.strip().strip('|').split('|')]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            flow += [Spacer(1, 2.5), table(rows, width, style, size), Spacer(1, 6)]
            continue
        if line.startswith('# '):
            flush(); flow.append(Paragraph(inline(line[2:], size), style['h1']))
        elif line.startswith('## '):
            flush(); flow.append(Paragraph(inline(line[3:], size), style['h2']))
        elif not line.strip():
            flush()
        else:
            paragraph.append(line.strip())
        i += 1
    flush()
    return flow


def render(name, limit, title, body_size, leading):
    margin = 15*mm
    style = styles(body_size, leading)
    source = ROOT/f'reports/{name}.md'
    pdf = ROOT/f'reports/{name}.pdf'

    def furniture(canvas, doc):
        canvas.setStrokeColor(RULE)
        canvas.line(margin, 32, A4[0]-margin, 32)
        canvas.setFillColor(colors.HexColor('#58677b'))
        canvas.setFont('AuditSans', 7.8)
        canvas.drawString(margin, 21, f'Insurance invoice auditing | {title}')
        canvas.drawRightString(A4[0]-margin, 21, str(doc.page))

    document = SimpleDocTemplate(str(pdf), pagesize=A4, leftMargin=margin, rightMargin=margin,
                                 topMargin=14*mm, bottomMargin=15*mm, title=title,
                                 author='Insurance invoice auditing', invariant=1)
    document.build(flowables(source.read_text(), A4[0]-2*margin, style, body_size),
                   onFirstPage=furniture, onLaterPages=furniture)
    pages = document.page
    assert pages <= limit, f'{name}: page limit exceeded, {pages} pages against {limit}'
    if PdfReader is None:
        check, characters = 'skipped: pypdf did not import', None
    else:
        extracted = '\n'.join(page.extract_text() for page in PdfReader(pdf).pages)
        assert extracted.strip(), f'{name}: rendered PDF carries no extractable text'
        check, characters = 'passed', len(extracted)
    return {'path': str(pdf.relative_to(ROOT)), 'pages': pages, 'page_limit': limit,
            'body_point_size': body_size, 'extracted_text_check': check,
            'extracted_text_characters': characters,
            'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'markdown_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}


def main():
    fonts = Path(reportlab.__file__).parent/'fonts'
    for alias, filename in [('AuditSans', 'Vera.ttf'), ('AuditSansBold', 'VeraBd.ttf'),
                            ('AuditSansItalic', 'VeraIt.ttf'), ('AuditSansBoldItalic', 'VeraBI.ttf')]:
        pdfmetrics.registerFont(TTFont(alias, str(fonts/filename)))
    pdfmetrics.registerFontFamily('AuditSans', normal='AuditSans', bold='AuditSansBold',
                                  italic='AuditSansItalic', boldItalic='AuditSansBoldItalic')
    # (body point size, leading). The brief caps the log at one page and the
    # write-up at two; body text never drops below 10pt to hit a limit.
    sizes = {'decision_log': (10.4, 13.4), 'submission_writeup': (10.0, 12.6)}
    report = {'status': 'page-count and text checks passed',
              'documents': {name: render(name, limit, title, *sizes[name])
                            for name, (limit, title) in sorted(DOCUMENTS.items())},
              'dependencies': {n: importlib.metadata.version(n) for n in
                               ['reportlab', 'pillow', 'charset-normalizer', 'pypdf']}}
    (ROOT/'reports/document_render.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
