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
# COLOURS
# ══════════════════════════════════════════════════════════════════════════════
C = {
    "purple":  "#C39BD3",
    "blue":    "#85C1E9",
    "yellow":  "#F9E79F",
    "green":   "#A9DFBF",
    "pink":    "#F1948A",
    "white":   "#FFFFFF",
    "ol":      "#5D6D7E",   # outline (normal)
    "act":     "#C0392B",   # active stroke
    "df":      "#F4F6F7",   # dim fill
    "ds":      "#CCD1D1",   # dim stroke
    "dt":      "#CCD1D1",   # dim text
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def _wrap(text, box_w, fs):
    cw = fs * 0.57
    mc = max(1, int((box_w - 16) / cw))
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= mc:
            cur = t
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
    dash = ' stroke-dasharray="6,3"' if dashed else ""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>\n'
    fw = "bold" if bold else "normal"
    lh = fs + 3.5
    if bullets:
        tot = len(bullets) * lh
        ty0 = y + (h - tot) / 2 + fs
        for i, b in enumerate(bullets):
            s += f'<text x="{x+9}" y="{ty0+i*lh}" font-size="{fs}" fill="{tc}" font-family="Arial,sans-serif">• {esc(b)}</text>\n'
    elif label:
        lines = _wrap(label, w, fs)
        tot = len(lines) * lh
        ty0 = y + (h - tot) / 2 + fs
        for i, ln in enumerate(lines):
            s += f'<text x="{x+w/2}" y="{ty0+i*lh}" font-size="{fs}" font-weight="{fw}" fill="{tc}" font-family="Arial,sans-serif" text-anchor="middle">{esc(ln)}</text>\n'
    return s

def arrow(x1, y1, x2, y2, act=False, dim=False):
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    mk  = f'url(#arr_{"a" if act else "n"})'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}" marker-end="{mk}"/>\n'

def seg(x1, y1, x2, y2, act=False, dim=False):
    """Line segment with no arrowhead."""
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}"/>\n'

def elbow(x1, y1, x2, y2, by=None, bx=None, act=False, dim=False):
    """Polyline elbow with arrowhead at end."""
    clr = C["act"] if act else (C["ds"] if dim else C["ol"])
    sw  = 2.5 if act else 1.3
    mk  = f'url(#arr_{"a" if act else "n"})'
    if by is not None:
        pts = f"{x1},{y1} {x1},{by} {x2},{by} {x2},{y2}"
    elif bx is not None:
        pts = f"{x1},{y1} {bx},{y1} {bx},{y2} {x2},{y2}"
    else:
        mx = (x1+x2)/2
        pts = f"{x1},{y1} {mx},{y1} {mx},{y2} {x2},{y2}"
    return f'<polyline points="{pts}" fill="none" stroke="{clr}" stroke-width="{sw}" marker-end="{mk}"/>\n'

def hbus(y, x_left, x_right, drops, act_set, dim_set):
    """
    Horizontal bus at y from x_left to x_right,
    then vertical drops with arrows to each (cx, top_y) in drops.
    act_set / dim_set: sets of indices into drops that are active/dimmed.
    """
    # pick bus line style from majority
    any_act = bool(act_set)
    any_dim = not any_act and len(dim_set) == len(drops)
    s = seg(x_left, y, x_right, y, act=any_act, dim=any_dim)
    for i, (cx, ty) in enumerate(drops):
        a = i in act_set
        d = i in dim_set
        s += arrow(cx, y, cx, ty, act=a, dim=d)
    return s

# ══════════════════════════════════════════════════════════════════════════════
# PATHWAY LOGIC
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
                    AN.add("continue_r")
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
        AN.add("persistent_fever")
        AN.add("recurrent_fever")
        AN.add("recurrent_actions")
        if stable:
            AN.add("p_stable")
            AN.add("continue_stable")
        else:
            AN.add("p_unstable")
            AN.add("unstable_box")
            AN.add("imaging_box")
    return AN

# ══════════════════════════════════════════════════════════════════════════════
# SVG BUILD
#
# 6 COLUMNS  (gap=10px between each):
#   C0  x=10   w=150   l_neutro_resolved, l_entero_yes, stop_abx / continue_l
#   C1  x=170  w=150   l_neutro_ongoing,  l_entero_no,  allo_sct,  cease_allo
#   C2  x=330  w=150   r_neutro_ongoing,  r_entero_yes, continue_r, cease_non_allo
#   C3  x=490  w=150   r_neutro_resolved, r_entero_no,  target_abx
#   C4  x=660  w=185   p_stable, continue_stable, recurrent_fever, recurrent_actions
#   C5  x=855  w=215   p_unstable, unstable_box, imaging_box
#
# Span nodes:
#   resolved_fever  spans C0-C1  x=10  w=310
#   micro_defined   spans C2-C3  x=330 w=310
#   persistent_fever spans C4-C5 x=660 w=410
#   fever_unknown   spans C0-C1  x=10  w=310
#   liaise_id       spans C2-C3  x=330 w=310
#   header / review72 span all   x=10  w=1060
#
# ROWS (top y, height):
#   R0  y=10   h=38   header
#   R1  y=60   h=30   review72
#   R2  y=106  h=46   resolved_fever | micro_defined | persistent_fever
#   R3  y=168  h=38   fever_unknown  | liaise_id     | p_stable | p_unstable
#   R4  y=224  h=34   neutro splits (C0-C3)          | continue_stable (C4) | unstable_box top
#   R5  y=276  h=34   entero splits  (C0-C3)
#   R6  y=328  h=34   stop/cont_l(C0) | allo(C1) | cont_r(C2) | target(C3)
#   R7  y=380  h=52   cease_allo(C1)  | cease_non_allo(C2)
#   R8  y=480  h=36   recurrent_fever (C4-C5)
#   R9  y=528  h=80   recurrent_actions (C4-C5)
#   unstable_box  y=224 h=90  (C5)
#   imaging_box   y=324 h=90  (C5)
#   legend y=650
# ══════════════════════════════════════════════════════════════════════════════

def build_svg(AN):
    def a(n): return n in AN
    def d(n): return len(AN) > 2 and n not in AN

    W, H = 1090, 700

    # ── geometry ──────────────────────────────────────────────────────────
    # columns: (x, w)
    COL = [
        (10,  150),   # C0
        (170, 150),   # C1
        (330, 150),   # C2
        (490, 150),   # C3
        (650, 185),   # C4
        (845, 215),   # C5
    ]
    def cx(c):   return COL[c][0] + COL[c][1] / 2   # col centre-x
    def cl(c):   return COL[c][0]                    # col left-x
    def cr(c):   return COL[c][0] + COL[c][1]        # col right-x
    def cw(c):   return COL[c][1]                    # col width
    def span_x(c0, c1): return COL[c0][0]
    def span_w(c0, c1): return COL[c1][0] + COL[c1][1] - COL[c0][0]
    def span_cx(c0,c1): return span_x(c0,c1) + span_w(c0,c1)/2

    # single node geometry by id
    G = {}
    # top spans
    G["header"]          = (span_x(0,5), 10,  span_w(0,5), 38)
    G["review72"]        = (span_x(0,5)+30, 60, span_w(0,5)-60, 30)
    # R2
    G["resolved_fever"]  = (span_x(0,1), 106, span_w(0,1), 46)
    G["micro_defined"]   = (span_x(2,3), 106, span_w(2,3), 46)
    G["persistent_fever"]= (span_x(4,5), 106, span_w(4,5), 46)
    # R3
    G["fever_unknown"]   = (span_x(0,1), 168, span_w(0,1), 38)
    G["liaise_id"]       = (span_x(2,3), 168, span_w(2,3), 38)
    G["p_stable"]        = (cl(4), 168, cw(4), 38)
    G["p_unstable"]      = (cl(5), 162, cw(5), 56)  # taller for bullets
    # R4 — neutro
    G["l_neutro_resolved"]= (cl(0), 224, cw(0), 34)
    G["l_neutro_ongoing"] = (cl(1), 224, cw(1), 34)
    G["r_neutro_ongoing"] = (cl(2), 224, cw(2), 34)
    G["r_neutro_resolved"]= (cl(3), 224, cw(3), 34)
    G["continue_stable"]  = (cl(4), 224, cw(4), 34)
    G["unstable_box"]     = (cl(5), 224, cw(5), 90)
    # R5 — entero
    G["l_entero_yes"]    = (cl(0), 278, cw(0), 34)
    G["l_entero_no"]     = (cl(1), 278, cw(1), 34)
    G["r_entero_yes"]    = (cl(2), 278, cw(2), 34)
    G["r_entero_no"]     = (cl(3), 278, cw(3), 34)
    G["imaging_box"]     = (cl(5), 324, cw(5), 90)
    # R6 — actions
    G["stop_abx"]        = (cl(0), 332, cw(0), 34)
    G["continue_l"]      = (cl(0), 332, cw(0), 34)   # exclusive with stop_abx
    G["allo_sct"]        = (cl(1), 332, cw(1), 34)
    G["non_allo"]        = (cl(1)+10, 332, cw(1)-10, 34)  # slight indent to not overlap allo
    G["continue_r"]      = (cl(2), 332, cw(2), 34)
    G["target_abx"]      = (cl(3), 332, cw(3), 34)
    # R7 — cease
    G["cease_allo"]      = (cl(1), 386, cw(1), 52)
    G["cease_non_allo"]  = (cl(2), 386, cw(2), 52)
    # Recurrent
    G["recurrent_fever"]   = (span_x(4,5), 478, span_w(4,5), 36)
    G["recurrent_actions"] = (span_x(4,5), 526, span_w(4,5), 82)

    def gx(n): return G[n][0]
    def gy(n): return G[n][1]
    def gw(n): return G[n][2]
    def gh(n): return G[n][3]
    def gcx(n): return G[n][0] + G[n][2]/2
    def gcy(n): return G[n][1] + G[n][3]/2
    def gtop(n): return G[n][1]
    def gbot(n): return G[n][1] + G[n][3]
    def glft(n): return G[n][0]
    def grgt(n): return G[n][0] + G[n][2]

    # ── SVG open ──────────────────────────────────────────────────────────
    svg = (f'<svg id="flowSVG" xmlns="http://www.w3.org/2000/svg" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'style="background:#fff;font-family:Arial,sans-serif">\n')

    svg += f"""<defs>
  <marker id="arr_n" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C['ol']}"/>
  </marker>
  <marker id="arr_a" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C['act']}"/>
  </marker>
</defs>\n"""

    # ── DRAW NODES ────────────────────────────────────────────────────────
    def N(nid, fill, label="", fs=10, bold=False, bullets=None, dashed=False):
        return node(*G[nid], fill, label=label, fs=fs, bold=bold,
                    bullets=bullets, dashed=dashed,
                    active=a(nid), dimmed=d(nid))

    # R0-R1
    svg += N("header",  C["purple"], "Neutropaenic Sepsis Management", fs=13, bold=True)
    svg += N("review72", C["blue"],  "Review at 72 hours empiric antibiotics", fs=10)

    # R2
    svg += N("resolved_fever",   C["yellow"],
             "Resolved fever: Afebrile ≥48h & clinically stable", fs=10)
    svg += N("micro_defined",    C["yellow"],
             "Microbiologically or clinically defined infection", fs=10, dashed=True)
    svg += N("persistent_fever", C["pink"],
             "Persistent fever or remains clinically unstable", fs=10)

    # R3
    svg += N("fever_unknown", C["yellow"], "Fever of unknown origin", fs=10)
    svg += N("liaise_id",     C["white"],  "Liaise with ID", fs=10, bold=True, dashed=True)
    svg += N("p_stable",      C["yellow"], "Clinically stable", fs=10)
    svg += node(*G["p_unstable"], C["pink"], fs=9, bold=True,
                bullets=["Consider aminoglycoside",
                         "Liaise with ID re MRO",
                         "Repeat periph & central cultures"],
                active=a("p_unstable"), dimmed=d("p_unstable"))

    # R4
    svg += N("l_neutro_resolved", C["yellow"], "Resolved neutropaenia", fs=9)
    svg += N("l_neutro_ongoing",  C["yellow"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_ongoing",  C["yellow"], "Ongoing neutropaenia",  fs=9)
    svg += N("r_neutro_resolved", C["yellow"], "Resolved neutropaenia", fs=9)
    svg += N("continue_stable",   C["green"],  "Continue empiric therapy", fs=9, bold=True)
    svg += node(*G["unstable_box"], C["pink"], fs=9,
                bullets=["Liaise with ID",
                         "CT chest ± abdo/pelvis/sinus",
                         "MRI brain if CNS signs",
                         "Consider non-infective causes"],
                active=a("unstable_box"), dimmed=d("unstable_box"))

    # R5
    svg += N("l_entero_yes", C["yellow"], "Enterocolitis / mucositis",    fs=9)
    svg += N("l_entero_no",  C["yellow"], "No enterocolitis / mucositis", fs=9)
    svg += N("r_entero_yes", C["yellow"], "Enterocolitis / mucositis",    fs=9)
    svg += N("r_entero_no",  C["yellow"], "No enterocolitis / mucositis", fs=9)
    svg += node(*G["imaging_box"], C["yellow"], fs=9,
                bullets=["Liaise with ID",
                         "CT chest ± abdo/pelvis/sinus",
                         "MRI brain if CNS signs",
                         "Consider non-infective causes"],
                active=a("imaging_box"), dimmed=d("imaging_box"))

    # R6 — mutually exclusive per path
    svg += N("stop_abx",   C["green"],  "Stop antibiotics",            fs=9, bold=True)
    svg += N("continue_l", C["green"],  "Continue empiric antibiotics",fs=9, bold=True)
    svg += N("allo_sct",   C["yellow"], "Allo-SCT patient",            fs=9)
    svg += N("non_allo",   C["yellow"], "Non-allo-SCT patient",        fs=9)
    svg += N("continue_r", C["green"],  "Continue empiric antibiotics",fs=9, bold=True)
    svg += N("target_abx", C["green"],  "Target antibiotics",          fs=9, bold=True)

    # R7
    svg += node(*G["cease_allo"], C["yellow"],
                label="Consider ceasing if another cause found", fs=9,
                active=a("cease_allo"), dimmed=d("cease_allo"))
    svg += node(*G["cease_non_allo"], C["yellow"],
                label="Consider ceasing empiric antibiotics", fs=9,
                active=a("cease_non_allo"), dimmed=d("cease_non_allo"))

    # Recurrent
    svg += N("recurrent_fever",   C["purple"], "Recurrent fever", fs=10, bold=True)
    svg += node(*G["recurrent_actions"], C["pink"], fs=9,
                bullets=["Restart empiric abx & consider aminoglycoside",
                         "Liaise with ID about MRO coverage",
                         "Repeat peripheral & central cultures"],
                active=a("recurrent_actions"), dimmed=d("recurrent_actions"))

    # ── DRAW ARROWS ───────────────────────────────────────────────────────
    # Convenience: arrow from node bottom-centre to node top-centre
    def A(src, dst):
        return arrow(gcx(src), gbot(src), gcx(dst), gtop(dst),
                     act=a(src), dim=d(src) or d(dst))

    def E(src, dst, by=None, bx=None, x1=None, y1=None, x2=None, y2=None):
        _x1 = x1 if x1 is not None else gcx(src)
        _y1 = y1 if y1 is not None else gbot(src)
        _x2 = x2 if x2 is not None else gcx(dst)
        _y2 = y2 if y2 is not None else gtop(dst)
        return elbow(_x1, _y1, _x2, _y2, by=by, bx=bx,
                     act=a(src), dim=d(src) or d(dst))

    # header → review72
    svg += A("header", "review72")

    # review72 → three R2 branches via bus at y=95
    bus_y = 95
    # stem down from review72
    svg += seg(gcx("review72"), gbot("review72"), gcx("review72"), bus_y,
               act=a("review72"), dim=d("review72"))
    # horizontal bus
    lbus = gcx("resolved_fever")
    rbus = gcx("persistent_fever")
    svg += seg(lbus, bus_y, rbus, bus_y)
    # drops to each branch
    for nid in ("resolved_fever", "micro_defined", "persistent_fever"):
        svg += arrow(gcx(nid), bus_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # resolved_fever → fever_unknown
    svg += A("resolved_fever", "fever_unknown")
    # micro_defined → liaise_id
    svg += A("micro_defined", "liaise_id")

    # persistent_fever → p_stable / p_unstable via bus at y=156
    pb_y = 156
    svg += seg(gcx("persistent_fever"), gbot("persistent_fever"),
               gcx("persistent_fever"), pb_y, act=a("persistent_fever"), dim=d("persistent_fever"))
    svg += seg(gcx("p_stable"), pb_y, gcx("p_unstable"), pb_y)
    for nid in ("p_stable", "p_unstable"):
        svg += arrow(gcx(nid), pb_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # p_stable → continue_stable
    svg += A("p_stable", "continue_stable")
    # p_unstable → unstable_box
    svg += A("p_unstable", "unstable_box")
    # unstable_box → imaging_box
    svg += A("unstable_box", "imaging_box")

    # fever_unknown → l_neutro split via bus at y=212
    lb_y = 212
    svg += seg(gcx("fever_unknown"), gbot("fever_unknown"),
               gcx("fever_unknown"), lb_y, act=a("fever_unknown"), dim=d("fever_unknown"))
    svg += seg(gcx("l_neutro_resolved"), lb_y, gcx("l_neutro_ongoing"), lb_y)
    for nid in ("l_neutro_resolved", "l_neutro_ongoing"):
        svg += arrow(gcx(nid), lb_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # liaise_id → r_neutro split via bus at y=212
    svg += seg(gcx("liaise_id"), gbot("liaise_id"),
               gcx("liaise_id"), lb_y, act=a("liaise_id"), dim=d("liaise_id"))
    svg += seg(gcx("r_neutro_ongoing"), lb_y, gcx("r_neutro_resolved"), lb_y)
    for nid in ("r_neutro_ongoing", "r_neutro_resolved"):
        svg += arrow(gcx(nid), lb_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_neutro_resolved → stop_abx (straight down, same col)
    svg += arrow(gcx("l_neutro_resolved"), gbot("l_neutro_resolved"),
                 gcx("stop_abx"), gtop("stop_abx"),
                 act=a("l_neutro_resolved"), dim=d("l_neutro_resolved") or d("stop_abx"))

    # l_neutro_ongoing → l_entero split via bus at y=266
    le_y = 266
    svg += seg(gcx("l_neutro_ongoing"), gbot("l_neutro_ongoing"),
               gcx("l_neutro_ongoing"), le_y, act=a("l_neutro_ongoing"), dim=d("l_neutro_ongoing"))
    svg += seg(gcx("l_entero_yes"), le_y, gcx("l_entero_no"), le_y)
    for nid in ("l_entero_yes", "l_entero_no"):
        svg += arrow(gcx(nid), le_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_entero_yes → continue_l
    svg += arrow(gcx("l_entero_yes"), gbot("l_entero_yes"),
                 gcx("continue_l"), gtop("continue_l"),
                 act=a("l_entero_yes"), dim=d("l_entero_yes") or d("continue_l"))

    # l_entero_no → allo/non-allo split via bus at y=320
    la_y = 320
    svg += seg(gcx("l_entero_no"), gbot("l_entero_no"),
               gcx("l_entero_no"), la_y, act=a("l_entero_no"), dim=d("l_entero_no"))
    svg += seg(gcx("allo_sct"), la_y, gcx("non_allo"), la_y)
    for nid in ("allo_sct", "non_allo"):
        svg += arrow(gcx(nid), la_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # allo_sct → cease_allo
    svg += arrow(gcx("allo_sct"), gbot("allo_sct"),
                 gcx("cease_allo"), gtop("cease_allo"),
                 act=a("allo_sct"), dim=d("allo_sct") or d("cease_allo"))
    # non_allo → cease_non_allo
    svg += arrow(gcx("non_allo"), gbot("non_allo"),
                 gcx("cease_non_allo"), gtop("cease_non_allo"),
                 act=a("non_allo"), dim=d("non_allo") or d("cease_non_allo"))

    # r_neutro_ongoing → r_entero split via bus at y=266
    svg += seg(gcx("r_neutro_ongoing"), gbot("r_neutro_ongoing"),
               gcx("r_neutro_ongoing"), le_y, act=a("r_neutro_ongoing"), dim=d("r_neutro_ongoing"))
    svg += seg(gcx("r_entero_yes"), le_y, gcx("r_entero_no"), le_y)
    for nid in ("r_entero_yes", "r_entero_no"):
        svg += arrow(gcx(nid), le_y, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # r_entero_yes → continue_r
    svg += arrow(gcx("r_entero_yes"), gbot("r_entero_yes"),
                 gcx("continue_r"), gtop("continue_r"),
                 act=a("r_entero_yes"), dim=d("r_entero_yes") or d("continue_r"))

    # r_entero_no → target_abx
    svg += arrow(gcx("r_entero_no"), gbot("r_entero_no"),
                 gcx("target_abx"), gtop("target_abx"),
                 act=a("r_entero_no"), dim=d("r_entero_no") or d("target_abx"))

    # r_neutro_resolved → target_abx (elbow: down then left then down)
    rr_y = 266   # same bus level
    svg += elbow(gcx("r_neutro_resolved"), gbot("r_neutro_resolved"),
                 gcx("target_abx"), gtop("target_abx"), by=rr_y,
                 act=a("r_neutro_resolved"), dim=d("r_neutro_resolved") or d("target_abx"))

    # persistent_fever → recurrent_fever: elbow out right side then down
    rf_bx = grgt("persistent_fever") + 12
    svg += elbow(grgt("persistent_fever"), gcy("persistent_fever"),
                 gcx("recurrent_fever"), gtop("recurrent_fever"),
                 bx=rf_bx,
                 act=a("persistent_fever"), dim=d("persistent_fever") or d("recurrent_fever"))

    # recurrent_fever → recurrent_actions
    svg += A("recurrent_fever", "recurrent_actions")

    # ── LEGEND ────────────────────────────────────────────────────────────
    ly = 640
    legend_items = [
        (10,   C["green"],  "Action / recommendation"),
        (230,  C["yellow"], "Clinical decision point"),
        (450,  C["pink"],   "Urgent / unstable"),
        (640,  C["purple"], "Pathway header"),
        (830,  C["white"],  "▶  Active pathway highlighted"),
    ]
    for lx, lc, lt in legend_items:
        svg += node(lx, ly, 195, 26, lc, label=lt, fs=9)
    # active border on last item
    svg += (f'<rect x="830" y="{ly}" width="195" height="26" rx="7" '
            f'fill="none" stroke="{C["act"]}" stroke-width="2.5"/>\n')

    svg += "</svg>\n"
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_recommendations(AN):
    recs = []
    if "stop_abx" in AN:
        recs.append(("✅", "Stop antibiotics",
                     "Neutropaenia resolved and fever resolved — antibiotics can be discontinued."))
    if any(x in AN for x in ("continue_l","continue_r","continue_stable")):
        recs.append(("💊", "Continue empiric antibiotics",
                     "Clinical situation warrants ongoing broad-spectrum cover."))
    if "cease_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Allo-SCT)",
                     "Cease if another cause found. Discuss with ID / haematology."))
    if "cease_non_allo" in AN:
        recs.append(("⚠️", "Consider ceasing empiric antibiotics (Non-allo-SCT)",
                     "Discuss with ID / treating team."))
    if "target_abx" in AN:
        recs.append(("🎯", "Target antibiotics",
                     "De-escalate to targeted therapy based on identified pathogen / source."))
    if "p_unstable" in AN:
        recs.append(("🚨", "Clinically unstable — escalate immediately",
                     "Consider aminoglycoside. Liaise with ID re MRO coverage. "
                     "Repeat peripheral and central cultures."))
    if "unstable_box" in AN:
        recs.append(("🖥️", "Investigations",
                     "CT chest ± abdo/pelvis/sinus guided by symptoms. "
                     "MRI brain if CNS signs / symptoms. Consider non-infective causes."))
    if "recurrent_actions" in AN:
        recs.append(("🔄", "Recurrent fever management",
                     "Restart empiric antibiotics and consider aminoglycoside. "
                     "Liaise with ID about MRO coverage. Repeat peripheral and central cultures."))
    return recs


# ══════════════════════════════════════════════════════════════════════════════
# COPY-TO-CLIPBOARD JS
# ══════════════════════════════════════════════════════════════════════════════

COPY_JS = """
<button id="copyBtn" onclick="copyChart()" style="
    background:#2471A3;color:#fff;border:none;border-radius:7px;
    padding:9px 20px;font-size:14px;cursor:pointer;
    font-family:Arial,sans-serif;display:inline-flex;
    align-items:center;gap:8px;margin-bottom:6px;">
  <span>📋</span><span>Copy flowchart to clipboard</span>
</button>
<div id="copyMsg" style="font-size:12px;font-family:Arial,sans-serif;
     min-height:18px;margin-top:3px;"></div>
<script>
async function copyChart() {
  const msg = document.getElementById('copyMsg');
  msg.style.color='#888'; msg.textContent='Rendering…';
  const svg = document.getElementById('flowSVG');
  if (!svg) { msg.textContent='⚠️ SVG not found.'; return; }
  const ser = new XMLSerializer().serializeToString(svg);
  const vb  = svg.viewBox.baseVal;
  const sc  = 2;
  const cv  = document.createElement('canvas');
  cv.width  = vb.width * sc;
  cv.height = vb.height * sc;
  const ctx = cv.getContext('2d');
  ctx.scale(sc, sc);
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, vb.width, vb.height);
  const blob = new Blob([ser], {type:'image/svg+xml;charset=utf-8'});
  const url  = URL.createObjectURL(blob);
  const img  = new Image();
  img.onload = async () => {
    ctx.drawImage(img, 0, 0);
    URL.revokeObjectURL(url);
    cv.toBlob(async (pngBlob) => {
      if (navigator.clipboard && navigator.clipboard.write) {
        try {
          await navigator.clipboard.write([new ClipboardItem({'image/png': pngBlob})]);
          msg.style.color='#1e8449';
          msg.textContent='✅ Copied! Paste into eNotes with Ctrl+V / Cmd+V.';
          return;
        } catch(e) {}
      }
      // fallback: download
      const a = document.createElement('a');
      a.href = cv.toDataURL('image/png');
      a.download = 'neutropenic_sepsis_pathway.png';
      a.click();
      msg.style.color='#e67e22';
      msg.textContent='📥 Saved as PNG — insert into eNotes manually.';
    }, 'image/png');
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
        ["Resolved (afebrile ≥48h, clinically stable)",
         "Persistent / recurrent fever"],
    ) == "Resolved (afebrile ≥48h, clinically stable)"

    neutro_resolved = st.radio(
        "**Neutropaenia status**",
        ["Resolved", "Ongoing"],
        index=1,
    ) == "Resolved"

    micro_defined = st.checkbox(
        "**Microbiologically or clinically defined infection**", value=False
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
        fever_resolved=fever_resolved,
        neutro_resolved=neutro_resolved,
        stable=stable,
        enterocolitis=enterocolitis,
        allo_sct=allo_sct,
        micro_defined=micro_defined,
    )

    svg_str = build_svg(AN)

    html = f"""<!DOCTYPE html>
<html><head><style>body{{margin:0;padding:4px;background:#fff}}</style></head>
<body>
{COPY_JS}
<div style="overflow-x:auto;margin-top:4px">{svg_str}</div>
</body></html>"""

    components.html(html, height=800, scrolling=True)

# Recommendations
st.markdown("---")
st.subheader("📋 Recommended Actions")

recs = get_recommendations(AN)
if recs:
    for icon, title, detail in recs:
        st.markdown(f"**{icon} {title}**  \n{detail}")
else:
    st.info("Select patient parameters to see recommendations.")

st.markdown("---")
st.caption("Based on ADHB Neutropaenic Sepsis Management Guidelines. Not a substitute for clinical judgement.")
