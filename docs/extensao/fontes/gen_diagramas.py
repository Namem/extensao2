# -*- coding: utf-8 -*-
"""Gera os 4 diagramas tecnicos do Ceres Diagnostico em SVG (tema Ceres).
Saida: casos_de_uso.svg, diagrama_classes.svg, mer.svg, arquitetura.svg
Renderizar para PNG via render.js (resvg)."""
import os

OUT = "C:/Users/Rachid/Desktop/NR/Semestre 2026_1/extensao/ceres-diagnostico/docs/extensao/anexos/diagramas"

# Paleta Ceres
BG      = "#F5F0E8"   # creme (fundo)
GREEN   = "#1A3A1A"   # verde escuro (titulos/bordas)
CARD    = "#2D5A2D"   # verde card
GOLD    = "#C8860A"   # dourado (destaque)
INK     = "#261E19"   # texto escuro
PAPER   = "#FBF7F0"   # cartao claro
LINE    = "#5D6B52"   # linhas
MUTED   = "#6B6256"   # texto secundario
BLUE    = "#0C447C"   # dispositivo/externo
BLUEBG  = "#E8F1FB"

FONT = "Segoe UI, Arial, sans-serif"
MONO = "Consolas, monospace"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def header(w, h, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L8,3 L0,6 Z" fill="{GREEN}"/>
  </marker>
  <marker id="arrowOpen" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L9,4 L0,8" fill="none" stroke="{GREEN}" stroke-width="1.4"/>
  </marker>
  <marker id="tri" markerWidth="16" markerHeight="14" refX="14" refY="6" orient="auto" markerUnits="userSpaceOnUse">
    <path d="M1,1 L14,6 L1,11 Z" fill="{BG}" stroke="{GREEN}" stroke-width="1.4"/>
  </marker>
</defs>
<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>
<text x="{w/2}" y="42" font-size="24" font-weight="700" fill="{GREEN}" text-anchor="middle">{esc(title)}</text>
<text x="{w/2}" y="64" font-size="12.5" fill="{MUTED}" text-anchor="middle">Ceres Diagnostico — Atividade de Extensao II — IFMT Cuiaba</text>
'''


def box(x, y, w, h, fill, stroke, rx=8, sw=1.6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=13, fill=INK, anchor="start", weight="400", font=FONT, italic=False):
    st = ' font-style="italic"' if italic else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="{font}"{st}>{esc(s)}</text>'


def ellipse(cx, cy, rx, ry, fill, stroke, sw=1.6):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke=LINE, sw=1.4, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{marker})"' if marker else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>'


def actor(cx, cy, label):
    """Stick figure UML actor."""
    s = []
    s.append(f'<circle cx="{cx}" cy="{cy-26}" r="11" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'<line x1="{cx}" y1="{cy-15}" x2="{cx}" y2="{cy+12}" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'<line x1="{cx-16}" y1="{cy-4}" x2="{cx+16}" y2="{cy-4}" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'<line x1="{cx}" y1="{cy+12}" x2="{cx-14}" y2="{cy+34}" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'<line x1="{cx}" y1="{cy+12}" x2="{cx+14}" y2="{cy+34}" stroke="{GREEN}" stroke-width="2"/>')
    for i, ln in enumerate(label.split("\n")):
        s.append(txt(cx, cy+52+i*15, ln, size=12.5, fill=GREEN, anchor="middle", weight="700"))
    return "\n".join(s)


# ============================================================
# 1. DIAGRAMA DE CASOS DE USO
# ============================================================
def casos_de_uso():
    W, H = 1160, 860
    s = [header(W, H, "Diagrama de Casos de Uso")]
    # system boundary
    bx, by, bw, bh = 330, 96, 500, 720
    s.append(box(bx, by, bw, bh, "none", GREEN, rx=14, sw=2))
    s.append(txt(bx+bw/2, by+26, "Sistema Ceres Diagnostico", size=15, fill=GREEN, anchor="middle", weight="700"))

    # use cases (cx, cy, label, ry)
    ucs = [
        ("UC1", 580, 170, "Autenticar-se\n(login / cadastro)"),
        ("UC2", 580, 250, "Diagnosticar folha\npor foto"),
        ("UC3", 580, 330, "Classificar imagem\ncom IA (TFLite)"),
        ("UC4", 580, 410, "Alternar modo\nCloud / Offline"),
        ("UC5", 580, 490, "Sincronizar\ndiagnosticos offline"),
        ("UC6", 580, 570, "Consultar\nhistorico IoT"),
        ("UC7", 580, 650, "Visualizar mapa\nde ocorrencias"),
        ("UC8", 580, 730, "Consultar\nenciclopedia"),
        ("UC9", 780, 610, "Registrar leitura\nde sensores"),
        ("UC10", 780, 730, "Gerenciar perfil\n/ exportar CSV"),
    ]
    pos = {}
    for uid, cx, cy, label in ucs:
        pos[uid] = (cx, cy)
        s.append(ellipse(cx, cy, 92, 34, PAPER, CARD, sw=1.6))
        for i, ln in enumerate(label.split("\n")):
            off = -6 + i*15 if len(label.split("\n")) > 1 else 5
            s.append(txt(cx, cy+off, ln, size=12, fill=INK, anchor="middle", weight="600"))

    # actor Produtor (left)
    s.append(actor(140, 300, "Produtor\nRural"))
    # actor ESP32 (right, secondary)
    s.append(actor(1010, 610, "ESP32-S3\n(IoT)"))
    # actor Modelo IA (right)
    s.append(actor(1010, 330, "Servico IA\n(TFLite)"))

    # associations Produtor -> UCs
    for uid in ["UC1", "UC2", "UC4", "UC5", "UC6", "UC7", "UC8"]:
        cx, cy = pos[uid]
        s.append(line(168, 300, cx-92, cy, stroke=LINE, sw=1.3))
    s.append(line(168, 300, pos["UC10"][0]-92, pos["UC10"][1], stroke=LINE, sw=1.3))
    # ESP32 -> UC9
    s.append(line(982, 610, pos["UC9"][0]+92, pos["UC9"][1], stroke=BLUE, sw=1.4))
    # Servico IA -> UC3
    s.append(line(982, 330, pos["UC3"][0]+92, pos["UC3"][1], stroke=BLUE, sw=1.4))
    # UC9 feeds UC6 (leitura -> historico) include
    s.append(line(pos["UC9"][0], pos["UC9"][1]-34, pos["UC6"][0]+70, pos["UC6"][1]+18, stroke=GREEN, sw=1.2, dash="5,4", marker="arrowOpen"))

    # include: UC2 -> UC3
    s.append(line(pos["UC2"][0], pos["UC2"][1]+34, pos["UC3"][0], pos["UC3"][1]-34, stroke=GREEN, sw=1.2, dash="5,4", marker="arrowOpen"))
    s.append(txt(pos["UC2"][0]+8, (pos["UC2"][1]+pos["UC3"][1])/2, "<<include>>", size=10.5, fill=GREEN, anchor="start", italic=True))
    # extend: UC4 -> UC2
    s.append(line(pos["UC4"][0], pos["UC4"][1]-34, pos["UC2"][0], pos["UC2"][1]+34, stroke=GOLD, sw=1.2, dash="5,4", marker="arrowOpen"))
    s.append(txt(pos["UC4"][0]-150, (pos["UC4"][1]+pos["UC2"][1])/2+40, "<<extend>>", size=10.5, fill=GOLD, anchor="start", italic=True))

    # legend
    ly = H-30
    s.append(txt(bx, ly, "—— associacao      - - -> <<include>> / <<extend>>", size=11, fill=MUTED))
    s.append("</svg>")
    open(os.path.join(OUT, "casos_de_uso.svg"), "w", encoding="utf-8").write("\n".join(s))
    print("casos_de_uso.svg")


# ============================================================
# 4. ARQUITETURA DO SISTEMA
# ============================================================
def arquitetura():
    W, H = 1200, 900
    s = [header(W, H, "Arquitetura do Sistema")]

    def node(x, y, w, h, title, lines, fill=PAPER, stroke=CARD, tcol=GREEN):
        out = [box(x, y, w, h, fill, stroke, rx=10, sw=1.8)]
        out.append(txt(x+14, y+26, title, size=14, fill=tcol, anchor="start", weight="700"))
        for i, ln in enumerate(lines):
            out.append(txt(x+14, y+48+i*17, ln, size=11.5, fill=INK, anchor="start"))
        return "\n".join(out)

    # Camada de Borda (IoT)
    s.append(txt(60, 100, "CAMADA DE BORDA (IoT)", size=12, fill=GOLD, weight="700"))
    s.append(node(60, 112, 300, 150, "ESP32-S3-WROOM-1",
                  ["• Sensor DHT22 (temp / umid. ar)",
                   "• Sensor capacitivo (umid. solo)",
                   "• TFLite Micro — MobileNetV2 INT8",
                   "• Latencia ~692 ms | Arena 200 KB",
                   "• Firmware PlatformIO (C++)"], fill=BLUEBG, stroke=BLUE, tcol=BLUE))

    # Broker
    s.append(txt(60, 320, "MENSAGERIA", size=12, fill=GOLD, weight="700"))
    s.append(node(60, 332, 300, 92, "HiveMQ Cloud (Broker MQTT)",
                  ["• MQTT/TLS porta 8883",
                   "• WebSocket/TLS porta 8884",
                   "• Topico: ceres/sensor/#"], fill=PAPER, stroke=CARD))

    # Nuvem Railway
    s.append(txt(470, 100, "CAMADA DE NUVEM (Railway)", size=12, fill=GOLD, weight="700"))
    s.append(box(470, 112, 360, 340, "#FFFFFF", GREEN, rx=12, sw=2))
    s.append(txt(490, 138, "Backend — Django REST Framework", size=13, fill=GREEN, weight="700"))
    s.append(node(490, 150, 320, 96, "API REST (JWT / SimpleJWT)",
                  ["• /api/diagnostico/inferir/  (foto)",
                   "• /api/diagnostico/historico/",
                   "• /api/auth/  (login, registro, me)"], fill=PAPER, stroke=CARD))
    s.append(node(490, 258, 320, 74, "mqtt_listener (management cmd)",
                  ["• Assina ceres/sensor/# (WS+TLS)",
                   "• Persiste DiagnosticoEvento"], fill=PAPER, stroke=CARD))
    s.append(node(490, 344, 320, 92, "Servico de Inferencia (TFLite)",
                  ["• ceres_expe_int8.tflite (638 KB)",
                   "• Temperature scaling T=0.25",
                   "• PIL LANCZOS 96x96"], fill=PAPER, stroke=CARD))

    # Banco
    s.append(node(470, 500, 360, 92, "PostgreSQL (Railway)",
                  ["• Tenant / CustomUser",
                   "• Diagnostico / Pergunta / Opcao",
                   "• DiagnosticoEvento (persistente)"], fill="#EFE7D6", stroke=GOLD, tcol=GREEN))

    # App Flutter
    s.append(txt(920, 100, "CAMADA DE APLICACAO", size=12, fill=GOLD, weight="700"))
    s.append(node(920, 112, 240, 300, "App Flutter (Android)",
                  ["• 5 telas: Diagnostico,",
                   "  Mapa, IoT, Enciclopedia,",
                   "  Perfil",
                   "• TFLite on-device (~60 ms)",
                   "• Drift (SQLite offline)",
                   "• Sync offline -> online",
                   "• GPS (geolocator)",
                   "• flutter_map / OSM"], fill=PAPER, stroke=CARD))

    # Pipeline de treino
    s.append(txt(920, 500, "PIPELINE DE TREINO (offline)", size=12, fill=GOLD, weight="700"))
    s.append(node(920, 512, 240, 148, "WSL2 + RTX 3060 Ti",
                  ["• TensorFlow / Keras",
                   "• MobileNetV2 0.35 · 96x96 · INT8",
                   "• Export INT8 calibrado (rep. dataset)",
                   "• Exp B (2 fases) -> ESP32 · 639 KB",
                   "• Exp E (Focal Loss) -> App/API · 638 KB"], fill=BLUEBG, stroke=BLUE, tcol=BLUE))

    # connections
    def conn(x1, y1, x2, y2, label, col=GREEN, dash=None):
        out = [line(x1, y1, x2, y2, stroke=col, sw=1.8, marker="arrow", dash=dash)]
        mx, my = (x1+x2)/2, (y1+y2)/2
        out.append(f'<rect x="{mx-70}" y="{my-12}" width="140" height="18" rx="4" fill="{BG}" opacity="0.9"/>')
        out.append(txt(mx, my+1, label, size=10.5, fill=col, anchor="middle", weight="600"))
        return "\n".join(out)

    # ESP32 -> broker
    s.append(conn(210, 262, 210, 332, "MQTT / TLS 8883", col=BLUE))
    # broker -> mqtt_listener
    s.append(conn(360, 300, 490, 290, "WebSocket / TLS 8884", col=GREEN))
    # api <-> postgres
    s.append(conn(620, 436, 620, 500, "Django ORM", col=GREEN))
    s.append(conn(720, 500, 720, 340, "leitura/escrita", col=GREEN))
    # app <-> api
    s.append(conn(920, 240, 810, 200, "HTTPS REST / JWT", col=GREEN))

    # ── Distribuicao do modelo treinado (dashed, roteado pela margem externa) ──
    def rpath(pts, r=12):
        import math
        d = f"M{pts[0][0]},{pts[0][1]}"
        for i in range(1, len(pts)-1):
            x0, y0 = pts[i-1]; x1, y1 = pts[i]; x2, y2 = pts[i+1]
            def u(ax, ay, bx, by):
                dx, dy = bx-ax, by-ay; L = math.hypot(dx, dy) or 1; return dx/L, dy/L
            ux1, uy1 = u(x0, y0, x1, y1); ux2, uy2 = u(x1, y1, x2, y2)
            d += f" L{x1-ux1*r:.1f},{y1-uy1*r:.1f} Q{x1},{y1} {x1+ux2*r:.1f},{y1+uy2*r:.1f}"
        d += f" L{pts[-1][0]},{pts[-1][1]}"
        return d

    # Exp B (MobileNetV2 639KB) -> embarcado no firmware do ESP32 (barramento base/esquerda)
    s.append(f'<path d="{rpath([(1040,660),(1040,792),(34,792),(34,187),(60,187)])}" '
             f'fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="7,5" marker-end="url(#arrow)"/>')
    s.append(f'<rect x="330" y="783" width="420" height="19" rx="4" fill="{BG}"/>')
    s.append(txt(540, 797, "Exp B — MobileNetV2 INT8 · 639 KB embarcado no firmware do ESP32", size=11, fill=BLUE, anchor="middle", italic=True))
    # Exp E (638KB) -> embarcado no App / servico de inferencia
    s.append(f'<path d="{rpath([(1040,512),(1040,412)])}" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="7,5" marker-end="url(#arrow)"/>')
    s.append(txt(1052, 466, "Exp E · 638 KB no App", size=11, fill=BLUE, anchor="start", italic=True))

    s.append("</svg>")
    open(os.path.join(OUT, "arquitetura.svg"), "w", encoding="utf-8").write("\n".join(s))
    print("arquitetura.svg")


# ============================================================
# 2. DIAGRAMA DE CLASSES (models Django)
# ============================================================
def uml_class(x, y, w, name, attrs, methods, stereo=None):
    lh = 17
    head_h = 30 + (16 if stereo else 0)
    ah = len(attrs) * lh + 10
    mh = len(methods) * lh + 10
    h = head_h + ah + mh
    s = [box(x, y, w, h, PAPER, GREEN, rx=6, sw=1.8)]
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{head_h}" rx="6" fill="{CARD}"/>')
    s.append(f'<rect x="{x}" y="{y+head_h-6}" width="{w}" height="6" fill="{CARD}"/>')
    yy = y + 20
    if stereo:
        s.append(txt(x+w/2, yy, stereo, size=10.5, fill="#D8E8D0", anchor="middle", italic=True))
        yy += 16
    s.append(txt(x+w/2, yy, name, size=13.5, fill="#FFFFFF", anchor="middle", weight="700"))
    # attrs
    ya = y + head_h
    s.append(line(x, ya, x+w, ya, stroke=GREEN, sw=1.2))
    for i, a in enumerate(attrs):
        s.append(txt(x+10, ya+18+i*lh, a, size=11, fill=INK, font=MONO))
    # methods
    ym = ya + ah
    s.append(line(x, ym, x+w, ym, stroke=GREEN, sw=1.2))
    for i, m in enumerate(methods):
        s.append(txt(x+10, ym+18+i*lh, m, size=11, fill=MUTED, font=MONO))
    return "\n".join(s), h


def diagrama_classes():
    W, H = 1260, 940
    s = [header(W, H, "Diagrama de Classes")]
    boxes = {}

    def add(key, x, y, w, name, attrs, methods, stereo=None):
        svg, h = uml_class(x, y, w, name, attrs, methods, stereo)
        s.append(svg)
        boxes[key] = (x, y, w, h)

    # Cluster contas (esquerda) | Eventos (centro) | Arvore de decisao (direita)
    add("tenant", 70, 120, 260, "Tenant",
        ["+ id: AutoField (PK)", "+ nome: CharField(255)", "+ criado_em: DateTime"],
        ["+ __str__(): str"])
    add("user", 70, 360, 300, "CustomUser",
        ["+ id: AutoField (PK)", "+ username: CharField", "+ email: EmailField",
         "+ password: CharField", "+ tenant: FK(Tenant)"],
        ["+ __str__(): str"], stereo="extends AbstractUser")

    add("evt", 470, 300, 300, "DiagnosticoEvento",
        ["+ id: AutoField (PK)", "+ device_id: CharField(50)",
         "+ classe_detectada: CharField", "+ confianca: FloatField",
         "+ temperatura: FloatField", "+ umidade_ar: FloatField",
         "+ umidade_solo: FloatField", "+ latitude: FloatField",
         "+ longitude: FloatField", "+ timestamp: DateTime",
         "+ usuario: FK(CustomUser)", "+ diagnostico: FK(Diagnostico)",
         "+ criado_em: DateTime"],
        ["+ __str__(): str"])

    add("diag", 880, 110, 320, "Diagnostico",
        ["+ id: AutoField (PK)", "+ nome: CharField(200)", "+ descricao: TextField",
         "+ recomendacao_manejo: TextField", "+ criado_em: DateTime"],
        ["+ __str__(): str"])
    add("perg", 890, 440, 300, "Pergunta",
        ["+ id: AutoField (PK)", "+ texto: CharField(255)"],
        ["+ __str__(): str"])
    add("opc", 865, 660, 340, "Opcao",
        ["+ id: AutoField (PK)", "+ texto: CharField(200)",
         "+ pergunta_origem: FK(Pergunta)", "+ proxima_pergunta: FK(Pergunta)",
         "+ diagnostico_final: FK(Diagnostico)"],
        ["+ __str__(): str"])

    def anchor(key, side):
        x, y, w, h = boxes[key]
        return {"right": (x+w, y+h/2), "left": (x, y+h/2),
                "top": (x+w/2, y), "bottom": (x+w/2, y+h)}[side]

    def assoc(a, sa, b, sb, mult_a, mult_b, label, lx=None, ly=None):
        x1, y1 = anchor(a, sa); x2, y2 = anchor(b, sb)
        out = [line(x1, y1, x2, y2, stroke=GREEN, sw=1.5)]
        mx = lx if lx is not None else (x1+x2)/2
        my = ly if ly is not None else (y1+y2)/2 - 8
        out.append(txt(mx, my, label, size=11, fill=GOLD, anchor="middle", weight="600"))
        out.append(txt(x1+(9 if sa == "right" else (-9 if sa == "left" else 8)), y1-6, mult_a,
                       size=10.5, fill=MUTED, anchor="start" if sa != "left" else "end"))
        out.append(txt(x2+(-9 if sb == "left" else (9 if sb == "right" else 8)), y2-6, mult_b,
                       size=10.5, fill=MUTED, anchor="end" if sb == "left" else "start"))
        return "\n".join(out)

    def ortho(pts, stroke=CARD, dash="5,4"):
        d = " ".join(f"{'M' if i==0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
        return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.4" stroke-dasharray="{dash}" marker-end="url(#arrow)"/>'

    # associacoes limpas
    s.append(assoc("tenant", "bottom", "user", "top", "1", "0..*", "tenant", lx=230, ly=248))
    s.append(assoc("user", "right", "evt", "left", "0..1", "0..*", "usuario", ly=372))
    s.append(assoc("evt", "right", "diag", "left", "0..*", "0..1", "diagnostico", ly=250))
    s.append(assoc("perg", "bottom", "opc", "top", "1", "0..*", "pergunta_origem", lx=1035, ly=615))

    # auto-referencias (FK opcionais) — roteadas por fora, sem cruzar caixas
    xo, yo, wo, ho = boxes["opc"]
    xp, yp, wp, hp = boxes["perg"]
    xd, yd, wd, hd = boxes["diag"]
    # Opcao.proxima_pergunta -> Pergunta (elbow pela esquerda)
    s.append(ortho([(xo, yo+50), (xo-35, yo+50), (xo-35, yp+hp/2), (xp, yp+hp/2)]))
    s.append(txt(xo-40, yo+40, "proxima_pergunta", size=10, fill=MUTED, anchor="end"))
    # Opcao.diagnostico_final -> Diagnostico (elbow pela direita)
    s.append(ortho([(xo+wo, yo+80), (W-30, yo+80), (W-30, yd+hd/2), (xd+wd, yd+hd/2)]))
    s.append(txt(W-34, yo+70, "diagnostico_final", size=10, fill=MUTED, anchor="end"))

    s.append(txt(70, H-24, "Notacao UML — associacoes com multiplicidade; - - -> ForeignKey opcional (SET_NULL)", size=11, fill=MUTED))
    s.append("</svg>")
    open(os.path.join(OUT, "diagrama_classes.svg"), "w", encoding="utf-8").write("\n".join(s))
    print("diagrama_classes.svg")


# ============================================================
# 3. MER — Modelo Entidade-Relacionamento
# ============================================================
def mer():
    W, H = 1260, 900
    s = [header(W, H, "Modelo Entidade-Relacionamento (MER)")]
    boxes = {}

    def table(key, x, y, w, name, cols):
        lh = 18
        head_h = 28
        h = head_h + len(cols) * lh + 8
        s.append(box(x, y, w, h, PAPER, GREEN, rx=4, sw=1.8))
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{head_h}" rx="4" fill="{GREEN}"/>')
        s.append(f'<rect x="{x}" y="{y+head_h-4}" width="{w}" height="4" fill="{GREEN}"/>')
        s.append(txt(x+w/2, y+19, name, size=12.5, fill="#FFFFFF", anchor="middle", weight="700", font=MONO))
        for i, (key_type, col) in enumerate(cols):
            yy = y+head_h+16+i*lh
            if key_type:
                badge = {"PK": GOLD, "FK": BLUE, "PF": "#8A5A00"}.get(key_type, MUTED)
                s.append(f'<rect x="{x+8}" y="{yy-12}" width="26" height="15" rx="3" fill="{badge}"/>')
                s.append(txt(x+21, yy-1, key_type, size=9, fill="#FFFFFF", anchor="middle", weight="700", font=MONO))
            s.append(txt(x+42, yy, col, size=11, fill=INK, font=MONO))
        boxes[key] = (x, y, w, h)

    # Cluster contas (esq) | Evento (centro) | Arvore de decisao (dir)
    table("tenant", 70, 110, 260, "accounts_tenant",
          [("PK", "id  bigint"), ("", "nome  varchar(255)"), ("", "criado_em  timestamp")])
    table("user", 70, 340, 280, "accounts_customuser",
          [("PK", "id  bigint"), ("", "username  varchar"), ("", "email  varchar"),
           ("", "password  varchar"), ("FK", "tenant_id  bigint")])

    table("evt", 470, 250, 300, "diagnostico_diagnosticoevento",
          [("PK", "id  bigint"), ("", "device_id  varchar(50)"),
           ("", "classe_detectada  varchar"), ("", "confianca  double"),
           ("", "temperatura  double"), ("", "umidade_ar  double"),
           ("", "umidade_solo  double"), ("", "latitude  double"),
           ("", "longitude  double"), ("", "timestamp  timestamp"),
           ("FK", "usuario_id  bigint"), ("FK", "diagnostico_id  bigint"),
           ("", "criado_em  timestamp")])

    table("diag", 880, 110, 310, "diagnostico_diagnostico",
          [("PK", "id  bigint"), ("", "nome  varchar(200)"), ("", "descricao  text"),
           ("", "recomendacao_manejo  text"), ("", "criado_em  timestamp")])
    table("perg", 890, 450, 290, "diagnostico_pergunta",
          [("PK", "id  bigint"), ("", "texto  varchar(255)")])
    table("opc", 865, 640, 320, "diagnostico_opcao",
          [("PK", "id  bigint"), ("", "texto  varchar(200)"),
           ("FK", "pergunta_origem_id"), ("FK", "proxima_pergunta_id"),
           ("FK", "diagnostico_final_id")])

    def anc(key, side):
        x, y, w, h = boxes[key]
        return {"right": (x+w, y+h/2), "left": (x, y+h/2),
                "top": (x+w/2, y), "bottom": (x+w/2, y+h)}[side]

    def rel(a, sa, b, sb, one="1", many="N"):
        x1, y1 = anc(a, sa); x2, y2 = anc(b, sb)
        out = [line(x1, y1, x2, y2, stroke=BLUE, sw=1.6)]
        out.append(txt(x1+(10 if sa == "right" else -10), y1-6, one, size=12, fill=GREEN,
                       anchor="start" if sa == "right" else "end", weight="700"))
        out.append(txt(x2+(-10 if sb == "left" else 10), y2+(16 if sb == "top" else -6), many,
                       size=12, fill=GREEN, anchor="end" if sb == "left" else "start", weight="700"))
        return "\n".join(out)

    def ortho(pts):
        d = " ".join(f"{'M' if i==0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
        return f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5,4"/>'

    s.append(rel("tenant", "bottom", "user", "top"))
    s.append(rel("user", "right", "evt", "left"))
    s.append(rel("evt", "right", "diag", "left"))
    s.append(rel("perg", "bottom", "opc", "top"))
    # FKs auto-referentes da opcao — roteadas por fora
    xo, yo, wo, ho = boxes["opc"]
    xp, yp, wp, hp = boxes["perg"]
    xd, yd, wd, hd = boxes["diag"]
    s.append(ortho([(xo, yo+56), (xo-32, yo+56), (xo-32, yp+hp/2), (xp, yp+hp/2)]))
    s.append(ortho([(xo+wo, yo+74), (W-28, yo+74), (W-28, yd+hd/2), (xd+wd, yd+hd/2)]))

    # legenda
    ly = H-40
    s.append(f'<rect x="70" y="{ly-12}" width="26" height="15" rx="3" fill="{GOLD}"/>')
    s.append(txt(83, ly-1, "PK", size=9, fill="#FFFFFF", anchor="middle", weight="700", font=MONO))
    s.append(txt(104, ly, "Chave primaria", size=11, fill=MUTED))
    s.append(f'<rect x="230" y="{ly-12}" width="26" height="15" rx="3" fill="{BLUE}"/>')
    s.append(txt(243, ly-1, "FK", size=9, fill="#FFFFFF", anchor="middle", weight="700", font=MONO))
    s.append(txt(264, ly, "Chave estrangeira      1 —— N : relacionamento um-para-muitos", size=11, fill=MUTED))
    s.append("</svg>")
    open(os.path.join(OUT, "mer.svg"), "w", encoding="utf-8").write("\n".join(s))
    print("mer.svg")


# ============================================================
# 5. ROADMAP — Linha do tempo das sprints
# ============================================================
def roadmap():
    W, H = 1520, 740
    s = [header(W, H, "Roadmap do Produto — Linha do Tempo")]

    sprints = [
        ("SPRINT 1", "Núcleo Inteligente", "Backend + IA", "18 tarefas", CARD,
         ["Motor de diagnóstico + API", "JWT · Multi-tenant · PostgreSQL",
          "Dataset PlantVillage (88.949)", "Modelo IA — Exp A→E (638 KB)",
          "Backend MQTT + validação campo"]),
        ("SPRINT 2", "Borda Embarcada", "Firmware + IoT", "8 tarefas", "#3B6B3B",
         ["Firmware ESP32-S3 (PlatformIO)", "WiFi + MQTT + DHT22 / solo",
          "TFLite Micro embarcado", "Benchmark 692 ms · 10/10", "Pilha IoT ponta a ponta"]),
        ("SPRINT 3", "Aplicativo e Integração", "App + UX + Deploy", "29 tarefas", "#4A7A4A",
         ["App Flutter — 5 telas", "Design System + on-device 60ms",
          "Deploy Railway + MQTT Cloud", "Mapa GPS · Perfil · Guia",
          "Sync offline + robustez"]),
    ]

    ty = 150
    cw, g = 350, 34
    cards_x = [70, 70+cw+g, 70+2*(cw+g)]      # 70, 454, 838  → card3 termina em 1188
    last_mx = cards_x[2] + cw/2               # 1013
    ffx = 1360                                 # centro do bloco Fase Futura

    # trilho
    s.append(f'<line x1="70" y1="{ty}" x2="{last_mx}" y2="{ty}" stroke="{LINE}" stroke-width="3"/>')
    s.append(f'<line x1="{last_mx}" y1="{ty}" x2="{ffx+15}" y2="{ty}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="9,6" marker-end="url(#arrow)"/>')

    for i, (tag, titulo, camada, ntar, cor, itens) in enumerate(sprints):
        cx = cards_x[i]
        mx = cx + cw/2
        s.append(f'<circle cx="{mx}" cy="{ty}" r="13" fill="{cor}" stroke="{BG}" stroke-width="3"/>')
        s.append(txt(mx, ty+5, str(i+1), size=13, fill="#FFFFFF", anchor="middle", weight="700"))
        s.append(txt(mx, ty-26, "≈ 1 mês", size=12, fill=GOLD, anchor="middle", weight="700"))
        cardy = ty + 45
        s.append(f'<line x1="{mx}" y1="{ty+13}" x2="{mx}" y2="{cardy}" stroke="{LINE}" stroke-width="1.5"/>')
        cardh = 428
        s.append(box(cx, cardy, cw, cardh, PAPER, cor, rx=12, sw=2))
        s.append(f'<rect x="{cx}" y="{cardy}" width="{cw}" height="54" rx="12" fill="{cor}"/>')
        s.append(f'<rect x="{cx}" y="{cardy+42}" width="{cw}" height="12" fill="{cor}"/>')
        s.append(txt(cx+18, cardy+23, tag, size=12, fill="#D8E8D0", anchor="start", weight="700"))
        s.append(txt(cx+18, cardy+44, titulo, size=15, fill="#FFFFFF", anchor="start", weight="700"))
        s.append(txt(cx+18, cardy+80, camada, size=11, fill=cor, anchor="start", weight="700"))
        s.append(txt(cx+cw-18, cardy+80, ntar, size=11, fill=GOLD, anchor="end", weight="700"))
        s.append(line(cx+18, cardy+92, cx+cw-18, cardy+92, stroke="#D8D0C0", sw=1))
        for j, it in enumerate(itens):
            yy = cardy + 124 + j*52
            s.append(f'<circle cx="{cx+26}" cy="{yy-4}" r="3.5" fill="{cor}"/>')
            s.append(txt(cx+40, yy, it, size=11.5, fill=INK, anchor="start"))
        s.append(f'<rect x="{cx}" y="{cardy+cardh-30}" width="{cw}" height="30" fill="{GREEN}"/>')
        s.append(f'<rect x="{cx}" y="{cardy+cardh-30}" width="{cw}" height="12" fill="{GREEN}"/>')
        s.append(txt(cx+cw/2, cardy+cardh-10, "✔ CONCLUÍDA", size=11, fill="#FFFFFF", anchor="middle", weight="700"))

    # Fase Futura (à direita, sem sobrepor)
    s.append(txt(ffx, ty-26, "Fase Futura", size=11.5, fill=GOLD, anchor="middle", weight="700", italic=True))
    s.append(f'<circle cx="{ffx}" cy="{ty}" r="11" fill="{BG}" stroke="{GOLD}" stroke-width="3"/>')
    cardy = ty + 45
    s.append(f'<line x1="{ffx}" y1="{ty+11}" x2="{ffx}" y2="{cardy}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="4,3"/>')
    bw = 260
    s.append(box(ffx-bw/2, cardy, bw, 210, "#FBF3E2", GOLD, rx=12, sw=1.8))
    s.append(txt(ffx, cardy+30, "PRÓXIMOS PASSOS", size=11, fill=GOLD, anchor="middle", weight="700"))
    s.append(line(ffx-bw/2+18, cardy+44, ffx+bw/2-18, cardy+44, stroke="#E0CFA8", sw=1))
    itens_ff = ["Câmera OV5640 no ESP32-S3", "(diagnóstico autônomo)", "",
                "EfficientNet-B0 no", "Raspberry Pi 3B+"]
    for j, it in enumerate(itens_ff):
        s.append(txt(ffx, cardy+72+j*24, it, size=11, fill=INK, anchor="middle"))

    s.append(txt(W/2, H-22, "Metodologia: Scrum adaptado · 3 sprints de ~1 mês · versionamento no GitHub (github.com/Namem/extensao2)",
                size=11, fill=MUTED, anchor="middle"))
    s.append("</svg>")
    open(os.path.join(OUT, "roadmap.svg"), "w", encoding="utf-8").write("\n".join(s))
    print("roadmap.svg")


if __name__ == "__main__":
    casos_de_uso()
    arquitetura()
    diagrama_classes()
    mer()
    roadmap()
