import os

BASE = 'C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao/slides/unpacked_v2/ppt/'

classes = [
    ('Requeima',        'cls_d01.jpg'),
    ('Septoriose',      'cls_d02.jpg'),
    ('Pinta Preta',     'cls_d03.jpg'),
    ('Mancha Alvo',     'cls_d03b.jpg'),
    ('Mofo Foliar',     'cls_d05.jpg'),
    ('Vira-Cabeca',     'cls_d06.jpg'),
    ('Mosaico',         'cls_d06b.jpg'),
    ('Acaro/Brz.',      'cls_d07.jpg'),
    ('Mancha Bact.',    'cls_d09.jpg'),
    ('Saudavel',        'cls_saudavel.jpg'),
]

IMG_W = 1640000
IMG_H = 1540000
GAP_X = 88000
LABEL_H = 210000
MARGIN = 292000

total_w = 5 * IMG_W + 4 * GAP_X
start_x = (9144000 - total_w) // 2

ROW1_Y = 580000
ROW2_Y = ROW1_Y + IMG_H + LABEL_H + 140000

def x_pos(col):
    return start_x + col * (IMG_W + GAP_X)

def make_pic(eid, rid, x, y, label):
    border_color = '88CC88' if label == 'Saudavel' else '3A6A3A'
    return (
        f'      <p:pic>\n'
        f'        <p:nvPicPr>\n'
        f'          <p:cNvPr id="{eid}" name="img{eid}"/>\n'
        f'          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>\n'
        f'          <p:nvPr/>\n'
        f'        </p:nvPicPr>\n'
        f'        <p:blipFill>\n'
        f'          <a:blip r:embed="{rid}"/>\n'
        f'          <a:stretch><a:fillRect/></a:stretch>\n'
        f'        </p:blipFill>\n'
        f'        <p:spPr>\n'
        f'          <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{IMG_W}" cy="{IMG_H}"/></a:xfrm>\n'
        f'          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
        f'          <a:ln w="19050"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill>'
        f'<a:prstDash val="solid"/></a:ln>\n'
        f'        </p:spPr>\n'
        f'      </p:pic>'
    )

def make_label(eid, text, x, y):
    color = '88FF88' if text == 'Saudavel' else 'CCCCCC'
    return (
        f'      <p:sp>\n'
        f'        <p:nvSpPr><p:cNvPr id="{eid}" name="lbl{eid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
        f'        <p:spPr>\n'
        f'          <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{IMG_W}" cy="{LABEL_H}"/></a:xfrm>\n'
        f'          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
        f'          <a:noFill/><a:ln/>\n'
        f'        </p:spPr>\n'
        f'        <p:txBody>\n'
        f'          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>\n'
        f'          <a:lstStyle/>\n'
        f'          <a:p>\n'
        f'            <a:pPr algn="ctr" indent="0" marL="0"><a:buNone/></a:pPr>\n'
        f'            <a:r><a:rPr lang="pt-BR" sz="800" b="1" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
        f'<a:t>{text}</a:t></a:r>\n'
        f'          </a:p>\n'
        f'        </p:txBody>\n'
        f'      </p:sp>'
    )

shapes = []
eid = 10
for i, (label, img) in enumerate(classes):
    row = i // 5
    col = i % 5
    rid = f'rId{i+1}'
    x = x_pos(col)
    y = ROW1_Y if row == 0 else ROW2_Y
    shapes.append(make_pic(eid, rid, x, y, label))
    eid += 1
    shapes.append(make_label(eid, label, x, y + IMG_H + 18000))
    eid += 1

shapes_xml = '\n'.join(shapes)

slide_xml = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
    '  <p:cSld name="Slide Classes">\n'
    '    <p:bg>\n'
    '      <p:bgPr><a:solidFill><a:srgbClr val="1A3A1A"/></a:solidFill></p:bgPr>\n'
    '    </p:bg>\n'
    '    <p:spTree>\n'
    '      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>\n'
    '      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>\n'
    '      <!-- Label -->\n'
    '      <p:sp>\n'
    '        <p:nvSpPr><p:cNvPr id="2" name="LabelBg"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
    '        <p:spPr>\n'
    '          <a:xfrm><a:off x="274320" y="80000"/><a:ext cx="2000000" cy="220000"/></a:xfrm>\n'
    '          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
    '          <a:solidFill><a:srgbClr val="C8860A"/></a:solidFill>\n'
    '          <a:ln w="12700"><a:solidFill><a:srgbClr val="C8860A"/></a:solidFill>'
    '<a:prstDash val="solid"/></a:ln>\n'
    '        </p:spPr>\n'
    '      </p:sp>\n'
    '      <p:sp>\n'
    '        <p:nvSpPr><p:cNvPr id="3" name="LabelText"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
    '        <p:spPr>\n'
    '          <a:xfrm><a:off x="274320" y="80000"/><a:ext cx="2000000" cy="220000"/></a:xfrm>\n'
    '          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
    '          <a:noFill/><a:ln/>\n'
    '        </p:spPr>\n'
    '        <p:txBody>\n'
    '          <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>\n'
    '          <a:lstStyle/>\n'
    '          <a:p>\n'
    '            <a:pPr algn="ctr" indent="0" marL="0"><a:buNone/></a:pPr>\n'
    '            <a:r><a:rPr lang="pt-BR" sz="900" b="1" kern="0" dirty="0">'
    '<a:solidFill><a:srgbClr val="1A3A1A"/></a:solidFill></a:rPr>'
    '<a:t>07 | 10 CLASSES</a:t></a:r>\n'
    '          </a:p>\n'
    '        </p:txBody>\n'
    '      </p:sp>\n'
    '      <!-- Title -->\n'
    '      <p:sp>\n'
    '        <p:nvSpPr><p:cNvPr id="4" name="Title"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
    '        <p:spPr>\n'
    '          <a:xfrm><a:off x="274320" y="340000"/><a:ext cx="8595360" cy="210000"/></a:xfrm>\n'
    '          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
    '          <a:noFill/><a:ln/>\n'
    '        </p:spPr>\n'
    '        <p:txBody>\n'
    '          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>\n'
    '          <a:lstStyle/>\n'
    '          <a:p>\n'
    '            <a:pPr indent="0" marL="0"><a:buNone/></a:pPr>\n'
    '            <a:r><a:rPr lang="pt-BR" sz="1600" b="1" dirty="0">'
    '<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr>'
    '<a:t>9 doencas + saudavel — o que o Ceres classifica</a:t></a:r>\n'
    '          </a:p>\n'
    '        </p:txBody>\n'
    '      </p:sp>\n'
    + shapes_xml + '\n'
    '      <!-- Footer -->\n'
    '      <p:sp>\n'
    '        <p:nvSpPr><p:cNvPr id="90" name="FooterBg"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
    '        <p:spPr>\n'
    '          <a:xfrm><a:off x="0" y="4892040"/><a:ext cx="9144000" cy="251460"/></a:xfrm>\n'
    '          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
    '          <a:solidFill><a:srgbClr val="2A4A2A"/></a:solidFill>\n'
    '          <a:ln w="0"><a:noFill/></a:ln>\n'
    '        </p:spPr>\n'
    '      </p:sp>\n'
    '      <p:sp>\n'
    '        <p:nvSpPr><p:cNvPr id="91" name="FooterText"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
    '        <p:spPr>\n'
    '          <a:xfrm><a:off x="274320" y="4892040"/><a:ext cx="8595360" cy="251460"/></a:xfrm>\n'
    '          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>\n'
    '          <a:noFill/><a:ln/>\n'
    '        </p:spPr>\n'
    '        <p:txBody>\n'
    '          <a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>\n'
    '          <a:lstStyle/>\n'
    '          <a:p>\n'
    '            <a:pPr algn="ctr" indent="0" marL="0"><a:buNone/></a:pPr>\n'
    '            <a:r><a:rPr lang="pt-BR" sz="800" dirty="0">'
    '<a:solidFill><a:srgbClr val="FFFFFF"><a:alpha val="70000"/></a:srgbClr></a:solidFill></a:rPr>'
    '<a:t>Dataset: PlantVillage (Hughes &amp; Salathe 2015) CC BY 4.0  ·  18.160 imagens</a:t></a:r>\n'
    '          </a:p>\n'
    '        </p:txBody>\n'
    '      </p:sp>\n'
    '    </p:spTree>\n'
    '  </p:cSld>\n'
    '  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>\n'
    '</p:sld>\n'
)

with open(BASE + 'slides/slide17.xml', 'w', encoding='utf-8') as f:
    f.write(slide_xml)
print('slide17.xml OK')

img_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
layout_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout'
rels_lines = []
for i, (_, img) in enumerate(classes):
    rels_lines.append(f'  <Relationship Id="rId{i+1}" Type="{img_type}" Target="../media/{img}"/>')
rels_lines.append(f'  <Relationship Id="rId11" Type="{layout_type}" Target="../slideLayouts/slideLayout1.xml"/>')

rels_xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            + '\n'.join(rels_lines) + '\n</Relationships>\n')

with open(BASE + 'slides/_rels/slide17.xml.rels', 'w', encoding='utf-8') as f:
    f.write(rels_xml)
print('slide17.xml.rels OK')
