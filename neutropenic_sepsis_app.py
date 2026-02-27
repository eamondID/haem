"""
Neutropaenic Sepsis Management — Interactive Decision Support
ADHB Antimicrobial Stewardship
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neutropaenic Sepsis Management",
    page_icon="🧬",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ══════════════════════════════════════════════════════════════════════════════
C = {
    "purple":        "#C39BD3",
    "blue":          "#85C1E9",
    "yellow":        "#F9E79F",
    "green":         "#A9DFBF",
    "pink":          "#F1948A",
    "white":         "#FFFFFF",
    "outline":       "#5D6D7E",
    "active_stroke": "#C0392B",
    "dim_fill":      "#F4F6F7",
    "dim_stroke":    "#CCD1D1",
    "dim_text":      "#CCD1D1",
}

# ══════════════════════════════════════════════════════════════════════════════
#  SVG PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def wrap_text(text: str, box_w: int, fs: int) -> list:
    char_w = fs * 0.56
    max_ch = max(1, int((box_w - 14) / char_w))
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if len(test) <= max_ch:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]

def box(x, y, w, h, fill, label="", fs=10, bold=False,
        bullets=None, active=False, dimmed=False, dashed=False):
    if dimmed:
        fill       = C["dim_fill"]
        stroke     = C["dim_stroke"]
        text_color = C["dim_text"]
        sw         = 1
    elif active:
        stroke     = C["active_stroke"]
        text_color = "#1A1A1A"
        sw         = 3
    else:
        stroke     = C["outline"]
        text_color = "#1A1A1A"
        sw         = 1.5

    dash = ' stroke-dasharray="6,3"' if dashed else ""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>\n')

    fw = "bold" if bold else "normal"
    lh = fs + 3

    if bullets:
        total = len(bullets) * lh
        ty0 = y + (h - total) / 2 + fs
        for i, bl in enumerate(bullets):
            s += (f'<text x="{x+10}" y="{ty0 + i*lh}" font-size="{fs}" '
                  f'fill="{text_color}" font-family="Arial,sans-serif">'
                  f'• {esc(bl)}</text>\n')
    elif label:
        lines = wrap_text(label, w, fs)
        total = len(lines) * lh
        ty0 = y + (h - total) / 2 + fs
        for i, ln in enumerate(lines):
            s += (f'<text x="{x + w/2}" y="{ty0 + i*lh}" font-size="{fs}" '
                  f'font-weight="{fw}" fill="{text_color}" '
                  f'font-family="Arial,sans-serif" text-anchor="middle">'
                  f'{esc(ln)}</text>\n')
    return s


def _line(x1, y1, x2, y2, active=False, dimmed=False):
    clr = C["active_stroke"] if active else (C["dim_stroke"] if dimmed else C["outline"])
    sw  = 2.5 if active else 1.2
    mk  = f'url(#arr_{"a" if active else "n"})'
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{clr}" stroke-width="{sw}" marker-end="{mk}"/>\n')


def _seg(x1, y1, x2, y2, active=False, dimmed=False):
    """Line segment with NO arrowhead (internal bus segment)."""
    clr = C["active_stroke"] if active else (C["dim_stroke"] if dimmed else C["outline"])
    sw  = 2.5 if active else 1.2
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{clr}" stroke-width="{sw}"/>\n')


def elbow(x1, y1, x2, y2, bend_y=None, bend_x=None, active=False, dimmed=False):
    """
    Elbow connector (L or Z shape).
    bend_y: go vertical to bend_y, then horizontal to x2, then vertical to y2.
    bend_x: go horizontal to bend_x, then vertical to y2, then horizontal to x2.
    """
    clr = C["active_stroke"] if active else (C["dim_stroke"] if dimmed else C["outline"])
    sw  = 2.5 if active else 1.2
    mk  = f'url(#arr_{"a" if active else "n"})'

    if bend_y is not None:
        pts = f"{x1},{y1} {x1},{bend_y} {x2},{bend_y} {x2},{y2}"
    elif bend_x is not None:
        pts = f"{x1},{y1} {bend_x},{y1} {bend_x},{y2} {x2},{y2}"
    else:
        mx = (x1 + x2) / 2
        pts = f"{x1},{y1} {mx},{y1} {mx},{y2} {x2},{y2}"

    return (f'<polyline points="{pts}" fill="none" stroke="{clr}" '
            f'stroke-width="{sw}" marker-end="{mk}"/>\n')


# ══════════════════════════════════════════════════════════════════════════════
#  PATHWAY LOGIC
# ══════════════════════════════════════════════════════════════════════════════

def determine_pathway(fever_resolved, neutro_resolved, stable,
                      enterocolitis, allo_sct, micro_defined):
    AN = {"header", "review72"}

    if fever_resolved:
        AN.add("resolved_fever")
        if micro_defined:
            AN.add("micro_defined")
            AN.add("liaise_id")
            if neutro_resolved:
                AN.add("r_neutro_resolved")
                AN.add("target_abx")
            else:
                AN.add("r_neutro_ongoing")
                if enterocolitis:
                    AN.add("r_entero_yes")
                    AN.add("continue_empiric_r")
                else:
                    AN.add("r_entero_no")
                    AN.add("target_abx")
        else:
            AN.add("fever_unknown")
            if neutro_resolved:
                AN.add("l_neutro_resolved")
                AN.add("stop_abx")
            else:
                AN.add("l_neutro_ongoing")
                if enterocolitis:
                    AN.add("l_entero_yes")
                    AN.add("continue_empiric_l")
                else:
                    AN.add("l_entero_no")
                    if allo_sct:
                        AN.add("allo_sct")
                        AN.add("cease_allo")
                    else:
                        AN.add("non_allo_sct")
                        AN.add("cease_non_allo")
    else:
        AN.add("persistent_fever")
        AN.add("recurrent_fever")
        AN.add("recurrent_actions")
        if stable:
            AN.add("p_stable")
            AN.add("continue_empiric_stable")
        else:
            AN.add("p_unstable")
            AN.add("unstable_actions")
            AN.add("imaging")

    return AN


# ══════════════════════════════════════════════════════════════════════════════
#  CLEAN GRID SVG LAYOUT
#
#  Canvas: 1020 × 790 px
#
#  Left half  (x 10–560):  Resolved fever pathway
#  Right half (x 580–1010): Persistent fever pathway
#
#  Row tops (Y coordinates):
#    R0   y=10    — main header (centred)
#    R1   y=58    — 72-hr review (centred)
#    R2   y=110   — resolved_fever | micro_defined | persistent_fever
#    R3   y=178   — fever_unknown  | liaise_id     | p_stable | p_unstable
#    R4   y=250   — neutro splits (both sides)
#    R5   y=318   — enterocolitis splits (both sides)
#    R6   y=388   — allo/non-allo | continue_empiric_r | continue_empiric_l
#    R7   y=456   — cease_allo | cease_non_allo | target_abx | stop_abx
#    R8   y=540   — recurrent_fever  (right half)
#    R9   y=600   — recurrent_actions
#    R10  y=700   — legend
# ══════════════════════════════════════════════════════════════════════════════

def build_svg(AN: set) -> str:

    def act(n): return n in AN
    def dim(n): return len(AN) > 2 and n not in AN

    W, H = 1020, 760

    svg = (f'<svg id="flowSVG" xmlns="http://www.w3.org/2000/svg" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'style="font-family:Arial,sans-serif;background:#fff">\n')

    svg += f"""<defs>
  <marker id="arr_n" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C['outline']}"/>
  </marker>
  <marker id="arr_a" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C['active_stroke']}"/>
  </marker>
</defs>\n"""

    # ── Helper: node geometry dict ─────────────────────────────────────────
    # Each entry: (x, y, w, h)
    G = {
        # ── Shared top ──────────────────────────────────────────────
        "header":       (360, 10,  300, 36),
        "review72":     (345, 58,  330, 30),

        # ── R2: three branch headers ─────────────────────────────────
        "resolved_fever":  (10,  112, 215, 44),
        "micro_defined":   (245, 112, 205, 44),   # dashed
        "persistent_fever":(730, 112, 280, 44),

        # ── R3 left: fever_unknown | liaise_id ──────────────────────
        "fever_unknown":   (10,  180, 190, 34),
        "liaise_id":       (230, 180, 195, 34),   # dashed

        # ── R3 right: stable / unstable ──────────────────────────────
        "p_stable":        (700, 180, 145, 34),
        "p_unstable":      (860, 174, 155, 60),

        # ── R4: neutro status ─────────────────────────────────────────
        "l_neutro_resolved": (10,  250, 130, 32),
        "l_neutro_ongoing":  (155, 250, 130, 32),
        "r_neutro_ongoing":  (230, 250, 130, 32),
        "r_neutro_resolved": (375, 250, 130, 32),

        # ── R5: enterocolitis ─────────────────────────────────────────
        "l_entero_yes":    (10,  318, 130, 34),
        "l_entero_no":     (155, 318, 130, 34),
        "r_entero_yes":    (225, 318, 135, 34),
        "r_entero_no":     (375, 318, 135, 34),

        # ── R6: allo/non-allo + continue empiric ─────────────────────
        "continue_empiric_l": (10,  388, 125, 32),
        "allo_sct":           (150, 388, 120, 32),
        "non_allo_sct":       (285, 388, 135, 32),
        "continue_empiric_r": (225, 388, 135, 32),   # overlaps geom-wise but used on right path only
        "continue_empiric_stable": (680, 248, 170, 34),
        "unstable_actions":   (845, 248, 165, 90),

        # ── R7: cease / stop / target ─────────────────────────────────
        "stop_abx":          (10,  388, 125, 32),   # same row as continue_l, exclusive paths
        "cease_allo":        (135, 456, 145, 52),
        "cease_non_allo":    (295, 456, 145, 52),
        "target_abx":        (390, 388, 140, 32),
        "imaging":           (845, 356, 165, 90),

        # ── R8/R9: recurrent ─────────────────────────────────────────
        "recurrent_fever":   (670, 480, 190, 34),
        "recurrent_actions": (650, 530, 230, 90),
    }

    # Geometry helpers
    def cx(n):  return G[n][0] + G[n][2] / 2
    def cy(n):  return G[n][1] + G[n][3] / 2
    def top(n): return G[n][1]
    def bot(n): return G[n][1] + G[n][3]
    def lft(n): return G[n][0]
    def rgt(n): return G[n][0] + G[n][2]

    # ── Draw helpers ──────────────────────────────────────────────────────
    def N(nid, fill, label="", fs=10, bold=False, bullets=None, dashed=False):
        x, y, w, h = G[nid]
        return box(x, y, w, h, fill, label=label, fs=fs, bold=bold,
                   bullets=bullets, dashed=dashed,
                   active=act(nid), dimmed=dim(nid))

    def AR(x1, y1, x2, y2, src, dst=None):
        a = act(src); d = dim(src) or (dst and dim(dst))
        return _line(x1, y1, x2, y2, active=a, dimmed=d)

    def EL(x1, y1, x2, y2, src, dst=None, by=None, bx=None):
        a = act(src); d = dim(src) or (dst and dim(dst))
        return elbow(x1, y1, x2, y2, bend_y=by, bend_x=bx, active=a, dimmed=d)

    def BUS_H(x1, x2, y, nodes):
        """Draw a horizontal bus line, then drop lines with arrows to each node."""
        s = ""
        any_act = any(act(n) for n in nodes)
        any_dim = all(dim(n) for n in nodes) and not any_act
        s += _seg(x1, y, x2, y, active=any_act, dimmed=any_dim)
        for n in nodes:
            s += _line(cx(n), y, cx(n), top(n), active=act(n), dimmed=dim(n))
        return s

    # ════════════════════════════════════════════════════════════════════════
    #  NODES
    # ════════════════════════════════════════════════════════════════════════

    # Headers
    svg += N("header",   C["purple"], "Neutropaenic Sepsis Management", fs=13, bold=True)
    svg += N("review72", C["blue"],   "Review at 72 hours empiric antibiotics", fs=10)

    # R2
    svg += N("resolved_fever",   C["yellow"],
             "Resolved fever: Afebrile ≥48h & clinically stable", fs=10)
    svg += N("micro_defined",    C["yellow"],
             "Microbiologically or clinically defined infection", fs=10, dashed=True)
    svg += N("persistent_fever", C["pink"],
             "Persistent fever or remains clinically unstable", fs=10)

    # R3 left
    svg += N("fever_unknown", C["yellow"], "Fever of unknown origin", fs=10)
    svg += N("liaise_id",     C["white"],  "Liaise with ID", fs=10, bold=True, dashed=True)

    # R3 right
    svg += N("p_stable",  C["yellow"], "Clinically stable", fs=10)
    svg += box(*G["p_unstable"], C["pink"], fs=9, bold=True,
               bullets=["Consider aminoglycoside",
                        "Liaise with ID re MRO",
                        "Repeat periph & central cultures"],
               active=act("p_unstable"), dimmed=dim("p_unstable"))

    # R4 neutro
    svg += N("l_neutro_resolved", C["yellow"], "Resolved neutropaenia", fs=9)
    svg += N("l_neutro_ongoing",  C["yellow"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_ongoing",  C["yellow"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_resolved", C["yellow"], "Resolved neutropaenia", fs=9)

    # R5 entero
    svg += N("l_entero_yes", C["yellow"], "Enterocolitis / mucositis",    fs=9)
    svg += N("l_entero_no",  C["yellow"], "No enterocolitis / mucositis", fs=9)
    svg += N("r_entero_yes", C["yellow"], "Enterocolitis / mucositis",    fs=9)
    svg += N("r_entero_no",  C["yellow"], "No enterocolitis / mucositis", fs=9)

    # R6 action nodes — left path
    svg += N("continue_empiric_l", C["green"], "Continue empiric antibiotics", fs=9, bold=True)
    svg += N("allo_sct",           C["yellow"], "Allo-SCT patient",            fs=9)
    svg += N("non_allo_sct",       C["yellow"], "Non-allo-SCT patient",        fs=9)
    # stop_abx shares row/x with continue_empiric_l (exclusive paths — only one drawn)
    svg += N("stop_abx",           C["green"],  "Stop antibiotics",            fs=10, bold=True)

    # R6 right path: continue empiric (placed at r_entero_yes column)
    svg += box(*G["continue_empiric_r"], C["green"],
               label="Continue empiric antibiotics", fs=9, bold=True,
               active=act("continue_empiric_r"), dimmed=dim("continue_empiric_r"))

    # R6 far right: continue empiric stable / unstable actions
    svg += N("continue_empiric_stable", C["green"], "Continue empiric therapy", fs=9, bold=True)
    svg += box(*G["unstable_actions"], C["pink"], fs=9,
               bullets=["Liaise with ID",
                        "CT chest ± abdo/pelvis/sinus",
                        "MRI brain if CNS signs",
                        "Consider non-infective causes"],
               active=act("unstable_actions"), dimmed=dim("unstable_actions"))

    # R7
    svg += box(*G["cease_allo"], C["yellow"],
               label="Consider ceasing empiric abx if another cause found", fs=9,
               active=act("cease_allo"), dimmed=dim("cease_allo"))
    svg += box(*G["cease_non_allo"], C["yellow"],
               label="Consider ceasing empiric antibiotics", fs=9,
               active=act("cease_non_allo"), dimmed=dim("cease_non_allo"))
    svg += N("target_abx", C["green"], "Target antibiotics", fs=10, bold=True)

    svg += box(*G["imaging"], C["yellow"], fs=9,
               bullets=["Liaise with ID",
                        "CT chest ± abdo/pelvis/sinus",
                        "MRI brain if CNS signs",
                        "Consider non-infective causes"],
               active=act("imaging"), dimmed=dim("imaging"))

    # Recurrent
    svg += N("recurrent_fever",   C["purple"], "Recurrent fever", fs=10, bold=True)
    svg += box(*G["recurrent_actions"], C["pink"], fs=9,
               bullets=["Restart empiric abx & consider aminoglycoside",
                        "Liaise with ID about MRO coverage",
                        "Repeat peripheral & central cultures"],
               active=act("recurrent_actions"), dimmed=dim("recurrent_actions"))

    # ════════════════════════════════════════════════════════════════════════
    #  ARROWS
    # ════════════════════════════════════════════════════════════════════════

    # header → review72
    svg += AR(cx("header"), bot("header"), cx("review72"), top("review72"), "header")

    # review72 → three branch headers via horizontal bus at y=100
    bus_y = 100
    svg += _seg(cx("review72"), bot("review72"), cx("review72"), bus_y,
                active=act("review72"), dimmed=dim("review72"))
    svg += BUS_H(cx("resolved_fever"), cx("persistent_fever"), bus_y,
                 ["resolved_fever", "micro_defined", "persistent_fever"])

    # resolved_fever → fever_unknown (straight down)
    svg += AR(cx("resolved_fever"), bot("resolved_fever"),
              cx("fever_unknown"), top("fever_unknown"), "resolved_fever")

    # micro_defined → liaise_id (straight down)
    svg += AR(cx("micro_defined"), bot("micro_defined"),
              cx("liaise_id"), top("liaise_id"), "micro_defined")

    # persistent_fever → p_stable / p_unstable via bus at y=168
    pb = 168
    svg += _seg(cx("persistent_fever"), bot("persistent_fever"),
                cx("persistent_fever"), pb, active=act("persistent_fever"), dimmed=dim("persistent_fever"))
    svg += BUS_H(cx("p_stable"), rgt("p_unstable"), pb, ["p_stable", "p_unstable"])

    # p_stable → continue_empiric_stable
    svg += AR(cx("p_stable"), bot("p_stable"),
              cx("continue_empiric_stable"), top("continue_empiric_stable"), "p_stable")

    # p_unstable → unstable_actions → imaging
    svg += AR(cx("p_unstable"), bot("p_unstable"),
              cx("unstable_actions"), top("unstable_actions"), "p_unstable")
    svg += AR(cx("unstable_actions"), bot("unstable_actions"),
              cx("imaging"), top("imaging"), "unstable_actions")

    # fever_unknown → l_neutro split via bus at y=238
    lb = 238
    svg += _seg(cx("fever_unknown"), bot("fever_unknown"),
                cx("fever_unknown"), lb, active=act("fever_unknown"), dimmed=dim("fever_unknown"))
    # bus from l_neutro_resolved to l_neutro_ongoing
    svg += BUS_H(cx("l_neutro_resolved"), cx("l_neutro_ongoing"), lb,
                 ["l_neutro_resolved", "l_neutro_ongoing"])

    # liaise_id → r_neutro split via bus at y=238
    svg += _seg(cx("liaise_id"), bot("liaise_id"),
                cx("liaise_id"), lb, active=act("liaise_id"), dimmed=dim("liaise_id"))
    svg += BUS_H(cx("r_neutro_ongoing"), cx("r_neutro_resolved"), lb,
                 ["r_neutro_ongoing", "r_neutro_resolved"])

    # l_neutro_resolved → stop_abx (straight down, same column)
    svg += AR(cx("l_neutro_resolved"), bot("l_neutro_resolved"),
              cx("stop_abx"), top("stop_abx"), "l_neutro_resolved", "stop_abx")

    # l_neutro_ongoing → l_entero split via bus at y=306
    le = 306
    svg += _seg(cx("l_neutro_ongoing"), bot("l_neutro_ongoing"),
                cx("l_neutro_ongoing"), le, active=act("l_neutro_ongoing"), dimmed=dim("l_neutro_ongoing"))
    svg += BUS_H(cx("l_entero_yes"), cx("l_entero_no"), le,
                 ["l_entero_yes", "l_entero_no"])

    # l_entero_yes → continue_empiric_l
    svg += AR(cx("l_entero_yes"), bot("l_entero_yes"),
              cx("continue_empiric_l"), top("continue_empiric_l"),
              "l_entero_yes", "continue_empiric_l")

    # l_entero_no → allo/non-allo via bus at y=375
    la = 375
    svg += _seg(cx("l_entero_no"), bot("l_entero_no"),
                cx("l_entero_no"), la, active=act("l_entero_no"), dimmed=dim("l_entero_no"))
    svg += BUS_H(cx("allo_sct"), cx("non_allo_sct"), la, ["allo_sct", "non_allo_sct"])

    # allo_sct → cease_allo
    svg += AR(cx("allo_sct"), bot("allo_sct"),
              cx("cease_allo"), top("cease_allo"), "allo_sct", "cease_allo")
    # non_allo_sct → cease_non_allo
    svg += AR(cx("non_allo_sct"), bot("non_allo_sct"),
              cx("cease_non_allo"), top("cease_non_allo"), "non_allo_sct", "cease_non_allo")

    # r_neutro_ongoing → r_entero split via bus at y=306
    re = 306
    svg += _seg(cx("r_neutro_ongoing"), bot("r_neutro_ongoing"),
                cx("r_neutro_ongoing"), re, active=act("r_neutro_ongoing"), dimmed=dim("r_neutro_ongoing"))
    svg += BUS_H(cx("r_entero_yes"), cx("r_entero_no"), re,
                 ["r_entero_yes", "r_entero_no"])

    # r_entero_yes → continue_empiric_r
    svg += AR(cx("r_entero_yes"), bot("r_entero_yes"),
              cx("continue_empiric_r"), top("continue_empiric_r"),
              "r_entero_yes", "continue_empiric_r")

    # r_entero_no → target_abx (elbow: right then down)
    svg += EL(cx("r_entero_no"), bot("r_entero_no"),
              cx("target_abx"), top("target_abx"),
              "r_entero_no", "target_abx", by=374)

    # r_neutro_resolved → target_abx (elbow: down to bus, across, down)
    svg += EL(cx("r_neutro_resolved"), bot("r_neutro_resolved"),
              cx("target_abx"), top("target_abx"),
              "r_neutro_resolved", "target_abx", by=374)

    # persistent_fever → recurrent_fever (elbow right then down)
    svg += EL(rgt("persistent_fever"), cy("persistent_fever"),
              cx("recurrent_fever"), top("recurrent_fever"),
              "persistent_fever", "recurrent_fever",
              bx=rgt("persistent_fever") + 8)

    # recurrent_fever → recurrent_actions
    svg += AR(cx("recurrent_fever"), bot("recurrent_fever"),
              cx("recurrent_actions"), top("recurrent_actions"),
              "recurrent_fever", "recurrent_actions")

    # ════════════════════════════════════════════════════════════════════════
    #  LEGEND
    # ════════════════════════════════════════════════════════════════════════
    ly = 700
    items = [
        (10,  C["green"],  "Action / recommendation"),
        (215, C["yellow"], "Clinical decision point"),
        (420, C["pink"],   "Urgent / unstable"),
        (600, C["purple"], "Pathway header"),
    ]
    for lx, lc, lt in items:
        svg += box(lx, ly, 195, 24, lc, label=lt, fs=9)

    # Active highlight example
    svg += box(810, ly, 200, 24, C["white"], label="  Active pathway highlighted", fs=9)
    svg += (f'<rect x="810" y="{ly}" width="200" height="24" rx="6" '
            f'fill="none" stroke="{C["active_stroke"]}" stroke-width="2.5"/>\n')
    svg += f'<text x="820" y="{ly+16}" font-size="9" fill="{C["active_stroke"]}" font-family="Arial">▶</text>\n'

    svg += "</svg>\n"
    return svg


# ══════════════════════════════════════════════════════════════════════════════
#  COPY-TO-CLIPBOARD  (SVG → canvas → PNG → clipboard, with download fallback)
# ══════════════════════════════════════════════════════════════════════════════

COPY_BLOCK = """
<button id="copyBtn" onclick="copyChart()" style="
    background:#2980B9; color:#fff; border:none; border-radius:6px;
    padding:10px 22px; font-size:15px; cursor:pointer;
    font-family:Arial,sans-serif; display:inline-flex;
    align-items:center; gap:8px; margin-bottom:6px;">
  <span>📋</span><span>Copy flowchart to clipboard</span>
</button>
<div id="copyMsg" style="font-size:13px;font-family:Arial,sans-serif;
     color:#27ae60;min-height:20px;margin-top:4px;"></div>

<script>
async function copyChart() {
  const msg = document.getElementById('copyMsg');
  msg.textContent = 'Rendering…';
  msg.style.color = '#888';

  const svg = document.getElementById('flowSVG');
  if (!svg) { msg.textContent = '⚠️ Chart SVG not found.'; return; }

  const serialised = new XMLSerializer().serializeToString(svg);
  const vb = svg.viewBox.baseVal;
  const scale = 2;
  const canvas = document.createElement('canvas');
  canvas.width  = vb.width  * scale;
  canvas.height = vb.height * scale;
  const ctx = canvas.getContext('2d');
  ctx.scale(scale, scale);
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, vb.width, vb.height);

  const blob = new Blob([serialised], {type:'image/svg+xml;charset=utf-8'});
  const url  = URL.createObjectURL(blob);
  const img  = new Image();

  img.onload = async () => {
    ctx.drawImage(img, 0, 0);
    URL.revokeObjectURL(url);

    canvas.toBlob(async (pngBlob) => {
      // Try modern clipboard API first
      if (navigator.clipboard && navigator.clipboard.write) {
        try {
          await navigator.clipboard.write([
            new ClipboardItem({'image/png': pngBlob})
          ]);
          msg.textContent = '✅ Copied! Paste directly into eNotes (Ctrl+V / Cmd+V).';
          msg.style.color = '#27ae60';
          return;
        } catch (e) { /* fall through to download */ }
      }
      // Fallback: download PNG
      const a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'neutropenic_sepsis_pathway.png';
      a.click();
      msg.textContent = '📥 Downloaded as PNG — insert the file into eNotes.';
      msg.style.color = '#e67e22';
    }, 'image/png');
  };

  img.onerror = () => {
    msg.textContent = '⚠️ SVG rendering failed. Try a different browser.';
    msg.style.color = '#e74c3c';
  };
  img.src = url;
}
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
#  RECOMMENDATION TEXT
# ══════════════════════════════════════════════════════════════════════════════

def get_recommendations(AN):
    recs = []
    if "stop_abx" in AN:
        recs.append(("✅", "Stop antibiotics",
                     "Neutropaenia resolved and fever resolved — antibiotics can be discontinued."))
    if any(x in AN for x in ("continue_empiric_l", "continue_empiric_r", "continue_empiric_stable")):
        recs.append(("💊", "Continue empiric antibiotics",
                     "Clinical situation warrants ongoing broad-spectrum cover."))
    if "cease_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Allo-SCT)",
                     "Cease if another cause found. Discuss with ID/haematology."))
    if "cease_non_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Non-allo-SCT)",
                     "Discuss with ID/treating team."))
    if "target_abx" in AN:
        recs.append(("🎯", "Target antibiotics",
                     "De-escalate to targeted therapy based on identified pathogen/source."))
    if "p_unstable" in AN or "unstable_actions" in AN:
        recs.append(("🚨", "Clinically unstable — escalate immediately",
                     "Consider aminoglycoside. Liaise with ID regarding MRO coverage. "
                     "Repeat peripheral and central cultures."))
    if "imaging" in AN:
        recs.append(("🖥️", "Consider imaging",
                     "CT chest ± abdo/pelvis/sinus guided by symptoms. "
                     "MRI brain if CNS signs/symptoms. Consider non-infective causes."))
    if "recurrent_actions" in AN:
        recs.append(("🔄", "Recurrent fever management",
                     "Restart empiric antibiotics and consider aminoglycoside. "
                     "Liaise with ID about MRO coverage. Repeat peripheral and central cultures."))
    return recs


# ══════════════════════════════════════════════════════════════════════════════
#  STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════

st.title("🧬 Neutropaenic Sepsis Management")
st.caption("ADHB Antimicrobial Stewardship — Interactive Decision Support Tool")
st.markdown("---")

col_form, col_chart = st.columns([1, 2.8], gap="large")

with col_form:
    st.subheader("Patient Assessment")

    fever_resolved = st.radio(
        "**Fever status at 72-hour review**",
        options=["Resolved (afebrile ≥48h, clinically stable)",
                 "Persistent / recurrent fever"],
        index=0
    ) == "Resolved (afebrile ≥48h, clinically stable)"

    neutro_resolved = st.radio(
        "**Neutropaenia status**",
        options=["Resolved", "Ongoing"],
        index=1
    ) == "Resolved"

    micro_defined = st.checkbox(
        "**Microbiologically or clinically defined infection identified**",
        value=False
    )

    stable_disabled = fever_resolved or micro_defined
    stable = st.radio(
        "**Clinical stability**",
        options=["Clinically stable", "Clinically unstable"],
        index=0,
        disabled=stable_disabled,
        help="Only applicable for persistent fever without a defined infection source"
    ) == "Clinically stable"

    entero_disabled = neutro_resolved and not micro_defined
    enterocolitis = st.checkbox(
        "**Enterocolitis or significant mucositis**",
        value=False,
        disabled=entero_disabled
    )

    allo_disabled = enterocolitis or neutro_resolved
    allo_sct = st.checkbox(
        "**Allo-SCT patient**",
        value=False,
        disabled=allo_disabled,
        help="Relevant when ongoing neutropaenia, no enterocolitis/mucositis, resolved fever"
    )

    st.markdown("---")
    st.caption(
        "ℹ️ All decisions should be made in clinical context and in consultation "
        "with Infectious Diseases as appropriate."
    )

with col_chart:
    # Determine active nodes
    AN = determine_pathway(
        fever_resolved=fever_resolved,
        neutro_resolved=neutro_resolved,
        stable=stable,
        enterocolitis=enterocolitis,
        allo_sct=allo_sct,
        micro_defined=micro_defined
    )

    svg_str = build_svg(AN)

    full_html = f"""<!DOCTYPE html>
<html><head>
<style>body{{margin:0;padding:4px;background:#fff;}}</style>
</head><body>
{COPY_BLOCK}
<div style="overflow-x:auto;margin-top:4px;">
{svg_str}
</div>
</body></html>"""

    components.html(full_html, height=870, scrolling=True)

# ── Recommendations ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Recommended Actions")

recs = get_recommendations(AN)
if recs:
    for icon, title, detail in recs:
        st.markdown(f"**{icon} {title}**  \n{detail}")
else:
    st.info("Select patient parameters to see tailored recommendations.")

st.markdown("---")
st.caption("Based on ADHB Neutropaenic Sepsis Management Guidelines. Not a substitute for clinical judgement.")
