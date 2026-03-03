"""
Neutropaenic Sepsis Management — Interactive Decision Support
ADHB Antimicrobial Stewardship
Built from FN_Flow_chart.pptx (exact layout reproduced)
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neutropaenic Sepsis Management",
    page_icon="🧬",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════════════════════
# COLOURS  — matched to PPTX fills
# ══════════════════════════════════════════════════════════════════════════════
C = {
    "purple":  "#C488C4",   # header / recurrent fever
    "blue":    "#85C1E9",   # review72
    "lpurple": "#EDCAED",   # resolved fever / persistent fever headers
    "yellow":  "#FFFAAA",   # decision / action nodes
    "green":   "#AAEEA4",   # stop/continue/target/cease
    "white":   "#FFFFFF",   # most decision nodes
    "ol":      "#5D6D7E",
    "act":     "#C0392B",
    "df":      "#F2F3F4",
    "ds":      "#C8CDD0",
    "dt":      "#C8CDD0",
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def _wrap(text, box_w, fs):
    cw  = fs * 0.56
    mc  = max(1, int((box_w - 14) / cw))
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= mc: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [text]

def node(x, y, w, h, fill, label="", fs=10, bold=False,
         bullets=None, active=False, dimmed=False, dashed=False):
    if dimmed:
        fill, stroke, tc, sw = C["df"], C["ds"], C["dt"], 1
    elif active:
        stroke, tc, sw = C["act"], "#111", 3
    else:
        stroke, tc, sw = C["ol"], "#111", 1.5
    dash = ' stroke-dasharray="5,3"' if dashed else ""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>\n'
    lh = fs + 3.5
    fw = "bold" if bold else "normal"
    if bullets:
        tot = len(bullets) * lh
        ty0 = y + max(fs, (h - tot) / 2 + fs)
        for i, b in enumerate(bullets):
            s += f'<text x="{x+9}" y="{ty0+i*lh}" font-size="{fs}" fill="{tc}" font-family="Arial,sans-serif">• {esc(b)}</text>\n'
    elif label:
        lines = _wrap(label, w, fs)
        tot   = len(lines) * lh
        ty0   = y + (h - tot) / 2 + fs
        for i, ln in enumerate(lines):
            s += f'<text x="{x+w/2}" y="{ty0+i*lh}" font-size="{fs}" font-weight="{fw}" fill="{tc}" font-family="Arial,sans-serif" text-anchor="middle">{esc(ln)}</text>\n'
    return s

def arrow(x1, y1, x2, y2, act=False, dim=False):
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}" marker-end="url(#arr_{"a" if act else "n"})"/>\n'

def seg(x1, y1, x2, y2, act=False, dim=False):
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}"/>\n'

def poly(pts_list, act=False, dim=False):
    """Polyline with arrowhead at final segment end."""
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    pts = " ".join(f"{x},{y}" for x,y in pts_list)
    return f'<polyline points="{pts}" fill="none" stroke="{clr}" stroke-width="{sw}" marker-end="url(#arr_{"a" if act else "n"})"/>\n'

def bus_drop(bus_y, drops, active_set=(), dim_set=()):
    """
    Horizontal bus at bus_y connecting leftmost to rightmost drop,
    then vertical arrows down to each (cx, top_y).
    drops = list of (cx, top_y, node_id)
    """
    xs = [d[0] for d in drops]
    any_act = bool(active_set)
    any_dim = not any_act and len(dim_set) == len(drops)
    s  = seg(min(xs), bus_y, max(xs), bus_y, act=any_act, dim=any_dim)
    for i, (cx, ty, nid) in enumerate(drops):
        a = nid in active_set
        d = nid in dim_set
        s += arrow(cx, bus_y, cx, ty, act=a, dim=d)
    return s

# ══════════════════════════════════════════════════════════════════════════════
# PATHWAY LOGIC  (matches PPTX exactly)
# ══════════════════════════════════════════════════════════════════════════════

def determine_pathway(fever_resolved, neutro_resolved, stable,
                      enterocolitis, allo_sct, micro_defined):
    AN = {"header", "review72"}

    if fever_resolved:
        AN.add("resolved_fever")
        if micro_defined:
            # Centre path: micro-defined
            AN.add("micro_defined")
            AN.add("liaise_id")
            if neutro_resolved:
                AN.add("r_neutro_resolved")
                AN.add("target_abx")
            else:
                AN.add("r_neutro_ongoing")
                if enterocolitis:
                    AN.add("r_entero_yes")
                    AN.add("continue_r")
                else:
                    AN.add("r_entero_no")
                    AN.add("target_abx")
        else:
            # Left path: fever of unknown origin
            AN.add("fever_unknown")
            if neutro_resolved:
                AN.add("l_neutro_resolved")
                AN.add("stop_abx")
            else:
                AN.add("l_neutro_ongoing")
                if enterocolitis:
                    AN.add("l_entero_yes")
                    AN.add("continue_l")
                else:
                    AN.add("l_entero_no")
                    if allo_sct:
                        AN.add("allo_sct")
                        AN.add("cease_allo")
                    else:
                        AN.add("non_allo")
                        AN.add("cease_non_allo")
    else:
        # Right path: persistent fever
        AN.add("persistent_fever")
        AN.add("recurrent_fever")
        AN.add("recurrent_box")
        if stable:
            AN.add("p_stable")
            AN.add("continue_stable")
        else:
            AN.add("p_unstable")
            AN.add("imaging_box")

    return AN

# ══════════════════════════════════════════════════════════════════════════════
# SVG LAYOUT
#
# Derived directly from PPTX shape positions (scale: 34px/cm, +10px left pad)
# Slide dimensions: ~35cm wide × ~20cm tall → 1200px × 700px
#
# COLUMN CENTRES (px):
#   CA  =  75   Stop abx / l_neutro_resolved
#   CB  = 173   Continue empiric L / l_entero_yes / l_neutro_ongoing (left)
#   CC  = 262   Allo-SCT / l_entero_no  (actually col C in PPTX)
#   CD  = 381   Non-allo-SCT
#   CE  = 432   r_neutro_ongoing / r_entero_yes / continue_r
#   CF  = 540   Micro-defined / Liaise ID / r_entero_no
#   CG  = 642   r_neutro_resolved / target_abx / recurrent_fever
#   CH  = 806   p_stable / continue_stable
#   CI  = 938   p_unstable / imaging_box
#
# NODE WIDTH = 95px for narrow cols, 165px for span nodes
# ROW Y TOPS (px):
#   R0  =  10   header
#   R1  =  55   review72
#   R2  =  90   resolved_fever / persistent_fever
#   R3  = 155   fever_unknown / micro_defined / p_stable / p_unstable
#   R4  = 210   liaise_id
#   R5  = 255   neutro status row
#   R6  = 305   imaging_box (right side, tall)
#   R7  = 330   enterocolitis row
#   R8  = 440   actions row (stop/continue_l/allo/non_allo/continue_r/target)
#   R9  = 496   recurrent_fever
#   R10 = 520   cease_allo / cease_non_allo
#   R11 = 556   recurrent_box
#   legend = 650
# ══════════════════════════════════════════════════════════════════════════════

# Node geometry: (x, y, w, h)
# All widths designed so same-column nodes are identical width and aligned
NW  = 100   # standard narrow node width
MW  = 140   # medium width
BW  = 165   # bullet/tall node width

def build_svg(AN):
    def a(n): return n in AN
    def d(n): return len(AN) > 2 and n not in AN

    W, H = 1230, 700

    # ── Column centre-x values ────────────────────────────────────────────
    # Spaced so same-row nodes NEVER overlap (verified: min gap = 10px)
    # Left section (resolved fever path):
    CA = 65    # stop_abx / l_neutro_resolved          edges: 15–115
    CB = 195   # continue_l / l_entero_yes              edges: 125–265
    CC = 325   # allo_sct / l_entero_no / l_neutro_ong  edges: 275–375
    CD = 435   # non_allo                                edges: 385–485
    # Middle section (micro-defined path):
    CE = 565   # continue_r / r_entero_yes / r_neutro_ong  edges: 495–635
    CF = 695   # r_entero_no                             edges: 645–745
    CG = 805   # target_abx / r_neutro_resolved          edges: 755–855
    # Right section (persistent fever):
    CH = 960   # p_stable / continue_stable              edges: 875–1045
    CI = 1115  # p_unstable / imaging_box                edges: 1020–1210

    # ── Node geometry: (x, y, w, h) ──────────────────────────────────────
    # Helper: centre a node of width w on column c
    def cx(c, w): return c - w//2

    G = {}

    # ── Node geometry — all positions derived from column centres above ──
    # cx(C, w) = C - w//2  gives the left edge for a node of width w centred on C

    # R0-R1: spanning nodes
    G["header"]           = (390, 10, 450, 36)
    G["review72"]         = (320, 56, 590, 28)

    # R2: branch headers
    # resolved_fever spans from CA-left (15) to CG-right (855)
    G["resolved_fever"]   = (15,  94, 840, 42)
    # persistent_fever spans CH-left to CI-right
    G["persistent_fever"] = (875, 94, 340, 42)

    # R3: second-level nodes
    # fever_unknown: under left half of resolved_fever — spans CA to CC area
    G["fever_unknown"]    = (15,  152, 400, 34)
    # micro_defined: under right half — spans CE to CG area, dashed
    G["micro_defined"]    = (495, 148, 360, 42)
    # p_stable: left column of right section
    G["p_stable"]         = (875, 152, 165, 34)
    # p_unstable: right column of right section (taller for bullets)
    G["p_unstable"]       = (1050, 146, 175, 58)

    # R4: Liaise with ID centred on mid-point of micro_defined
    G["liaise_id"]        = (530, 202, 290, 30)   # dashed

    # R5: neutropenia status — 4 nodes
    G["l_neutro_resolved"] = (cx(CA, NW), 252, NW, 32)   # 15–115
    G["l_neutro_ongoing"]  = (cx(CC, NW), 252, NW, 32)   # 275–375
    G["r_neutro_ongoing"]  = (cx(CE, NW), 252, NW, 32)   # 495–595  (was CE but CE=565, so 515-615)
    G["r_neutro_resolved"] = (cx(CG, NW), 252, NW, 32)   # 755–855

    # Right section R5 level
    G["continue_stable"]  = (875, 252, 165, 32)
    G["imaging_box"]      = (1050, 252, 175, 100)

    # R7: enterocolitis — 4 nodes (taller to fit 2-line text)
    G["l_entero_yes"]     = (cx(CB, NW), 306, NW, 58)    # 145–245
    G["l_entero_no"]      = (cx(CC, NW), 306, NW, 58)    # 275–375
    G["r_entero_yes"]     = (cx(CE, NW), 306, NW, 58)    # 515–615
    G["r_entero_no"]      = (cx(CF, NW), 306, NW, 58)    # 645–745

    # R8: actions row — 6 mutually-exclusive-path nodes
    G["stop_abx"]         = (cx(CA, NW), 390, NW, 32)    # 15–115
    G["continue_l"]       = (cx(CB, MW), 386, MW, 40)    # 125–265
    G["allo_sct"]         = (cx(CC, NW), 390, NW, 32)    # 275–375
    G["non_allo"]         = (cx(CD, NW), 390, NW, 32)    # 385–485
    G["continue_r"]       = (cx(CE, MW), 386, MW, 40)    # 495–635
    G["target_abx"]       = (cx(CG, NW), 390, NW, 32)    # 755–855

    # R10: cease nodes — sit under allo/non-allo columns, guaranteed no overlap
    G["cease_allo"]       = (cx(CC, MW), 444, MW, 56)     # 255–395
    G["cease_non_allo"]   = (405, 444, MW, 40)             # 405–545

    # Recurrent fever — sits under right section
    G["recurrent_fever"]  = (875, 444, 345, 32)

    # Recurrent actions box — spans full right section width
    G["recurrent_box"]    = (875, 490, 345, 80)

    # ── Helpers ──────────────────────────────────────────────────────────
    def gx(n):   return G[n][0]
    def gy(n):   return G[n][1]
    def gw(n):   return G[n][2]
    def gh(n):   return G[n][3]
    def gcx(n):  return G[n][0] + G[n][2]//2
    def gcy(n):  return G[n][1] + G[n][3]//2
    def gtop(n): return G[n][1]
    def gbot(n): return G[n][1] + G[n][3]
    def grgt(n): return G[n][0] + G[n][2]

    # ── SVG open ──────────────────────────────────────────────────────────
    svg = (f'<svg id="flowSVG" xmlns="http://www.w3.org/2000/svg" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'style="background:#fff;font-family:Arial,sans-serif">\n')
    svg += f'''<defs>
  <marker id="arr_n" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C["ol"]}"/>
  </marker>
  <marker id="arr_a" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C["act"]}"/>
  </marker>
</defs>\n'''

    # ── NODES ─────────────────────────────────────────────────────────────
    def N(nid, fill, label="", fs=10, bold=False, bullets=None, dashed=False):
        x,y,w,h = G[nid]
        return node(x,y,w,h, fill, label=label, fs=fs, bold=bold,
                    bullets=bullets, dashed=dashed, active=a(nid), dimmed=d(nid))

    # Headers
    svg += N("header",   C["purple"], "Neutropaenic Sepsis Management", fs=13, bold=True)
    svg += N("review72", C["blue"],   "Review at 72 hours empiric antibiotics", fs=10)

    # R2 branch headers
    svg += N("resolved_fever",   C["lpurple"],
             "Resolved fever: Afebrile >48 hours & clinically stable", fs=10)
    svg += N("persistent_fever", C["lpurple"],
             "Persistent fever or remains clinically unstable", fs=10)

    # R3
    svg += N("fever_unknown",  C["white"],  "Fever of unknown origin",                      fs=9)
    svg += N("micro_defined",  C["white"],  "Microbiologically or clinically defined infection", fs=9, dashed=True)
    svg += N("p_stable",       C["white"],  "Clinically stable:\nContinue empiric therapy", fs=9)
    svg += node(*G["p_unstable"], C["yellow"], fs=9, bold=True,
                bullets=["Clinically unstable:",
                         "Consider aminoglycoside",
                         "Liaise with ID about MRO coverage",
                         "Repeat peripheral and central cultures"],
                active=a("p_unstable"), dimmed=d("p_unstable"))

    # R5 neutro
    svg += N("l_neutro_resolved", C["white"], "Resolved neutropaenia", fs=9)
    svg += N("l_neutro_ongoing",  C["white"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_ongoing",  C["white"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_resolved", C["white"], "Resolved neutropaenia", fs=9)
    svg += N("continue_stable",   C["yellow"], "Continue empiric therapy", fs=9)

    # R4 liaise_id (drawn after neutro so it's above them visually in SVG order)
    svg += N("liaise_id", C["white"], "Liaise with ID", fs=9, dashed=True)

    # Imaging box — right side, beside p_stable/p_unstable rows
    svg += node(*G["imaging_box"], C["white"], fs=9,
                bullets=["Liaise with ID",
                         "Consider CT chest ± abdo/pelvis/sinus",
                         "MRI brain if CNS signs/symptoms",
                         "Consider non-infective causes"],
                active=a("imaging_box"), dimmed=d("imaging_box"))

    # R7 enterocolitis
    svg += N("l_entero_yes", C["white"], "Has enterocolitis or significant mucositis", fs=9)
    svg += N("l_entero_no",  C["white"], "No enterocolitis or significant mucositis",  fs=9)
    svg += N("r_entero_yes", C["white"], "Has enterocolitis or significant mucositis", fs=9)
    svg += N("r_entero_no",  C["white"], "No enterocolitis or significant mucositis",  fs=9)

    # R8 actions
    svg += N("stop_abx",   C["green"],  "Stop antibiotics",              fs=9, bold=True)
    svg += N("continue_l", C["yellow"], "Continue empiric antibiotics",  fs=9, bold=True)
    svg += N("allo_sct",   C["white"],  "Allo-SCT patient",              fs=9)
    svg += N("non_allo",   C["white"],  "Non-allo-SCT patient",          fs=9)
    svg += N("continue_r", C["yellow"], "Continue empiric antibiotics",  fs=9, bold=True)
    svg += N("target_abx", C["green"],  "Target antibiotics",            fs=9, bold=True)

    # R10 cease
    svg += node(*G["cease_allo"], C["green"],
                label="Consider ceasing empiric antibiotics if another cause found", fs=9,
                active=a("cease_allo"), dimmed=d("cease_allo"))
    svg += node(*G["cease_non_allo"], C["green"],
                label="Consider ceasing empiric antibiotics", fs=9,
                active=a("cease_non_allo"), dimmed=d("cease_non_allo"))

    # Recurrent
    svg += N("recurrent_fever", C["purple"],  "Recurrent fever", fs=10, bold=True)
    svg += node(*G["recurrent_box"], C["yellow"], fs=9,
                bullets=["Clinically unstable:",
                         "Restart empiric antibiotics and consider aminoglycoside",
                         "Liaise with ID about MRO coverage",
                         "Repeat peripheral and central cultures"],
                active=a("recurrent_box"), dimmed=d("recurrent_box"))

    # ── ARROWS ─────────────────────────────────────────────────────────────
    # header → review72
    svg += arrow(gcx("header"), gbot("header"), gcx("review72"), gtop("review72"),
                 act=a("header"), dim=False)

    # review72 → resolved_fever and persistent_fever via bus at y=82
    bus1 = 82
    svg += seg(gcx("review72"), gbot("review72"), gcx("review72"), bus1, act=a("review72"))
    svg += seg(gcx("resolved_fever"), bus1, gcx("persistent_fever"), bus1)
    for nid in ("resolved_fever", "persistent_fever"):
        svg += arrow(gcx(nid), bus1, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # resolved_fever → fever_unknown AND micro_defined via bus at y=140
    bus2 = 140
    svg += seg(gcx("resolved_fever"), gbot("resolved_fever"), gcx("resolved_fever"), bus2,
               act=a("resolved_fever"), dim=d("resolved_fever"))
    svg += seg(gcx("fever_unknown"), bus2, gcx("micro_defined"), bus2)
    for nid in ("fever_unknown", "micro_defined"):
        svg += arrow(gcx(nid), bus2, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # persistent_fever → p_stable / p_unstable via bus at y=140
    svg += seg(gcx("persistent_fever"), gbot("persistent_fever"), gcx("persistent_fever"), bus2,
               act=a("persistent_fever"), dim=d("persistent_fever"))
    svg += seg(gcx("p_stable"), bus2, gcx("p_unstable"), bus2)
    for nid in ("p_stable", "p_unstable"):
        svg += arrow(gcx(nid), bus2, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # p_stable → continue_stable (straight down, same column)
    svg += arrow(gcx("p_stable"), gbot("p_stable"), gcx("continue_stable"), gtop("continue_stable"),
                 act=a("p_stable"), dim=d("p_stable") or d("continue_stable"))

    # p_unstable → imaging_box (straight down, same column)
    svg += arrow(gcx("p_unstable"), gbot("p_unstable"), gcx("imaging_box"), gtop("imaging_box"),
                 act=a("p_unstable"), dim=d("p_unstable") or d("imaging_box"))

    # persistent_fever → recurrent_fever (straight down from centre of right section)
    svg += arrow(gcx("persistent_fever"), gbot("persistent_fever"),
                 gcx("recurrent_fever"), gtop("recurrent_fever"),
                 act=a("persistent_fever"), dim=d("persistent_fever") or d("recurrent_fever"))

    # recurrent_fever → recurrent_box
    svg += arrow(gcx("recurrent_fever"), gbot("recurrent_fever"),
                 gcx("recurrent_box"), gtop("recurrent_box"),
                 act=a("recurrent_fever"), dim=d("recurrent_fever") or d("recurrent_box"))

    # micro_defined → liaise_id
    svg += arrow(gcx("micro_defined"), gbot("micro_defined"), gcx("liaise_id"), gtop("liaise_id"),
                 act=a("micro_defined"), dim=d("micro_defined") or d("liaise_id"))

    # fever_unknown → l_neutro split via bus at y=240
    bus3 = 240
    svg += seg(gcx("fever_unknown"), gbot("fever_unknown"), gcx("fever_unknown"), bus3,
               act=a("fever_unknown"), dim=d("fever_unknown"))
    svg += seg(gcx("l_neutro_resolved"), bus3, gcx("l_neutro_ongoing"), bus3)
    for nid in ("l_neutro_resolved", "l_neutro_ongoing"):
        svg += arrow(gcx(nid), bus3, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # liaise_id → r_neutro split via bus at y=240
    svg += seg(gcx("liaise_id"), gbot("liaise_id"), gcx("liaise_id"), bus3,
               act=a("liaise_id"), dim=d("liaise_id"))
    svg += seg(gcx("r_neutro_ongoing"), bus3, gcx("r_neutro_resolved"), bus3)
    for nid in ("r_neutro_ongoing", "r_neutro_resolved"):
        svg += arrow(gcx(nid), bus3, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_neutro_resolved → stop_abx (straight down, column CA)
    svg += arrow(gcx("l_neutro_resolved"), gbot("l_neutro_resolved"),
                 gcx("stop_abx"), gtop("stop_abx"),
                 act=a("l_neutro_resolved"), dim=d("l_neutro_resolved") or d("stop_abx"))

    # l_neutro_ongoing → entero split via bus at y=294
    bus4 = 294
    svg += seg(gcx("l_neutro_ongoing"), gbot("l_neutro_ongoing"), gcx("l_neutro_ongoing"), bus4,
               act=a("l_neutro_ongoing"), dim=d("l_neutro_ongoing"))
    svg += seg(gcx("l_entero_yes"), bus4, gcx("l_entero_no"), bus4)
    for nid in ("l_entero_yes", "l_entero_no"):
        svg += arrow(gcx(nid), bus4, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # r_neutro_ongoing → r_entero split via bus at y=294
    svg += seg(gcx("r_neutro_ongoing"), gbot("r_neutro_ongoing"), gcx("r_neutro_ongoing"), bus4,
               act=a("r_neutro_ongoing"), dim=d("r_neutro_ongoing"))
    svg += seg(gcx("r_entero_yes"), bus4, gcx("r_entero_no"), bus4)
    for nid in ("r_entero_yes", "r_entero_no"):
        svg += arrow(gcx(nid), bus4, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_entero_yes → continue_l (straight down)
    svg += arrow(gcx("l_entero_yes"), gbot("l_entero_yes"),
                 gcx("continue_l"), gtop("continue_l"),
                 act=a("l_entero_yes"), dim=d("l_entero_yes") or d("continue_l"))

    # l_entero_no → allo/non_allo split via bus at y=378
    bus5 = 378
    svg += seg(gcx("l_entero_no"), gbot("l_entero_no"), gcx("l_entero_no"), bus5,
               act=a("l_entero_no"), dim=d("l_entero_no"))
    svg += seg(gcx("allo_sct"), bus5, gcx("non_allo"), bus5)
    for nid in ("allo_sct", "non_allo"):
        svg += arrow(gcx(nid), bus5, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # allo_sct → cease_allo
    svg += arrow(gcx("allo_sct"), gbot("allo_sct"), gcx("cease_allo"), gtop("cease_allo"),
                 act=a("allo_sct"), dim=d("allo_sct") or d("cease_allo"))

    # non_allo → cease_non_allo
    svg += arrow(gcx("non_allo"), gbot("non_allo"), gcx("cease_non_allo"), gtop("cease_non_allo"),
                 act=a("non_allo"), dim=d("non_allo") or d("cease_non_allo"))

    # r_entero_yes → continue_r (straight down)
    svg += arrow(gcx("r_entero_yes"), gbot("r_entero_yes"),
                 gcx("continue_r"), gtop("continue_r"),
                 act=a("r_entero_yes"), dim=d("r_entero_yes") or d("continue_r"))

    # r_entero_no → target_abx (elbow: down, across right to CG, down)
    bus6 = gbot("r_entero_no") + 20
    svg += poly([(gcx("r_entero_no"),  gbot("r_entero_no")),
                 (gcx("r_entero_no"),  bus6),
                 (gcx("target_abx"),   bus6),
                 (gcx("target_abx"),   gtop("target_abx"))],
                act=a("r_entero_no"), dim=d("r_entero_no") or d("target_abx"))

    # r_neutro_resolved → target_abx (elbow: down to entero bus, across, down)
    svg += poly([(gcx("r_neutro_resolved"), gbot("r_neutro_resolved")),
                 (gcx("r_neutro_resolved"), bus4),
                 (gcx("target_abx"),        bus4),
                 (gcx("target_abx"),        gtop("target_abx"))],
                act=a("r_neutro_resolved"), dim=d("r_neutro_resolved") or d("target_abx"))


    # ── LEGEND ────────────────────────────────────────────────────────────
    ly = 630
    for lx, lc, lt in [
        (10,   C["green"],   "Action / recommendation"),
        (200,  C["yellow"],  "Clinical decision point"),
        (390,  C["lpurple"], "Pathway header"),
        (570,  C["purple"],  "Header / Recurrent fever"),
        (750,  C["white"],   "Decision node"),
        (900,  "#fff",       "▶  Active pathway"),
    ]:
        svg += node(lx, ly, 182, 24, lc, label=lt, fs=9)
    svg += f'<rect x="900" y="{ly}" width="182" height="24" rx="6" fill="none" stroke="{C["act"]}" stroke-width="2.5"/>\n'
    svg += f'<text x="912" y="{ly+16}" font-size="9" fill="{C["act"]}" font-family="Arial">▶  Active pathway highlighted</text>\n'

    svg += "</svg>\n"
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_recommendations(AN):
    recs = []
    if "stop_abx" in AN:
        recs.append(("✅", "Stop antibiotics",
                     "Neutropaenia and fever both resolved — antibiotics can be discontinued."))
    if any(x in AN for x in ("continue_l","continue_r","continue_stable")):
        recs.append(("💊", "Continue empiric antibiotics",
                     "Clinical situation warrants ongoing broad-spectrum cover."))
    if "p_stable" in AN and "continue_stable" in AN:
        recs.append(("💊", "Continue empiric therapy",
                     "Fever persisting but patient is clinically stable — continue current empiric regimen."))
    if "cease_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Allo-SCT)",
                     "Consider ceasing if another cause is found. Discuss with ID / haematology."))
    if "cease_non_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Non-allo-SCT)",
                     "Consider ceasing empiric antibiotics. Discuss with ID / treating team."))
    if "target_abx" in AN:
        recs.append(("🎯", "Target antibiotics",
                     "De-escalate to targeted therapy based on identified pathogen / source."))
    if "p_unstable" in AN:
        recs.append(("🚨", "Clinically unstable — escalate",
                     "Consider aminoglycoside. Liaise with ID re MRO coverage. "
                     "Repeat peripheral and central cultures."))
    if "imaging_box" in AN:
        recs.append(("🖥️", "Consider further investigation",
                     "Liaise with ID. Consider CT chest ± abdo/pelvis/sinus guided by symptoms. "
                     "MRI brain if CNS signs/symptoms. Consider non-infective causes."))
    if "recurrent_box" in AN:
        recs.append(("🔄", "Recurrent fever — clinically unstable",
                     "Restart empiric antibiotics and consider aminoglycoside. "
                     "Liaise with ID about MRO coverage. Repeat peripheral and central cultures."))
    return recs


# ══════════════════════════════════════════════════════════════════════════════
# COPY-TO-CLIPBOARD JS
# ══════════════════════════════════════════════════════════════════════════════

COPY_JS = """
<button onclick="copyChart()" style="
    background:#2471A3;color:#fff;border:none;border-radius:7px;
    padding:9px 20px;font-size:14px;cursor:pointer;
    font-family:Arial,sans-serif;display:inline-flex;
    align-items:center;gap:8px;margin-bottom:6px;">
  📋 Copy flowchart to clipboard
</button>
<div id="copyMsg" style="font-size:12px;font-family:Arial,sans-serif;min-height:18px;margin-top:3px;"></div>
<script>
async function copyChart() {
  const msg = document.getElementById('copyMsg');
  msg.style.color='#888'; msg.textContent='Rendering…';
  const svg = document.getElementById('flowSVG');
  if (!svg) { msg.textContent='⚠️ Chart not found.'; return; }
  const ser = new XMLSerializer().serializeToString(svg);
  const vb  = svg.viewBox.baseVal;
  const sc  = 2;
  const cv  = document.createElement('canvas');
  cv.width  = vb.width*sc; cv.height = vb.height*sc;
  const ctx = cv.getContext('2d');
  ctx.scale(sc,sc); ctx.fillStyle='#fff'; ctx.fillRect(0,0,vb.width,vb.height);
  const blob = new Blob([ser],{type:'image/svg+xml;charset=utf-8'});
  const url  = URL.createObjectURL(blob);
  const img  = new Image();
  img.onload = async () => {
    ctx.drawImage(img,0,0); URL.revokeObjectURL(url);
    cv.toBlob(async (pngBlob) => {
      if (navigator.clipboard && navigator.clipboard.write) {
        try {
          await navigator.clipboard.write([new ClipboardItem({'image/png':pngBlob})]);
          msg.style.color='#1a6e35'; msg.textContent='✅ Copied! Paste into eNotes with Ctrl+V / Cmd+V.';
          return;
        } catch(e){}
      }
      const a = document.createElement('a');
      a.href = cv.toDataURL('image/png'); a.download='neutropenic_sepsis_pathway.png'; a.click();
      msg.style.color='#c87722'; msg.textContent='📥 Saved as PNG — insert into eNotes manually.';
    },'image/png');
  };
  img.onerror = () => { msg.style.color='#c0392b'; msg.textContent='⚠️ Render failed.'; };
  img.src = url;
}
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════

st.title("🧬 Neutropaenic Sepsis Management")
st.caption("ADHB Antimicrobial Stewardship — Interactive Decision Support Tool")
st.markdown("---")

col_form, col_chart = st.columns([1, 3.2], gap="large")

with col_form:
    st.subheader("Patient Assessment")

    fever_resolved = st.radio(
        "**Fever status at 72-hour review**",
        ["Resolved (afebrile >48h, clinically stable)",
         "Persistent / recurrent fever"],
    ) == "Resolved (afebrile >48h, clinically stable)"

    neutro_resolved = st.radio(
        "**Neutropaenia status**",
        ["Resolved", "Ongoing"], index=1,
    ) == "Resolved"

    micro_defined = st.checkbox(
        "**Microbiologically or clinically defined infection**", value=False,
    )

    stable = st.radio(
        "**Clinical stability**",
        ["Clinically stable", "Clinically unstable"],
        disabled=(fever_resolved or micro_defined),
        help="Only relevant for persistent fever without a defined infection source",
    ) == "Clinically stable"

    enterocolitis = st.checkbox(
        "**Enterocolitis or significant mucositis**", value=False,
        disabled=(neutro_resolved and not micro_defined),
    )

    allo_sct = st.checkbox(
        "**Allo-SCT patient**", value=False,
        disabled=(enterocolitis or neutro_resolved),
        help="Relevant when ongoing neutropaenia, no enterocolitis, resolved fever",
    )

    st.markdown("---")
    st.caption(
        "ℹ️ All decisions should be made in clinical context. "
        "Consult Infectious Diseases as appropriate."
    )

with col_chart:
    AN = determine_pathway(
        fever_resolved  = fever_resolved,
        neutro_resolved = neutro_resolved,
        stable          = stable,
        enterocolitis   = enterocolitis,
        allo_sct        = allo_sct,
        micro_defined   = micro_defined,
    )

    svg_str = build_svg(AN)

    html = f"""<!DOCTYPE html>
<html><head><style>body{{margin:0;padding:4px;background:#fff}}</style></head>
<body>
{COPY_JS}
<div style="overflow-x:auto;margin-top:4px">{svg_str}</div>
</body></html>"""

    components.html(html, height=800, scrolling=True)

# ── Recommendations ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Recommended Actions")

recs = get_recommendations(AN)
if recs:
    for icon, title, detail in recs:
        st.markdown(f"**{icon} {title}**  \n{detail}")
else:
    st.info("Select patient parameters above to see tailored recommendations.")

st.markdown("---")
st.caption("Based on ADHB Neutropaenic Sepsis Management Guidelines. Not a substitute for clinical judgement.")
