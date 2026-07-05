# -*- coding: utf-8 -*-
"""Renderiza o Relatorio Final de Extensao II em PDF (estilo Ceres)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, Image, KeepTogether, Preformatted)
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
import relatorio_conteudo as C

OUT = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao/relatorio_final_extensao.pdf"

VERDE = HexColor('#1A3A1A'); CARD = HexColor('#2D5A2D'); DOUR = HexColor('#C8860A')
CREME = HexColor('#F5F0E8'); CINZA = HexColor('#2B2B2B'); MUTED = HexColor('#777777')

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=1.8*cm, title="Relatorio Final Extensao II - Ceres")


def s(name, **kw): return ParagraphStyle(name, **kw)


TIT  = s('tit', fontSize=21, fontName='Helvetica-Bold', textColor=VERDE, leading=25, spaceAfter=6, alignment=TA_CENTER)
SUB  = s('sub', fontSize=9.5, fontName='Helvetica', textColor=MUTED, leading=13, spaceAfter=4, alignment=TA_CENTER)
H1   = s('h1', fontSize=15, fontName='Helvetica-Bold', textColor='#FFFFFF', leading=18)
H2   = s('h2', fontSize=12, fontName='Helvetica-Bold', textColor=VERDE, spaceBefore=10, spaceAfter=4)
H3   = s('h3', fontSize=10.5, fontName='Helvetica-Bold', textColor=DOUR, spaceBefore=7, spaceAfter=3)
BODY = s('body', fontSize=9.7, fontName='Helvetica', textColor=CINZA, leading=14, spaceAfter=5)
BUL  = s('bul', fontSize=9.7, fontName='Helvetica', textColor=CINZA, leading=13.5, spaceAfter=3, leftIndent=12, bulletIndent=2)
CAP  = s('cap', fontSize=8.3, fontName='Helvetica-Oblique', textColor=MUTED, spaceBefore=2, spaceAfter=8, alignment=TA_CENTER)
CELL = s('cell', fontSize=8.7, fontName='Helvetica', textColor=CINZA, leading=11)
CELLB = s('cellb', fontSize=8.7, fontName='Helvetica-Bold', textColor='#FFFFFF', leading=11)
CODE = s('code', fontSize=8, fontName='Courier', textColor=HexColor('#1A2D1A'), leading=10.5)


def md(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def h1_bar(txt):
    t = Table([[Paragraph(md(txt), H1)]], colWidths=[17*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), VERDE),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return t


def make_table(headers, rows):
    ncol = len(headers)
    data = [[Paragraph(md(h), CELLB) for h in headers]]
    for r in rows:
        data.append([Paragraph(md(c), CELL) for c in r])
    total = 17.0
    if ncol == 2:
        cw = [total*0.32, total*0.68] if len(headers[0]) < 14 else [total*0.5, total*0.5]
    elif ncol == 5:
        cw = [total*0.07, total*0.42, total*0.15, total*0.13, total*0.23]
    else:
        cw = [total/ncol]*ncol
    t = Table(data, colWidths=[w*cm for w in cw], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CARD),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['#FFFFFF', HexColor('#F7F3EC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def figure(path, caption):
    w, h = PILImage.open(path).size
    iw = 15.5*cm
    ih = iw*h/w
    maxh = 10.5*cm
    if ih > maxh:
        ih = maxh; iw = ih*w/h
    return KeepTogether([Spacer(1, 4), Image(path, width=iw, height=ih), Paragraph(md(caption), CAP)])


def code_block(txt):
    t = Table([[Preformatted(txt, CODE)]], colWidths=[16.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F2EEE6')),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#D8D0C0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([Spacer(1, 2), t, Spacer(1, 6)])


def fig_grid(cols, items):
    """Grade de imagens (cols por linha) com legenda pequena sob cada uma."""
    total = 17.0
    cellw = total / cols
    imgw = (cellw - 0.5) * cm
    rows = []
    for i in range(0, len(items), cols):
        chunk = items[i:i+cols]
        cells = []
        for path, cap in chunk:
            w, h = PILImage.open(path).size
            iw = imgw
            ih = iw * h / w
            maxh = 8.2 * cm
            if ih > maxh:
                ih = maxh; iw = ih * w / h
            inner = [Image(path, width=iw, height=ih), Spacer(1, 2), Paragraph(md(cap), CAP)]
            cells.append(inner)
        while len(cells) < cols:
            cells.append([Spacer(1, 1)])
        rows.append(cells)
    t = Table(rows, colWidths=[cellw*cm]*cols)
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 4)])


story = [Paragraph(C.TITULO, TIT), Paragraph(C.SUBTITULO, SUB),
         HRFlowable(width='100%', thickness=1.2, color=VERDE, spaceBefore=6, spaceAfter=10)]

for blk in C.BLOCKS:
    kind = blk[0]
    if kind == 'h1':
        story.append(Spacer(1, 6)); story.append(h1_bar(blk[1])); story.append(Spacer(1, 6))
    elif kind == 'h2':
        story.append(Paragraph(md(blk[1]), H2))
    elif kind == 'h3':
        story.append(Paragraph(md(blk[1]), H3))
    elif kind == 'p':
        story.append(Paragraph(md(blk[1]), BODY))
    elif kind == 'bul':
        for it in blk[1]:
            story.append(Paragraph(md(it), BUL, bulletText='•'))
    elif kind == 'tab':
        story.append(Spacer(1, 2)); story.append(make_table(blk[1], blk[2])); story.append(Spacer(1, 6))
    elif kind == 'fig':
        story.append(figure(blk[1], blk[2]))
    elif kind == 'code':
        story.append(code_block(blk[1]))
    elif kind == 'figrow':
        story.append(fig_grid(blk[1], blk[2]))

doc.build(story)
print("OK:", OUT)
