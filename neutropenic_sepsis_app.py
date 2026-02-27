"""
Neutropaenic Sepsis Management - Interactive Decision Support Tool
ADHB Antimicrobial Stewardship
"""

import streamlit as st

st.set_page_config(
    page_title="Neutropaenic Sepsis Management",
    page_icon="🧬",
    layout="wide"
)

# ──────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE  (matches original sticker)
# ──────────────────────────────────────────────────────────────────────────────
C = {
    "purple":   "#C39BD3",   # top header
    "yellow":   "#F9E79F",   # clinical decision nodes
    "green":    "#A9DFBF",   # action nodes
    "pink":     "#F1948A",   # warning / clinically unstable
    "blue":     "#85C1E9",   # 72-hr review header
    "white":    "#FFFFFF",
    "grey":     "#D5D8DC",
    "outline":  "#5D6D7E",
    # Active highlight
    "active_stroke": "#E74C3C",
    "active_fill":   "#FADBD8",
    "dim_fill":      "#F2F3F4",
    "dim_stroke":    "#BDC3C7",
    "dim_text":      "#BDC3C7",
}

def make_rect(x, y, w, h, fill, stroke, label, fontsize=11, bold=False,
              active=False, dimmed=False, text_color="#2C3E50", wrap_width=None,
              bullet_lines=None):
    """Return SVG for a rounded rectangle with centred text (or bullet list)."""
    if dimmed:
        fill   = C["dim_fill"]
        stroke = C["dim_stroke"]
        text_color = C["dim_text"]
    if active:
        stroke = C["active_stroke"]
        stroke_w = 3
    else:
        stroke_w = 1.5

    rx = 6
    svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
    svg += f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>\n'

    fw = "bold" if bold else "normal"

    if bullet_lines:
        # render bullet list inside box
        line_h = fontsize + 3
        total_h = len(bullet_lines) * line_h
        start_y = y + (h - total_h) / 2 + fontsize
        for i, line in enumerate(bullet_lines):
            ty = start_y + i * line_h
            svg += (f'<text x="{x+8}" y="{ty}" font-size="{fontsize-1}" '
                    f'fill="{text_color}" font-family="Arial">'
                    f'• {_esc(line)}</text>\n')
    else:
        lines = _wrap(label, wrap_width or w - 10, fontsize)
        line_h = fontsize + 3
        total_h = len(lines) * line_h
        start_y = y + (h - total_h) / 2 + fontsize
        for i, line in enumerate(lines):
            ty = start_y + i * line_h
            svg += (f'<text x="{x + w/2}" y="{ty}" font-size="{fontsize}" '
                    f'font-weight="{fw}" fill="{text_color}" '
                    f'font-family="Arial" text-anchor="middle">'
                    f'{_esc(line)}</text>\n')
    return svg


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _wrap(text, max_px, fontsize):
    """Very rough word-wrap: ~0.55*fontsize px per char."""
    char_w = fontsize * 0.55
    max_chars = max(1, int(max_px / char_w))
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if len(test) <= max_chars:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def arrow(x1, y1, x2, y2, active=False, dimmed=False):
    color = C["active_stroke"] if active else (C["dim_stroke"] if dimmed else C["outline"])
    w = 2 if active else 1
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{w}" marker-end="url(#arr)"/>\n')


def label_line(x1, y1, x2, y2, label, active=False, dimmed=False, lx=None, ly=None):
    svg = arrow(x1, y1, x2, y2, active=active, dimmed=dimmed)
    tc = C["active_stroke"] if active else (C["dim_stroke"] if dimmed else "#555")
    tx = lx if lx is not None else (x1 + x2) / 2
    ty = ly if ly is not None else (y1 + y2) / 2
    svg += f'<text x="{tx}" y="{ty}" font-size="9" fill="{tc}" font-family="Arial" text-anchor="middle">{_esc(label)}</text>\n'
    return svg


# ──────────────────────────────────────────────────────────────────────────────
# PATHWAY LOGIC
# ──────────────────────────────────────────────────────────────────────────────

def determine_pathway(fever, neutropenia, stable, enterocolitis, allo_sct, micro_defined):
    """
    Returns a set of active node IDs that describe the patient's pathway.
    Node IDs are defined in build_svg() below.
    """
    active = {"header", "review72"}

    if fever == "Resolved (afebrile ≥48h & clinically stable)":
        active.add("resolved_fever_hdr")
        active.add("fever_unknown_origin")

        if neutropenia == "Resolved":
            active.add("resolved_neutro_left")
            active.add("stop_antibiotics")
        else:  # ongoing
            active.add("ongoing_neutro_left")
            if enterocolitis:
                active.add("has_entero_left")
                active.add("continue_empiric_left")
            else:
                active.add("no_entero_left")
                if allo_sct:
                    active.add("allo_sct")
                    active.add("consider_ceasing_allo")
                else:
                    active.add("non_allo_sct")
                    active.add("consider_ceasing_nonallo")

    else:  # Persistent / clinically unstable
        active.add("persistent_fever_hdr")

        if micro_defined:
            active.add("micro_defined")
            active.add("liaise_id_micro")
            if neutropenia == "Ongoing":
                active.add("ongoing_neutro_right")
                if enterocolitis:
                    active.add("has_entero_right")
                    active.add("continue_empiric_right")
                else:
                    active.add("no_entero_right")
                    active.add("target_abx")
            else:  # resolved
                active.add("resolved_neutro_right")
                active.add("target_abx")
        else:
            # Clinically defined / fever of unknown origin path on right side
            active.add("fever_unknown_right")
            if stable:
                active.add("clinically_stable_right")
                active.add("continue_empiric_stable")
            else:
                active.add("clinically_unstable_right")
                active.add("unstable_actions")
                active.add("liaise_id_unstable")
                active.add("imaging_box")

        # Recurrent fever always shows on persistent side
        active.add("recurrent_fever")
        active.add("recurrent_unstable")

    return active


# ──────────────────────────────────────────────────────────────────────────────
# SVG BUILDER
# ──────────────────────────────────────────────────────────────────────────────

def build_svg(active_nodes: set) -> str:

    def a(node_id):
        return node_id in active_nodes

    def d(node_id):
        # dimmed if nothing in the diagram is selected (initial state) → never dim
        # dim if active set is non-trivial and this node NOT active
        if len(active_nodes) <= 2:
            return False  # don't dim anything on first load
        return node_id not in active_nodes

    W, H = 980, 720
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'

    # Arrow marker
    svg += """<defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#5D6D7E"/>
  </marker>
  <marker id="arr_active" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#E74C3C"/>
  </marker>
</defs>\n"""

    # ── ROW 0: Main header ─────────────────────────────────────────────────
    svg += make_rect(340, 5, 300, 34, C["purple"], C["outline"],
                     "Neutropaenic Sepsis Management", fontsize=13, bold=True,
                     active=a("header"), dimmed=False)

    # ── ROW 1: 72hr review ────────────────────────────────────────────────
    svg += make_rect(330, 48, 320, 28, C["blue"], C["outline"],
                     "Review at 72 hours empiric antibiotics", fontsize=10,
                     active=a("review72"), dimmed=False)

    # Arrow from header → review
    svg += arrow(490, 39, 490, 48)

    # Branch lines from review72
    svg += arrow(490, 76, 490, 95)      # centre down to fever split
    svg += arrow(490, 76, 175, 76)      # left to resolved
    svg += arrow(175, 76, 175, 95)
    svg += arrow(490, 76, 805, 76)      # right to persistent
    svg += arrow(805, 76, 805, 95)

    # ── ROW 2: Left / Right top headers ───────────────────────────────────
    svg += make_rect(50, 95, 250, 36, C["yellow"], C["outline"],
                     "Resolved fever: Afebrile ≥48h & clinically stable",
                     fontsize=10, active=a("resolved_fever_hdr"), dimmed=d("resolved_fever_hdr"))

    svg += make_rect(680, 95, 250, 36, C["pink"], C["outline"],
                     "Persistent fever or remains clinically unstable",
                     fontsize=10, active=a("persistent_fever_hdr"), dimmed=d("persistent_fever_hdr"))

    # ── ROW 3: Second-level splits ────────────────────────────────────────
    # Left side: Fever of unknown origin  |  Micro defined
    svg += make_rect(30, 155, 160, 30, C["yellow"], C["outline"],
                     "Fever of unknown origin", fontsize=9,
                     active=a("fever_unknown_origin"), dimmed=d("fever_unknown_origin"))

    svg += make_rect(330, 148, 160, 44, C["yellow"], C["outline"],
                     "Microbiologically or clinically defined infection",
                     fontsize=9, active=a("micro_defined"), dimmed=d("micro_defined"))

    # Arrow resolved_fever → fever_unknown_origin
    svg += arrow(175, 131, 175, 155)
    svg += arrow(175, 155, 110, 155)

    # Arrow resolved_fever → micro_defined (centre path)
    svg += arrow(490, 131, 490, 148)
    svg += arrow(490, 148, 410, 148)

    # Right side: Clinically stable | Clinically unstable
    svg += make_rect(630, 148, 120, 44, C["yellow"], C["outline"],
                     "Clinically stable", fontsize=9,
                     active=a("clinically_stable_right"), dimmed=d("clinically_stable_right"))

    svg += make_rect(765, 140, 170, 52, C["pink"], C["outline"],
                     "Clinically unstable",
                     fontsize=9, bold=True,
                     bullet_lines=["Consider aminoglycoside", "Liaise with ID about MRO", "Repeat periph & central cultures"],
                     active=a("clinically_unstable_right"), dimmed=d("clinically_unstable_right"))

    # Arrow persistent → clinically stable / unstable
    svg += arrow(805, 131, 805, 155)
    svg += arrow(805, 155, 750, 155)
    svg += arrow(805, 155, 850, 155)

    # ── Liaise with ID (dashed style – we'll do solid but different colour)
    svg += make_rect(330, 210, 160, 28, C["white"], C["outline"],
                     "Liaise with ID", fontsize=9, bold=True,
                     active=a("liaise_id_micro"), dimmed=d("liaise_id_micro"))

    svg += arrow(410, 192, 410, 210)

    # ── ROW 4: Neutropenia status ─────────────────────────────────────────
    # Left side
    svg += make_rect(5, 220, 100, 30, C["yellow"], C["outline"],
                     "Resolved neutropaenia", fontsize=8,
                     active=a("resolved_neutro_left"), dimmed=d("resolved_neutro_left"))

    svg += make_rect(115, 220, 100, 30, C["yellow"], C["outline"],
                     "Ongoing neutropaenia", fontsize=8,
                     active=a("ongoing_neutro_left"), dimmed=d("ongoing_neutro_left"))

    svg += arrow(110, 185, 110, 220)
    svg += arrow(110, 220, 55, 220)
    svg += arrow(110, 220, 165, 220)

    # Right side (micro-defined path)
    svg += make_rect(255, 256, 110, 30, C["yellow"], C["outline"],
                     "Ongoing neutropaenia", fontsize=8,
                     active=a("ongoing_neutro_right"), dimmed=d("ongoing_neutro_right"))

    svg += make_rect(375, 256, 110, 30, C["yellow"], C["outline"],
                     "Resolved neutropaenia", fontsize=8,
                     active=a("resolved_neutro_right"), dimmed=d("resolved_neutro_right"))

    svg += arrow(410, 238, 410, 256)
    svg += arrow(410, 256, 310, 256)
    svg += arrow(410, 256, 430, 256)

    # ── ROW 5: Enterocolitis / mucositis ─────────────────────────────────
    # Left - resolved neutro → stop abx
    svg += make_rect(5, 270, 100, 30, C["green"], C["outline"],
                     "Stop antibiotics", fontsize=9, bold=True,
                     active=a("stop_antibiotics"), dimmed=d("stop_antibiotics"))
    svg += arrow(55, 250, 55, 270)

    # Left - ongoing neutro → enterocolitis split
    svg += make_rect(90, 270, 80, 28, C["yellow"], C["outline"],
                     "Has enterocolitis or mucositis", fontsize=7.5,
                     active=a("has_entero_left"), dimmed=d("has_entero_left"))

    svg += make_rect(180, 270, 80, 28, C["yellow"], C["outline"],
                     "No enterocolitis or mucositis", fontsize=7.5,
                     active=a("no_entero_left"), dimmed=d("no_entero_left"))

    svg += arrow(165, 250, 165, 270)
    svg += arrow(165, 270, 130, 270)
    svg += arrow(165, 270, 220, 270)

    # Right (micro defined) - ongoing → enterocolitis
    svg += make_rect(225, 304, 90, 28, C["yellow"], C["outline"],
                     "Has enterocolitis or mucositis", fontsize=7.5,
                     active=a("has_entero_right"), dimmed=d("has_entero_right"))

    svg += make_rect(325, 304, 90, 28, C["yellow"], C["outline"],
                     "No enterocolitis or mucositis", fontsize=7.5,
                     active=a("no_entero_right"), dimmed=d("no_entero_right"))

    svg += arrow(310, 286, 310, 304)
    svg += arrow(310, 304, 270, 304)
    svg += arrow(310, 304, 370, 304)

    # ── ROW 6: SCT split (left, no enterocolitis path) ───────────────────
    svg += make_rect(160, 320, 80, 28, C["yellow"], C["outline"],
                     "Allo-SCT patient", fontsize=8,
                     active=a("allo_sct"), dimmed=d("allo_sct"))

    svg += make_rect(250, 320, 80, 28, C["yellow"], C["outline"],
                     "Non-allo-SCT patient", fontsize=8,
                     active=a("non_allo_sct"), dimmed=d("non_allo_sct"))

    svg += arrow(220, 298, 220, 320)
    svg += arrow(220, 320, 200, 320)
    svg += arrow(220, 320, 290, 320)

    # ── ROW 7: Action nodes ───────────────────────────────────────────────
    # Continue empiric (left, has entero)
    svg += make_rect(65, 320, 90, 28, C["green"], C["outline"],
                     "Continue empiric antibiotics", fontsize=8, bold=True,
                     active=a("continue_empiric_left"), dimmed=d("continue_empiric_left"))
    svg += arrow(130, 298, 110, 320)

    # Consider ceasing (allo)
    svg += make_rect(140, 366, 100, 40, C["yellow"], C["outline"],
                     "Consider ceasing empiric antibiotics if another cause found",
                     fontsize=7.5, active=a("consider_ceasing_allo"), dimmed=d("consider_ceasing_allo"))
    svg += arrow(200, 348, 190, 366)

    # Consider ceasing (non-allo)
    svg += make_rect(248, 366, 100, 40, C["yellow"], C["outline"],
                     "Consider ceasing empiric antibiotics",
                     fontsize=7.5, active=a("consider_ceasing_nonallo"), dimmed=d("consider_ceasing_nonallo"))
    svg += arrow(290, 348, 298, 366)

    # Continue empiric (right, has entero)
    svg += make_rect(200, 350, 110, 28, C["green"], C["outline"],
                     "Continue empiric antibiotics", fontsize=8, bold=True,
                     active=a("continue_empiric_right"), dimmed=d("continue_empiric_right"))
    svg += arrow(270, 332, 255, 350)

    # Target antibiotics
    svg += make_rect(330, 350, 110, 28, C["green"], C["outline"],
                     "Target antibiotics", fontsize=9, bold=True,
                     active=a("target_abx"), dimmed=d("target_abx"))
    svg += arrow(370, 332, 385, 350)
    svg += arrow(430, 286, 430, 378)   # resolved neutro right → target
    svg += arrow(430, 378, 440, 378)

    # ── RIGHT SIDE: Clinically stable → continue empiric ─────────────────
    svg += make_rect(600, 210, 150, 28, C["green"], C["outline"],
                     "Continue empiric therapy", fontsize=9, bold=True,
                     active=a("continue_empiric_stable"), dimmed=d("continue_empiric_stable"))
    svg += arrow(690, 192, 675, 210)

    # ── RIGHT SIDE: Clinically unstable actions ───────────────────────────
    svg += make_rect(750, 210, 190, 60, C["pink"], C["outline"],
                     "", fontsize=8,
                     bullet_lines=["Liaise with ID", "Consider CT chest +/- abdo/pelvis/sinus", "MRI brain if CNS signs", "Consider non-infective causes"],
                     active=a("liaise_id_unstable"), dimmed=d("liaise_id_unstable"))
    svg += arrow(850, 192, 845, 210)

    # ── RECURRENT FEVER ───────────────────────────────────────────────────
    svg += make_rect(560, 290, 130, 28, C["purple"], C["outline"],
                     "Recurrent fever", fontsize=10, bold=True,
                     active=a("recurrent_fever"), dimmed=d("recurrent_fever"))

    svg += make_rect(530, 336, 190, 68, C["pink"], C["outline"],
                     "", fontsize=8,
                     bullet_lines=["Restart empiric abx & consider aminoglycoside", "Liaise with ID about MRO coverage", "Repeat periph & central cultures"],
                     active=a("recurrent_unstable"), dimmed=d("recurrent_unstable"))

    svg += arrow(625, 318, 625, 336)

    # ── IMAGING BOX ───────────────────────────────────────────────────────
    svg += make_rect(750, 280, 190, 60, C["yellow"], C["outline"],
                     "", fontsize=8,
                     bullet_lines=["Liaise with ID", "CT chest +/- abdo/pelvis guided by Sx", "MRI brain if CNS signs/Sx", "Consider non-infective causes"],
                     active=a("imaging_box"), dimmed=d("imaging_box"))

    # Legend
    svg += make_rect(10, 650, 120, 20, C["green"], C["outline"], "Action / recommendation", fontsize=8)
    svg += make_rect(140, 650, 120, 20, C["yellow"], C["outline"], "Clinical decision point", fontsize=8)
    svg += make_rect(270, 650, 120, 20, C["pink"], C["outline"], "Urgent / unstable pathway", fontsize=8)
    svg += f'<rect x="400" y="650" width="20" height="20" rx="3" fill="{C["dim_fill"]}" stroke="{C["active_stroke"]}" stroke-width="2"/>'
    svg += f'<text x="425" y="664" font-size="8" fill="#555" font-family="Arial">Active pathway</text>'

    svg += "</svg>\n"
    return svg


# ──────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION TEXT
# ──────────────────────────────────────────────────────────────────────────────

def get_recommendation(active_nodes):
    recs = []
    if "stop_antibiotics" in active_nodes:
        recs.append("✅ **Stop antibiotics** — neutropaenia has resolved and fever has resolved.")
    if "continue_empiric_left" in active_nodes or "continue_empiric_right" in active_nodes or "continue_empiric_stable" in active_nodes:
        recs.append("💊 **Continue empiric antibiotics** — clinical situation warrants ongoing broad cover.")
    if "consider_ceasing_allo" in active_nodes:
        recs.append("⚠️ **Consider ceasing empiric antibiotics if another cause is found** (Allo-SCT patient).")
    if "consider_ceasing_nonallo" in active_nodes:
        recs.append("⚠️ **Consider ceasing empiric antibiotics** (Non-allo-SCT patient).")
    if "target_abx" in active_nodes:
        recs.append("🎯 **Target antibiotics** to the identified pathogen/source.")
    if "clinically_unstable_right" in active_nodes:
        recs.append("🚨 **Clinically unstable with persistent fever:**\n"
                    "- Consider aminoglycoside\n"
                    "- Liaise with ID regarding MRO coverage\n"
                    "- Repeat peripheral and central cultures")
    if "liaise_id_unstable" in active_nodes:
        recs.append("🖥️ **Imaging:** Consider CT chest ± abdo/pelvis/sinus guided by symptoms. MRI brain if CNS signs/symptoms. Consider non-infective causes.")
    if "recurrent_fever" in active_nodes:
        recs.append("🔄 **Recurrent fever — clinically unstable:**\n"
                    "- Restart empiric antibiotics and consider aminoglycoside\n"
                    "- Liaise with ID about MRO coverage\n"
                    "- Repeat peripheral and central cultures")
    return recs


# ──────────────────────────────────────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────────────────────────────────────

st.title("🧬 Neutropaenic Sepsis Management")
st.caption("ADHB Antimicrobial Stewardship — Interactive Decision Support")

st.markdown("---")

col_form, col_chart = st.columns([1, 2.2], gap="large")

with col_form:
    st.subheader("Patient Parameters")

    fever = st.radio(
        "**Fever status at 72-hour review**",
        options=[
            "Resolved (afebrile ≥48h & clinically stable)",
            "Persistent / clinically unstable"
        ],
        index=0
    )

    neutropenia = st.radio(
        "**Neutropaenia status**",
        options=["Resolved", "Ongoing"],
        index=1
    )

    micro_defined = st.checkbox(
        "**Microbiologically or clinically defined infection identified**",
        value=False
    )

    stable = st.radio(
        "**Clinical stability**",
        options=["Clinically stable", "Clinically unstable"],
        index=0,
        disabled=(fever == "Resolved (afebrile ≥48h & clinically stable)" or micro_defined)
    )

    enterocolitis = st.checkbox(
        "**Enterocolitis or significant mucositis present**",
        value=False,
        disabled=(neutropenia == "Resolved" and not micro_defined)
    )

    allo_sct = st.checkbox(
        "**Allo-SCT patient**",
        value=False,
        disabled=(enterocolitis or neutropenia == "Resolved")
    )

    st.markdown("---")
    st.caption("ℹ️ All antibiotic decisions should be made in consultation with your clinical team and the Infectious Diseases service as appropriate.")

with col_chart:
    st.subheader("Pathway Flowchart")

    # Determine active nodes
    active = determine_pathway(
        fever=fever,
        neutropenia=neutropenia,
        stable=(stable == "Clinically stable"),
        enterocolitis=enterocolitis,
        allo_sct=allo_sct,
        micro_defined=micro_defined
    )

    svg = build_svg(active)
    st.components.v1.html(f"<div style='overflow-x:auto'>{svg}</div>", height=730, scrolling=True)

# Recommendations
st.markdown("---")
st.subheader("📋 Recommended Actions")

recs = get_recommendation(active)
if recs:
    for r in recs:
        st.markdown(r)
else:
    st.info("Complete the patient parameters on the left to see tailored recommendations.")

st.markdown("---")
st.caption("Based on ADHB Neutropaenic Sepsis Management Guidelines. Not a substitute for clinical judgement.")
