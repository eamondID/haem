"""
Neutropaenic Sepsis Management — Interactive Decision Support
ADHB Antimicrobial Stewardship  v2 — Enhanced Visualisation
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neutropaenic Sepsis Management",
    page_icon="🧬",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════════════════
C = {
    # Node fills — cleaner, more intentional palette
    "hdr_fill":    "#7B3FA0",   # deep purple — main title
    "hdr_text":    "#FFFFFF",
    "review_fill": "#2E86C1",   # strong blue — 72hr review
    "review_text": "#FFFFFF",

    # Branch header fills (coloured per section)
    "resolved_fill":    "#6C3483",   # deep purple
    "resolved_text":    "#FFFFFF",
    "persistent_fill":  "#A93226",   # deep red
    "persistent_text":  "#FFFFFF",

    # Lane background tints (very subtle)
    "lane_l":  "#F9F4FC",   # pale lavender  — fever unknown path
    "lane_m":  "#F2F8FF",   # pale blue      — micro-defined path
    "lane_r":  "#FFFDF5",   # pale amber     — persistent path

    # Decision / condition nodes
    "decision_fill":   "#FDFEFE",
    "decision_stroke": "#5D6D7E",

    # Action nodes (terminal)
    "action_stop":     "#1E8449",   # dark green — Stop
    "action_stop_t":   "#FFFFFF",
    "action_cont":     "#1A5276",   # dark navy  — Continue empiric
    "action_cont_t":   "#FFFFFF",
    "action_target":   "#117A65",   # teal       — Target
    "action_target_t": "#FFFFFF",
    "action_cease":    "#7D6608",   # dark gold  — Cease / consider
    "action_cease_t":  "#FFFFFF",

    # Urgent / unstable
    "urgent_fill":     "#F1948A",
    "urgent_dark":     "#922B21",   # deep red for p_unstable

    # Recurrent
    "recurrent_fill":  "#7B3FA0",
    "recurrent_text":  "#FFFFFF",
    "recurrent_box":   "#FDEDEC",

    # Connectors
    "ol":   "#7F8C8D",
    "act":  "#1A6B5E",   # dark teal — active pathway highlight
    "dim_fill":   "#F8F9F9",
    "dim_stroke": "#D5D8DC",
    "dim_text":   "#D5D8DC",

    # Label text on branch lines
    "label_text": "#5D6D7E",
}

FONT = "Arial, Helvetica, sans-serif"

# ══════════════════════════════════════════════════════════════════════════════
# SVG PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def _wrap(text, box_w, fs):
    cw  = fs * 0.54
    mc  = max(1, int((box_w - 16) / cw))
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= mc: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [text]

def rect(x, y, w, h, fill, stroke, sw=1.5, rx=7, dash=False):
    d = ' stroke-dasharray="5,3"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>\n'

def node(x, y, w, h, fill, stroke, label="", fs=10, bold=False, text_color="#111",
         bullets=None, active=False, dimmed=False, dashed=False, sw=1.5, rx=7):
    if dimmed:
        fill, stroke, text_color, sw = C["dim_fill"], C["dim_stroke"], C["dim_text"], 1
    elif active:
        stroke, sw = C["act"], 2
    s = rect(x, y, w, h, fill, stroke, sw=sw, rx=rx, dash=dashed)
    lh = fs + 3.5
    fw = "bold" if bold else "normal"
    if bullets:
        tot = len(bullets) * lh
        ty0 = y + max(fs + 2, (h - tot) / 2 + fs)
        for i, b in enumerate(bullets):
            s += f'<text x="{x+10}" y="{ty0+i*lh}" font-size="{fs}" fill="{text_color}" font-family="{FONT}">• {esc(b)}</text>\n'
    elif label:
        lines = _wrap(label, w, fs)
        tot   = len(lines) * lh
        ty0   = y + (h - tot) / 2 + fs
        for i, ln in enumerate(lines):
            s += f'<text x="{x+w/2}" y="{ty0+i*lh}" font-size="{fs}" font-weight="{fw}" fill="{text_color}" font-family="{FONT}" text-anchor="middle">{esc(ln)}</text>\n'
    return s

def arrow(x1, y1, x2, y2, act=False, dim=False):
    clr = C["act"] if act else (C["dim_stroke"] if dim else C["ol"])
    sw  = 1.8 if act else 1.3
    mk  = f'url(#arr_{"a" if act else "n"})'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}" marker-end="{mk}"/>\n'

def seg(x1, y1, x2, y2, act=False, dim=False):
    clr = C["act"] if act else (C["dim_stroke"] if dim else C["ol"])
    sw  = 1.8 if act else 1.3
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{clr}" stroke-width="{sw}"/>\n'

def poly(pts, act=False, dim=False):
    clr = C["act"] if act else (C["dim_stroke"] if dim else C["ol"])
    sw  = 1.8 if act else 1.3
    s   = " ".join(f"{x},{y}" for x,y in pts)
    mk  = f'url(#arr_{"a" if act else "n"})'
    return f'<polyline points="{s}" fill="none" stroke="{clr}" stroke-width="{sw}" marker-end="{mk}"/>\n'

def branch_label(x, y, text, act=False, dim=False):
    """Small italic label on a branch arrow — with white background pill for readability."""
    clr = C["act"] if act else (C["dim_text"] if dim else C["label_text"])
    cw = 5.2 * len(text)  # approximate text width
    rx, ry, rw, rh = x - cw/2 - 3, y - 9, cw + 6, 11
    bg = f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="3" fill="white" opacity="0.85"/>\n'
    txt = f'<text x="{x}" y="{y}" font-size="8.5" font-style="italic" fill="{clr}" font-family="{FONT}" text-anchor="middle">{esc(text)}</text>\n'
    return bg + txt

def lane_bg(x, y, w, h, fill, label="", label_color="#999"):
    """Subtle lane background rectangle with optional vertical label."""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="none"/>\n'
    if label:
        tx = x + 10
        ty = y + h // 2
        s += (f'<text x="{tx}" y="{ty}" font-size="8" fill="{label_color}" '
              f'font-family="{FONT}" text-anchor="middle" '
              f'transform="rotate(-90,{tx},{ty})" opacity="0.6">{esc(label)}</text>\n')
    return s

def row_band(x, y, w, h, fill):
    """Subtle horizontal band for row-level visual grouping."""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="none"/>\n'

def divider(x, y1, y2, dim=False):
    """Thin vertical lane divider."""
    clr = "#D5D8DC" if dim else "#BFC9CA"
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{clr}" stroke-width="1" stroke-dasharray="3,4"/>\n'

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
                AN.add("recurrent_fever")
                AN.add("recurrent_box")
            else:
                AN.add("r_neutro_ongoing")
                if enterocolitis:
                    AN.add("r_entero_yes")
                    AN.add("continue_r")
                else:
                    AN.add("r_entero_no")
                    AN.add("target_abx")
                    AN.add("recurrent_fever")
                    AN.add("recurrent_box")
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
        if stable:
            AN.add("p_stable")
        else:
            AN.add("p_unstable")
            AN.add("imaging_box")

    return AN

# ══════════════════════════════════════════════════════════════════════════════
# SVG BUILD
# ══════════════════════════════════════════════════════════════════════════════

NW = 105    # narrow node width
MW = 145    # medium (continue empiric)

def build_svg(AN):
    def a(n): return n in AN
    def d(n): return len(AN) > 2 and n not in AN

    W, H = 1260, 780

    # ── Column centres ────────────────────────────────────────────────────
    CA = 68     # stop_abx / l_neutro_resolved
    CB = 200    # continue_l / l_entero_yes
    CC = 328    # allo_sct / l_entero_no / l_neutro_ongoing
    CD = 440    # non_allo
    CE = 568    # continue_r / r_entero_yes / r_neutro_ongoing
    CF = 700    # r_entero_no
    CG = 810    # target_abx / r_neutro_resolved / recurrent
    CH = 975    # p_stable
    CI = 1135   # p_unstable / imaging_box

    def cx(c, w): return c - w // 2

    # ── Lane boundaries (for background panels) ───────────────────────────
    LANE_PAD   = 6
    LANE_TOP   = 88     # top of lane backgrounds (below review72)
    LANE_BOT   = 690    # bottom of lane backgrounds
    # Left lane: CA to CC area
    L_LANE_X   = 12
    L_LANE_W   = CD - 40 - 12          # ~388
    # Mid lane: CE to CG area
    M_LANE_X   = CD - 30               # ~410
    M_LANE_W   = CG + NW//2 + 15 - M_LANE_X   # ~460
    # Right lane
    R_LANE_X   = M_LANE_X + M_LANE_W + 8
    R_LANE_W   = W - R_LANE_X - 12

    # ── Geometry dict ─────────────────────────────────────────────────────
    G = {}

    # Header / review rows
    G["header"]   = (370, 8,  520, 38)
    G["review72"] = (300, 56, 660, 28)

    # R2: branch headers
    G["resolved_fever"]   = (L_LANE_X,  92, R_LANE_X - L_LANE_X - 8, 40)
    G["persistent_fever"] = (R_LANE_X,  92, R_LANE_W,  40)

    # R3: sub-branch nodes
    G["fever_unknown"] = (L_LANE_X,  166, L_LANE_W // 2 + 30, 32)
    G["micro_defined"] = (M_LANE_X,  164, M_LANE_W - 4, 40)   # dashed
    G["p_stable"]      = (R_LANE_X,  166, (R_LANE_W - 10) // 2, 32)
    G["p_unstable"]    = (R_LANE_X + (R_LANE_W - 10) // 2 + 10, 162, (R_LANE_W - 10) // 2, 52)

    # R4: liaise_id
    G["liaise_id"] = (M_LANE_X + 4, 216, M_LANE_W - 12, 28)  # dashed

    # R5: neutropaenia status
    G["l_neutro_resolved"] = (cx(CA, NW), 278, NW, 30)
    G["l_neutro_ongoing"]  = (cx(CC, NW), 278, NW, 30)
    G["r_neutro_ongoing"]  = (cx(CE, NW), 278, NW, 30)
    G["r_neutro_resolved"] = (cx(CG, NW), 278, NW, 30)
    G["imaging_box"]       = (R_LANE_X,   258, R_LANE_W, 112)

    # R6: enterocolitis (tighter height)
    G["l_entero_yes"] = (cx(CB, NW), 342, NW, 48)
    G["l_entero_no"]  = (cx(CC, NW), 342, NW, 48)
    G["r_entero_yes"] = (cx(CE, NW), 342, NW, 48)
    G["r_entero_no"]  = (cx(CF, NW), 342, NW, 48)

    # R7: action nodes — terminal — slightly taller, stronger visual weight
    G["stop_abx"]   = (cx(CA, NW),  424, NW,  34)
    G["continue_l"] = (cx(CB, MW),  406, MW,  42)
    G["allo_sct"]   = (cx(CC, NW),  424, NW,  34)
    G["non_allo"]   = (cx(CD, NW),  424, NW,  34)
    G["continue_r"] = (cx(CE, MW),  406, MW,  42)
    G["target_abx"] = (cx(CG, NW),  424, NW,  34)

    # R8: cease nodes
    G["cease_allo"]     = (cx(CC, MW), 478, MW, 52)
    G["cease_non_allo"] = (410,        478, MW, 38)

    # Recurrent fever (same column as target_abx)
    G["recurrent_fever"] = (cx(CG, NW + 60), 478, NW + 60, 30)
    G["recurrent_box"]   = (cx(CG, NW + 120), 524, NW + 120, 86)

    # ── Helpers ───────────────────────────────────────────────────────────
    def gx(n):   return G[n][0]
    def gy(n):   return G[n][1]
    def gw(n):   return G[n][2]
    def gh(n):   return G[n][3]
    def gcx(n):  return G[n][0] + G[n][2] // 2
    def gtop(n): return G[n][1]
    def gbot(n): return G[n][1] + G[n][3]
    def grgt(n): return G[n][0] + G[n][2]

    # ── SVG OPEN ──────────────────────────────────────────────────────────
    svg = (f'<svg id="flowSVG" xmlns="http://www.w3.org/2000/svg" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'style="background:#FAFAFA;font-family:{FONT}">\n')

    svg += f'''<defs>
  <marker id="arr_n" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C["ol"]}"/>
  </marker>
  <marker id="arr_a" markerWidth="9" markerHeight="9" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L0,7 L9,3.5 z" fill="{C["act"]}"/>
  </marker>
  <filter id="shadow" x="-5%" y="-5%" width="110%" height="120%">
    <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#00000018"/>
  </filter>
</defs>\n'''

    # ── BACKGROUND LAYERS ─────────────────────────────────────────────────
    # White base
    svg += f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FAFAFA"/>\n'

    # Lane backgrounds (drawn before nodes so nodes sit on top)
    L_lc = C["lane_l"] if not d("fever_unknown") else C["dim_fill"]
    M_lc = C["lane_m"] if not d("micro_defined") else C["dim_fill"]
    R_lc = C["lane_r"] if not d("persistent_fever") else C["dim_fill"]

    svg += lane_bg(L_LANE_X, LANE_TOP, L_LANE_W, LANE_BOT - LANE_TOP, L_lc)
    svg += lane_bg(M_LANE_X, LANE_TOP, M_LANE_W, LANE_BOT - LANE_TOP, M_lc)
    svg += lane_bg(R_LANE_X, LANE_TOP, R_LANE_W, LANE_BOT - LANE_TOP, R_lc)

    # Single faint action row band — scoped to left+mid lanes only, very subtle
    svg += row_band(L_LANE_X, 416, R_LANE_X - L_LANE_X - 8, 52, "#E8EAF0")

    # Vertical lane dividers
    svg += divider(M_LANE_X - 2, LANE_TOP + 46, 660)
    # Right divider stops at imaging box top to avoid intersecting it
    svg += divider(R_LANE_X - 2, LANE_TOP + 46, 238)

    # ── DRAW NODES ────────────────────────────────────────────────────────
    def N(nid, fill, stroke, label="", fs=10, bold=False, text_color="#111",
          bullets=None, dashed=False, sw=1.5, rx=7):
        x, y, w, h = G[nid]
        return node(x, y, w, h, fill, stroke,
                    label=label, fs=fs, bold=bold, text_color=text_color,
                    bullets=bullets, active=a(nid), dimmed=d(nid),
                    dashed=dashed, sw=sw, rx=rx)

    # Top nodes — with shadow filter applied via extra rect
    svg += f'<g filter="url(#shadow)">\n'
    svg += N("header",   C["hdr_fill"],    C["hdr_fill"],
             "Neutropaenic Sepsis Management", fs=14, bold=True,
             text_color=C["hdr_text"], sw=0)
    svg += N("review72", C["review_fill"], C["review_fill"],
             "Review at 72 hours empiric antibiotics", fs=10, bold=True,
             text_color=C["review_text"], sw=0)
    svg += f'</g>\n'

    # Branch headers
    svg += N("resolved_fever",   C["resolved_fill"], C["resolved_fill"],
             "Resolved fever:  Afebrile >48 hours & clinically stable",
             fs=10, bold=True, text_color=C["resolved_text"], sw=0)
    svg += N("persistent_fever", C["persistent_fill"], C["persistent_fill"],
             "Persistent fever or remains clinically unstable",
             fs=10, bold=True, text_color=C["persistent_text"], sw=0)

    # R3 sub-branch decision nodes
    svg += N("fever_unknown", C["decision_fill"], C["decision_stroke"],
             "Fever of unknown origin", fs=9, sw=1.5)
    svg += N("micro_defined", C["decision_fill"], "#2E86C1",
             "Microbiologically or clinically defined infection",
             fs=9, dashed=True, sw=1.5)
    svg += N("p_stable", C["decision_fill"], C["decision_stroke"],
             "Clinically stable: Continue empiric therapy", fs=9, sw=1.5)
    svg += node(*G["p_unstable"], C["urgent_fill"], C["urgent_dark"],
                fs=9, bold=True, text_color="#7B241C",
                bullets=["Clinically unstable:",
                         "Consider aminoglycoside",
                         "Liaise with ID re MRO",
                         "Repeat periph & central cultures"],
                active=a("p_unstable"), dimmed=d("p_unstable"), sw=2)

    # R4: liaise_id
    svg += N("liaise_id", C["decision_fill"], "#2E86C1",
             "Liaise with ID", fs=9, dashed=True)

    # R5: neutropaenia
    for nid in ("l_neutro_resolved", "l_neutro_ongoing",
                "r_neutro_ongoing",  "r_neutro_resolved"):
        lbl = "Resolved neutropaenia" if "resolved" in nid else "Ongoing neutropaenia"
        svg += N(nid, C["decision_fill"], C["decision_stroke"], lbl, fs=8.5)

    # Imaging box (right, tall bullet box)
    svg += node(*G["imaging_box"], C["decision_fill"], C["decision_stroke"],
                fs=9,
                bullets=["Liaise with ID",
                         "CT chest ± abdo/pelvis/sinus",
                         "MRI brain if CNS signs",
                         "Consider non-infective causes"],
                active=a("imaging_box"), dimmed=d("imaging_box"))

    # R6: enterocolitis nodes
    for nid, lbl in [
        ("l_entero_yes", "Has enterocolitis\nor mucositis"),
        ("l_entero_no",  "No enterocolitis\nor mucositis"),
        ("r_entero_yes", "Has enterocolitis\nor mucositis"),
        ("r_entero_no",  "No enterocolitis\nor mucositis"),
    ]:
        svg += N(nid, C["decision_fill"], C["decision_stroke"], lbl, fs=8.5)

    # R7: TERMINAL ACTION NODES — distinct fills, bold, slightly larger
    svg += N("stop_abx",   C["action_stop"],    C["action_stop"],
             "Stop antibiotics",            fs=9, bold=True,
             text_color=C["action_stop_t"], sw=0, rx=8)
    svg += N("continue_l", C["action_cont"],    C["action_cont"],
             "Continue empiric antibiotics", fs=9, bold=True,
             text_color=C["action_cont_t"], sw=0, rx=8)
    svg += N("allo_sct",   C["decision_fill"],  C["decision_stroke"],
             "Allo-SCT patient",            fs=8.5)
    svg += N("non_allo",   C["decision_fill"],  C["decision_stroke"],
             "Non-allo-SCT patient",        fs=8.5)
    svg += N("continue_r", C["action_cont"],    C["action_cont"],
             "Continue empiric antibiotics", fs=9, bold=True,
             text_color=C["action_cont_t"], sw=0, rx=8)
    svg += N("target_abx", C["action_target"],  C["action_target"],
             "Target antibiotics",          fs=9, bold=True,
             text_color=C["action_target_t"], sw=0, rx=8)

    # R8: cease nodes
    svg += node(*G["cease_allo"], C["action_cease"], C["action_cease"],
                label="Consider ceasing if another cause found",
                fs=8.5, bold=False, text_color=C["action_cease_t"],
                active=a("cease_allo"), dimmed=d("cease_allo"), sw=0, rx=8)
    svg += node(*G["cease_non_allo"], C["action_cease"], C["action_cease"],
                label="Consider ceasing empiric antibiotics",
                fs=8.5, bold=False, text_color=C["action_cease_t"],
                active=a("cease_non_allo"), dimmed=d("cease_non_allo"), sw=0, rx=8)

    # Recurrent
    svg += N("recurrent_fever", C["recurrent_fill"], C["recurrent_fill"],
             "Recurrent fever", fs=10, bold=True,
             text_color=C["recurrent_text"], sw=0)
    svg += node(*G["recurrent_box"], C["recurrent_box"], C["urgent_dark"],
                fs=8.5, sw=1.5,
                bullets=["Clinically unstable:",
                         "Restart empiric abx + consider aminoglycoside",
                         "Liaise with ID re MRO coverage",
                         "Repeat peripheral & central cultures"],
                active=a("recurrent_box"), dimmed=d("recurrent_box"))

    # ── ARROWS ────────────────────────────────────────────────────────────
    # header → review72
    svg += arrow(gcx("header"), gbot("header"), gcx("review72"), gtop("review72"),
                 act=a("header"))

    # review72 → resolved_fever & persistent_fever via bus
    bus1 = 84
    svg += seg(gcx("review72"), gbot("review72"), gcx("review72"), bus1, act=a("review72"))
    svg += seg(gcx("resolved_fever"), bus1, gcx("persistent_fever"), bus1)
    for nid in ("resolved_fever", "persistent_fever"):
        svg += arrow(gcx(nid), bus1, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # resolved_fever → fever_unknown | micro_defined via bus
    bus2 = 152
    svg += seg(gcx("resolved_fever"), gbot("resolved_fever"), gcx("resolved_fever"), bus2,
               act=a("resolved_fever"), dim=d("resolved_fever"))
    svg += seg(gcx("fever_unknown"), bus2, gcx("micro_defined"), bus2)
    # branch labels
    svg += branch_label(gcx("fever_unknown") + 28, bus2 - 5, "No defined source",
                        act=a("fever_unknown"), dim=d("fever_unknown"))
    svg += branch_label(gcx("micro_defined") - 10, bus2 - 5, "Defined source",
                        act=a("micro_defined"), dim=d("micro_defined"))
    for nid in ("fever_unknown", "micro_defined"):
        svg += arrow(gcx(nid), bus2, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # persistent_fever → p_stable | p_unstable via bus
    svg += seg(gcx("persistent_fever"), gbot("persistent_fever"), gcx("persistent_fever"), bus2,
               act=a("persistent_fever"), dim=d("persistent_fever"))
    svg += seg(gcx("p_stable"), bus2, gcx("p_unstable"), bus2)
    svg += branch_label(gcx("p_stable") + 20, bus2 - 5, "Stable",
                        act=a("p_stable"), dim=d("p_stable"))
    svg += branch_label(gcx("p_unstable") - 18, bus2 - 5, "Unstable",
                        act=a("p_unstable"), dim=d("p_unstable"))
    for nid in ("p_stable", "p_unstable"):
        svg += arrow(gcx(nid), bus2, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # p_unstable → imaging_box
    svg += arrow(gcx("p_unstable"), gbot("p_unstable"), gcx("imaging_box"), gtop("imaging_box"),
                 act=a("p_unstable"), dim=d("p_unstable") or d("imaging_box"))

    # micro_defined → liaise_id
    svg += arrow(gcx("micro_defined"), gbot("micro_defined"), gcx("liaise_id"), gtop("liaise_id"),
                 act=a("micro_defined"), dim=d("micro_defined") or d("liaise_id"))

    # fever_unknown → l_neutro split
    bus3 = 264
    svg += seg(gcx("fever_unknown"), gbot("fever_unknown"), gcx("fever_unknown"), bus3,
               act=a("fever_unknown"), dim=d("fever_unknown"))
    svg += seg(gcx("l_neutro_resolved"), bus3, gcx("l_neutro_ongoing"), bus3)
    svg += branch_label(gcx("l_neutro_resolved") + 22, bus3 - 5, "Resolved",
                        act=a("l_neutro_resolved"), dim=d("l_neutro_resolved"))
    svg += branch_label(gcx("l_neutro_ongoing") - 22, bus3 - 5, "Ongoing",
                        act=a("l_neutro_ongoing"), dim=d("l_neutro_ongoing"))
    for nid in ("l_neutro_resolved", "l_neutro_ongoing"):
        svg += arrow(gcx(nid), bus3, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # liaise_id → r_neutro split
    svg += seg(gcx("liaise_id"), gbot("liaise_id"), gcx("liaise_id"), bus3,
               act=a("liaise_id"), dim=d("liaise_id"))
    svg += seg(gcx("r_neutro_ongoing"), bus3, gcx("r_neutro_resolved"), bus3)
    svg += branch_label(gcx("r_neutro_ongoing") + 22, bus3 - 5, "Ongoing",
                        act=a("r_neutro_ongoing"), dim=d("r_neutro_ongoing"))
    svg += branch_label(gcx("r_neutro_resolved") - 22, bus3 - 5, "Resolved",
                        act=a("r_neutro_resolved"), dim=d("r_neutro_resolved"))
    for nid in ("r_neutro_ongoing", "r_neutro_resolved"):
        svg += arrow(gcx(nid), bus3, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_neutro_resolved → stop_abx
    svg += arrow(gcx("l_neutro_resolved"), gbot("l_neutro_resolved"),
                 gcx("stop_abx"), gtop("stop_abx"),
                 act=a("l_neutro_resolved"), dim=d("l_neutro_resolved") or d("stop_abx"))

    # l_neutro_ongoing → entero split
    bus4 = 328
    svg += seg(gcx("l_neutro_ongoing"), gbot("l_neutro_ongoing"), gcx("l_neutro_ongoing"), bus4,
               act=a("l_neutro_ongoing"), dim=d("l_neutro_ongoing"))
    svg += seg(gcx("l_entero_yes"), bus4, gcx("l_entero_no"), bus4)
    svg += branch_label(gcx("l_entero_yes") + 20, bus4 - 5, "Yes",
                        act=a("l_entero_yes"), dim=d("l_entero_yes"))
    svg += branch_label(gcx("l_entero_no") - 20, bus4 - 5, "No",
                        act=a("l_entero_no"), dim=d("l_entero_no"))
    for nid in ("l_entero_yes", "l_entero_no"):
        svg += arrow(gcx(nid), bus4, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # r_neutro_ongoing → r_entero split
    svg += seg(gcx("r_neutro_ongoing"), gbot("r_neutro_ongoing"), gcx("r_neutro_ongoing"), bus4,
               act=a("r_neutro_ongoing"), dim=d("r_neutro_ongoing"))
    svg += seg(gcx("r_entero_yes"), bus4, gcx("r_entero_no"), bus4)
    svg += branch_label(gcx("r_entero_yes") + 20, bus4 - 5, "Yes",
                        act=a("r_entero_yes"), dim=d("r_entero_yes"))
    svg += branch_label(gcx("r_entero_no") - 20, bus4 - 5, "No",
                        act=a("r_entero_no"), dim=d("r_entero_no"))
    for nid in ("r_entero_yes", "r_entero_no"):
        svg += arrow(gcx(nid), bus4, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # l_entero_yes → continue_l
    svg += arrow(gcx("l_entero_yes"), gbot("l_entero_yes"),
                 gcx("continue_l"), gtop("continue_l"),
                 act=a("l_entero_yes"), dim=d("l_entero_yes") or d("continue_l"))

    # l_entero_no → allo/non_allo split
    bus5 = 410
    svg += seg(gcx("l_entero_no"), gbot("l_entero_no"), gcx("l_entero_no"), bus5,
               act=a("l_entero_no"), dim=d("l_entero_no"))
    svg += seg(gcx("allo_sct"), bus5, gcx("non_allo"), bus5)
    svg += branch_label(gcx("allo_sct") + 18, bus5 - 5, "Allo-SCT",
                        act=a("allo_sct"), dim=d("allo_sct"))
    svg += branch_label(gcx("non_allo") - 18, bus5 - 5, "Non-allo",
                        act=a("non_allo"), dim=d("non_allo"))
    for nid in ("allo_sct", "non_allo"):
        svg += arrow(gcx(nid), bus5, gcx(nid), gtop(nid), act=a(nid), dim=d(nid))

    # allo_sct → cease_allo
    svg += arrow(gcx("allo_sct"), gbot("allo_sct"), gcx("cease_allo"), gtop("cease_allo"),
                 act=a("allo_sct"), dim=d("allo_sct") or d("cease_allo"))
    # non_allo → cease_non_allo
    svg += arrow(gcx("non_allo"), gbot("non_allo"), gcx("cease_non_allo"), gtop("cease_non_allo"),
                 act=a("non_allo"), dim=d("non_allo") or d("cease_non_allo"))

    # r_entero_yes → continue_r
    svg += arrow(gcx("r_entero_yes"), gbot("r_entero_yes"),
                 gcx("continue_r"), gtop("continue_r"),
                 act=a("r_entero_yes"), dim=d("r_entero_yes") or d("continue_r"))

    # r_entero_no → target_abx (elbow right)
    bus6 = gbot("r_entero_no") + 16
    svg += poly([(gcx("r_entero_no"), gbot("r_entero_no")),
                 (gcx("r_entero_no"), bus6),
                 (gcx("target_abx"),  bus6),
                 (gcx("target_abx"),  gtop("target_abx"))],
                act=a("r_entero_no"), dim=d("r_entero_no") or d("target_abx"))

    # r_neutro_resolved → target_abx (elbow via bus4)
    svg += poly([(gcx("r_neutro_resolved"), gbot("r_neutro_resolved")),
                 (gcx("r_neutro_resolved"), bus4),
                 (gcx("target_abx"),        bus4),
                 (gcx("target_abx"),        gtop("target_abx"))],
                act=a("r_neutro_resolved"), dim=d("r_neutro_resolved") or d("target_abx"))

    # target_abx → recurrent_fever
    svg += arrow(gcx("target_abx"), gbot("target_abx"),
                 gcx("recurrent_fever"), gtop("recurrent_fever"),
                 act=a("target_abx"), dim=d("target_abx") or d("recurrent_fever"))

    # recurrent_fever → recurrent_box
    svg += arrow(gcx("recurrent_fever"), gbot("recurrent_fever"),
                 gcx("recurrent_box"), gtop("recurrent_box"),
                 act=a("recurrent_fever"), dim=d("recurrent_fever") or d("recurrent_box"))

    # ── LEGEND ────────────────────────────────────────────────────────────
    ly = 700
    legend_items = [
        (C["action_stop"],    C["action_stop"],    C["action_stop_t"],  "Stop / discharge"),
        (C["action_cont"],    C["action_cont"],    C["action_cont_t"],  "Continue empiric"),
        (C["action_target"],  C["action_target"],  C["action_target_t"],"Target antibiotics"),
        (C["action_cease"],   C["action_cease"],   C["action_cease_t"], "Consider ceasing"),
        (C["decision_fill"],  C["decision_stroke"],  "#111",            "Decision / condition"),
        (C["urgent_fill"],    C["urgent_dark"],    "#7B241C",           "Urgent / unstable"),
        (C["recurrent_fill"], C["recurrent_fill"], C["recurrent_text"], "Recurrent fever"),
    ]
    lw, lg = 160, 8
    total_lw = len(legend_items) * (lw + lg)
    lx0 = (W - total_lw) // 2
    for i, (lf, ls, lt, ll) in enumerate(legend_items):
        lx = lx0 + i * (lw + lg)
        svg += node(lx, ly, lw, 24, lf, ls, label=ll, fs=8.5, text_color=lt, sw=1.5, rx=5)

    # Active pathway indicator line
    svg += (f'<rect x="{lx0 + 6*(lw+lg)}" y="{ly}" width="{lw}" height="24" rx="5" '
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
                     "Neutropaenia and fever both resolved — antibiotics can be discontinued."))
    if any(x in AN for x in ("continue_l", "continue_r")):
        recs.append(("💊", "Continue empiric antibiotics",
                     "Clinical situation warrants ongoing broad-spectrum cover."))
    if "p_stable" in AN:
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
                     "Liaise with ID. Consider CT chest ± abdo/pelvis/sinus. "
                     "MRI brain if CNS signs. Consider non-infective causes."))
    if "recurrent_box" in AN:
        recs.append(("🔄", "Recurrent fever",
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
  ctx.scale(sc,sc); ctx.fillStyle='#FAFAFA'; ctx.fillRect(0,0,vb.width,vb.height);
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
      a.href = cv.toDataURL('image/png');
      a.download = 'neutropenic_sepsis_pathway.png';
      a.click();
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

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #F7F9FB; }
[data-testid="stSidebar"] { background: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

st.title("🧬 Neutropaenic Sepsis Management")
st.caption("ADHB Antimicrobial Stewardship — Interactive Decision Support Tool")
st.markdown("---")

col_form, col_chart = st.columns([1, 3.4], gap="large")

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
<html><head><style>body{{margin:0;padding:4px;background:#FAFAFA}}</style></head>
<body>
{COPY_JS}
<div style="overflow-x:auto;margin-top:4px">{svg_str}</div>
</body></html>"""

    components.html(html, height=740, scrolling=True)

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
