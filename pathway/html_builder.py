_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:          #F7F3EE;
  --bg-left:     #EBF4FB;
  --bg-mid:      #EBF5F0;
  --bg-right:    #FEF3EB;
  --purple:      #4A3A8C;
  --red-hdr:     #8B2727;
  --teal-hdr:    #1F6E58;
  --blue-hdr:    #2354A0;
  --teal:        #2BBBAD;
  --teal-dk:     #0F7A62;
  --red-no:      #E03030;
  --q-bg:        #E4F1F9;
  --q-border:    #7BB8D4;
  --q-text:      #163344;
  --dash-bg:     #EAF8F3;
  --dash-border: #2BBBAD;
  --stop:        #219150;
  --cont:        #1D5FA8;
  --target:      #0F7A62;
  --cease-bg:    #FFF8DC;
  --cease-bdr:   #C49A00;
  --cease-text:  #7A5E00;
  --urg-bg:      #FCDFDA;
  --urg-bdr:     #C0392B;
  --urg-text:    #7B1A1A;
  --rec:         #7D3C98;
  --rec-bg:      #F8EAFF;
  --rec-bdr:     #A355C8;
  --dim-bg:      #F0F0F0;
  --dim-bdr:     #D0D0D0;
  --dim-text:    #BBBBBB;
  --arrow:       #2C3E50;
  --act-arrow:   #0F7A62;
  --shadow:      0 2px 8px rgba(0,0,0,0.09);
  --shadow-act:  0 3px 14px rgba(15,122,98,0.22);
  --font:        'Nunito', 'Segoe UI', sans-serif;
}
 
body { font-family: var(--font); background: var(--bg); padding: 10px 12px 16px; }
 
.infographic { max-width: 1400px; margin: 0 auto; }
 
/* ── HEADER PILLS ── */
.hdr-title {
  background: var(--purple); color: #fff;
  text-align: center; font-size: 17px; font-weight: 800;
  padding: 11px 36px; border-radius: 50px;
  display: block; width: fit-content; margin: 0 auto 8px;
  box-shadow: var(--shadow); letter-spacing: 0.01em;
}
.hdr-review {
  background: var(--blue-hdr); color: #fff;
  text-align: center; font-size: 12px; font-weight: 700;
  padding: 8px 44px; border-radius: 50px;
  display: block; width: fit-content; margin: 0 auto 10px;
  box-shadow: var(--shadow);
}
 
/* ── THREE COLUMN GRID ── */
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
 
/* ── SECTION PANELS ── */
.section-panel {
  border-radius: 18px; padding: 10px 10px 14px;
  display: flex; flex-direction: column; align-items: center;
}
.panel-left  { background: var(--bg-left); }
.panel-mid   { background: var(--bg-mid); }
.panel-right { background: var(--bg-right); }
.panel-dim   { background: var(--dim-bg); }
 
/* ── SECTION HEADERS ── */
.section-hdr {
  color: #fff; font-size: 11px; font-weight: 800;
  padding: 8px 12px; border-radius: 11px; text-align: center;
  width: 100%; margin-bottom: 7px; box-shadow: var(--shadow); line-height: 1.4;
}
.hdr-resolved   { background: var(--purple); }
.hdr-micro      { background: var(--teal-hdr); }
.hdr-persistent { background: var(--red-hdr); }
 
/* ── QUESTION CARD ── */
.q-card {
  background: var(--q-bg); border: 1.5px solid var(--q-border);
  border-radius: 12px; padding: 7px 10px;
  font-size: 10.5px; font-weight: 600; color: var(--q-text);
  text-align: center; line-height: 1.4; width: 100%;
  box-shadow: var(--shadow);
}
.q-card .sub {
  font-size: 9px; font-weight: 600; color: #5A7A8A;
  margin-top: 3px; font-style: italic; display: block;
}
.q-card.dashed {
  background: var(--dash-bg);
  border: 1.5px dashed var(--dash-border);
}
.q-card.urgent {
  background: var(--urg-bg); border: 1.5px solid var(--urg-bdr);
  color: var(--urg-text); text-align: left;
}
.q-card.urgent ul { margin: 4px 0 0 14px; font-size: 10px; }
.q-card.active {
  outline: 2.5px solid var(--teal); outline-offset: 2px;
  box-shadow: var(--shadow-act);
}
.q-card.dimmed {
  background: var(--dim-bg) !important; border-color: var(--dim-bdr) !important;
  color: var(--dim-text) !important; box-shadow: none;
}
.q-card.dimmed .sub,
.q-card.dimmed li { color: var(--dim-text) !important; }
 
/* ── YES/NO BADGE ROW ── */
.yn-row {
  display: flex; justify-content: space-around; width: 100%;
  align-items: center; margin: 3px 0; position: relative;
}
.yn-row::before {
  content: ''; position: absolute;
  top: 12px; left: 14%; right: 14%;
  height: 2px; background: var(--arrow); z-index: 0;
}
.yn-row.dim::before { background: var(--dim-bdr); }
 
.badge-wrap { display: flex; flex-direction: column; align-items: center; gap: 2px; z-index: 1; }
 
.badge {
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 900; color: #fff;
  box-shadow: 0 1px 5px rgba(0,0,0,0.18); flex-shrink: 0;
}
.badge.yes { background: var(--teal); }
.badge.no  { background: var(--red-no); }
.badge.badge-active {
  box-shadow: 0 0 0 3px rgba(43,187,173,0.35), 0 1px 5px rgba(0,0,0,0.18);
}
.badge.badge-dimmed { background: var(--dim-bdr) !important; color: var(--dim-text); box-shadow: none; }
 
.badge-lbl { font-size: 9px; font-weight: 700; color: #5A6A7A; }
.badge-lbl.active { color: var(--teal-dk); }
.badge-lbl.dimmed { color: var(--dim-text); }
 
/* ── CONNECTOR ARROW ── */
.connector { display: flex; justify-content: center; width: 100%; margin: 1px 0; }
 
/* ── TWO-COLUMN sub-layouts ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; width: 100%; }
 
/* ── ACTION / TERMINAL NODES ── */
.action-node {
  width: 100%; padding: 9px 10px; border-radius: 12px;
  text-align: center; font-size: 10.5px; font-weight: 800;
  line-height: 1.3; box-shadow: var(--shadow);
}
.action-node.stop   { background: var(--stop);   color: #fff; }
.action-node.cont   { background: var(--cont);   color: #fff; }
.action-node.target { background: var(--target); color: #fff; }
.action-node.cease  {
  background: var(--cease-bg); color: var(--cease-text);
  border: 1.5px solid var(--cease-bdr);
}
.action-node.active {
  outline: 2.5px solid var(--teal); outline-offset: 2px; box-shadow: var(--shadow-act);
}
.action-node.dimmed {
  background: var(--dim-bg) !important; color: var(--dim-text) !important;
  border-color: var(--dim-bdr) !important; box-shadow: none;
}
 
/* ── RECURRENT FEVER ── */
.rec-hdr {
  background: var(--rec); color: #fff;
  font-size: 11px; font-weight: 800; text-align: center;
  padding: 8px 12px; border-radius: 50px; width: 100%; box-shadow: var(--shadow);
}
.rec-hdr.active { outline: 2.5px solid var(--teal); outline-offset: 2px; box-shadow: var(--shadow-act); }
.rec-hdr.dimmed { background: var(--dim-bg) !important; color: var(--dim-text) !important; box-shadow: none; }
 
.rec-box {
  background: var(--rec-bg); border: 1.5px solid var(--rec-bdr);
  border-radius: 12px; padding: 9px 12px;
  font-size: 10px; color: #4A1A60; line-height: 1.5; width: 100%;
}
.rec-box ul { margin-left: 14px; }
.rec-box.active { outline: 2.5px solid var(--teal); outline-offset: 2px; box-shadow: var(--shadow-act); }
.rec-box.dimmed {
  background: var(--dim-bg) !important; border-color: var(--dim-bdr) !important;
  color: var(--dim-text) !important;
}
 
/* ── BULLET INFO CARD ── */
.bullet-card {
  background: var(--q-bg); border: 1.5px solid var(--q-border);
  border-radius: 12px; padding: 9px 12px;
  font-size: 10px; color: var(--q-text); line-height: 1.5; width: 100%;
}
.bullet-card ul { margin: 4px 0 0 14px; }
.bullet-card.active { outline: 2.5px solid var(--teal); outline-offset: 2px; box-shadow: var(--shadow-act); }
.bullet-card.dimmed {
  background: var(--dim-bg) !important; border-color: var(--dim-bdr) !important;
  color: var(--dim-text) !important;
}
 
/* ── LEGEND ── */
.legend {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 8px; margin-top: 16px; padding-top: 12px; border-top: 1px solid #DDD;
}
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 9.5px; font-weight: 700; color: #3A4A5A; }
.legend-swatch { width: 26px; height: 15px; border-radius: 5px; flex-shrink: 0; }
 
/* ── CONVERGENCE BAR ── */
.converge-wrap { width: 100%; display: flex; justify-content: center; margin: 0; }
 
/* ── FOOTER ── */
.footer { text-align: right; font-size: 9px; color: #8A9AA8; margin-top: 8px; font-style: italic; }
 
/* ── UTILITIES ── */
.w100 { width: 100%; }
.mt4  { margin-top: 4px; }
.col  { display: flex; flex-direction: column; align-items: center; width: 100%; }
</style>
"""
 
 
def _node_cls(node_id, AN):
    """Return 'active', 'dimmed', or '' based on pathway state."""
    if node_id in AN:
        return "active"
    if len(AN) > 2:
        return "dimmed"
    return ""
 
 
def _badge_html(is_yes, state):
    kind = "yes" if is_yes else "no"
    sym  = "\u2713"  if is_yes else "\u2715"
    extra = f" badge-{state}" if state else ""
    return f'<div class="badge {kind}{extra}">{sym}</div>'
 
 
def _yn_row(yes_id, no_id, AN, yes_lbl="Yes", no_lbl="No"):
    sy = _node_cls(yes_id, AN)
    sn = _node_cls(no_id, AN)
    dim_line = " dim" if (sy == "dimmed" and sn == "dimmed") else ""
    return f"""<div class="yn-row{dim_line}">
        <div class="badge-wrap">{_badge_html(True, sy)}<span class="badge-lbl {sy}">{yes_lbl}</span></div>
        <div class="badge-wrap">{_badge_html(False, sn)}<span class="badge-lbl {sn}">{no_lbl}</span></div>
      </div>"""
 
 
def _arrow_svg(from_id, to_id, AN):
    """Coloured connector arrow: teal if both active, grey if dimmed, dark otherwise."""
    both_active = from_id in AN and to_id in AN
    either_dim  = len(AN) > 2 and not both_active
    clr = "#0F7A62" if both_active else ("#CCCCCC" if either_dim else "#2C3E50")
    sw  = "2.5" if both_active else "2.2"
    return f"""<div class="connector">
        <svg width="20" height="20" viewBox="0 0 20 20">
          <line x1="10" y1="0" x2="10" y2="11" stroke="{clr}" stroke-width="{sw}"/>
          <polygon points="10,20 3,9 17,9" fill="{clr}"/>
        </svg></div>"""
 
 
def build_html(AN, auto_copy=False):
    def c(nid):                    return _node_cls(nid, AN)
    def arr(fid, tid):             return _arrow_svg(fid, tid, AN)
    def yn(yes_id, no_id, yl, nl): return _yn_row(yes_id, no_id, AN, yl, nl)
 
    def qcard(nid, text, extra="", sub="", fs=""):
        s = f' style="font-size:{fs};"' if fs else ""
        sub_h = f'<span class="sub">{sub}</span>' if sub else ""
        return f'<div class="q-card {extra} {c(nid)}"{s}>{text}{sub_h}</div>'
 
    def action(nid, kind, text, fs=""):
        s = f' style="font-size:{fs};"' if fs else ""
        return f'<div class="action-node {kind} {c(nid)}"{s}>{text}</div>'
 
    # Panel tint: dim entire column when its path is not active
    left_dim  = len(AN) > 2 and "fever_unknown"    not in AN
    mid_dim   = len(AN) > 2 and "micro_defined"    not in AN
    right_dim = len(AN) > 2 and "persistent_fever" not in AN
 
    lp = "panel-dim" if left_dim  else "panel-left"
    mp = "panel-dim" if mid_dim   else "panel-mid"
    rp = "panel-dim" if right_dim else "panel-right"
 
    # Label colours for top split text
    lc = "#BBBBBB" if left_dim  else "#5A6A7A"
    rc = "#BBBBBB" if right_dim else "#5A6A7A"
 
    def routing_row(yes_lbl, no_lbl):
        """Top routing yn-row in the left column.
        Only the YES (left/No-source) badge can be active \u2014 when fever_unknown path is taken.
        The NO badge (Defined \u2192 mid column) is NEVER active; it points to another column.
        Panel tint already communicates which column is live."""
        if len(AN) <= 2:
            sy = sn = ""          # nothing selected: all neutral
        elif "fever_unknown" in AN:
            sy = "active"         # left path chosen: yes badge active
            sn = "dimmed"
        else:
            sy = "dimmed"         # mid or right path chosen: left panel dimmed throughout
            sn = "dimmed"
        dim_line = " dim" if sy == "dimmed" else ""
        return f"""<div class="yn-row{dim_line}">
          <div class="badge-wrap">{_badge_html(True, sy)}<span class="badge-lbl {sy}">{yes_lbl}</span></div>
          <div class="badge-wrap">{_badge_html(False, sn)}<span class="badge-lbl {sn}">{no_lbl}</span></div>
        </div>"""

    auto_copy_js = "setTimeout(copyDiagram, 400);" if auto_copy else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
{_CSS}</head>
<body>
<div style="text-align:left;margin-bottom:8px;">
  <button id="copyBtn" onclick="copyDiagram()" style="
    font-family:var(--font);font-size:12px;font-weight:700;
    padding:9px 22px;border-radius:50px;border:none;cursor:pointer;
    background:#2BBBAD;color:#fff;box-shadow:var(--shadow);
    transition:background 0.2s;">&#128203; Copy diagram to clipboard</button>
</div>
<div class="infographic">

 
  <!-- ── TITLE + REVIEW BAR ── -->
  <span class="hdr-title">\U0001f9ec Neutropaenic Sepsis Management</span>
  {arr("header", "review72")}
  <span class="hdr-review">Review at 72 hours \u2014 empiric antibiotics</span>
 
  <!-- Top split bus -->
  <div style="display:flex;justify-content:center;width:100%;position:relative;margin-bottom:3px;">
    <svg width="100%" height="26" viewBox="0 0 900 26" preserveAspectRatio="none"
         style="position:absolute;top:0;left:0;pointer-events:none;">
      <line x1="450" y1="0"  x2="450" y2="9"  stroke="#2C3E50" stroke-width="2.2"/>
      <line x1="160" y1="9"  x2="740" y2="9"  stroke="#2C3E50" stroke-width="2.2"/>
      <line x1="160" y1="9"  x2="160" y2="26" stroke="#2C3E50" stroke-width="2.2"/>
      <line x1="450" y1="9"  x2="450" y2="26" stroke="#2C3E50" stroke-width="2.2"/>
      <line x1="740" y1="9"  x2="740" y2="26" stroke="#2C3E50" stroke-width="2.2"/>
    </svg>
    <div style="width:33%;text-align:center;padding-top:15px;">
      <span style="font-size:9.5px;font-weight:700;color:{lc};">Fever resolved</span></div>
    <div style="width:34%"></div>
    <div style="width:33%;text-align:center;padding-top:15px;">
      <span style="font-size:9.5px;font-weight:700;color:{rc};">Persistent fever</span></div>
  </div>
 
  <!-- ── THREE COLUMNS ── -->
  <div class="three-col">
 
    <!-- LEFT: Fever unknown path -->
    <div class="section-panel {lp} col">
      <div class="section-hdr hdr-resolved">Resolved fever: Afebrile &gt;48 h &amp; clinically stable</div>
 
      {routing_row(yes_lbl="No source", no_lbl="Defined")}
      {qcard("fever_unknown", "Fever of unknown origin")}
      {arr("fever_unknown", "l_neutro_resolved")}
      {yn("l_neutro_resolved", "l_neutro_ongoing", "Resolved", "Ongoing")}
 
      <div class="two-col mt4">
 
        <div class="col">
          {qcard("l_neutro_resolved", "Resolved neutropaenia", fs="9.5px")}
          {arr("l_neutro_resolved", "stop_abx")}
          {action("stop_abx", "stop", "Stop antibiotics")}
        </div>
 
        <div class="col">
          {qcard("l_neutro_ongoing", "Ongoing neutropaenia", fs="9.5px")}
          {arr("l_neutro_ongoing", "l_entero_yes")}
          {yn("l_entero_yes", "l_entero_no", "Entero", "No entero")}
          <div class="two-col mt4">
 
            <div class="col">
              {qcard("l_entero_yes", "Has enterocolitis or mucositis", fs="9px")}
              {arr("l_entero_yes", "continue_l")}
              {action("continue_l", "cont", "Continue empiric antibiotics", fs="9.5px")}
            </div>
 
            <div class="col">
              {qcard("l_entero_no", "No enterocolitis or mucositis", fs="9px")}
              {arr("l_entero_no", "allo_sct")}
              {yn("allo_sct", "non_allo", "Allo-SCT", "Non-allo")}
              <div class="two-col mt4">
                <div class="col">
                  {action("cease_allo", "cease",
                          "Consider ceasing if another cause found", fs="9px")}
                </div>
                <div class="col">
                  {action("cease_non_allo", "cease",
                          "Consider ceasing empiric antibiotics", fs="9px")}
                </div>
              </div>
            </div>
 
          </div>
        </div>
 
      </div>
    </div><!-- /left -->
 
 
    <!-- MIDDLE: Micro-defined path -->
    <div class="section-panel {mp} col">
      <div class="section-hdr hdr-micro">Microbiologically / clinically defined infection</div>
 
      {qcard("liaise_id", "Liaise with ID", extra="dashed")}
      {arr("liaise_id", "r_neutro_ongoing")}
      {yn("r_neutro_ongoing", "r_neutro_resolved", "Ongoing", "Resolved")}
 
      <div class="two-col mt4">
 
        <div class="col">
          {qcard("r_neutro_ongoing", "Ongoing neutropaenia", fs="9.5px")}
          {arr("r_neutro_ongoing", "r_entero_yes")}
          {yn("r_entero_yes", "r_entero_no", "Entero", "No entero")}
          <div class="two-col mt4">
            <div class="col">
              {qcard("r_entero_yes", "Has enterocolitis or mucositis", fs="9px")}
              {arr("r_entero_yes", "continue_r")}
              {action("continue_r", "cont", "Continue empiric antibiotics", fs="9.5px")}
            </div>
            <div class="col">
              {qcard("r_entero_no", "No enterocolitis or mucositis", fs="9px")}
              {arr("r_entero_no", "target_abx_o")}
              {action("target_abx_o", "target", "Target antibiotics", fs="9.5px")}
              {arr("target_abx_o", "recurrent_fever_o")}
              <div class="rec-hdr {c('recurrent_fever_o')}">Recurrent fever</div>
              {arr("recurrent_fever_o", "recurrent_box_o")}
              <div class="rec-box {c('recurrent_box_o')}"><ul>
                <li>Clinically unstable</li>
                <li>Restart empiric abx + aminoglycoside</li>
                <li>Liaise with ID re MRO</li>
                <li>Repeat peripheral &amp; central cultures</li>
              </ul></div>
            </div>
          </div>
        </div>
 
        <div class="col">
          {qcard("r_neutro_resolved", "Resolved neutropaenia", fs="9.5px")}
          {arr("r_neutro_resolved", "target_abx_r")}
          {action("target_abx_r", "target", "Target antibiotics")}
          {arr("target_abx_r", "recurrent_fever_r")}
          <div class="rec-hdr {c('recurrent_fever_r')}">Recurrent fever</div>
          {arr("recurrent_fever_r", "recurrent_box_r")}
          <div class="rec-box {c('recurrent_box_r')}"><ul>
            <li>Clinically unstable</li>
            <li>Restart empiric abx + aminoglycoside</li>
            <li>Liaise with ID re MRO</li>
            <li>Repeat peripheral &amp; central cultures</li>
          </ul></div>
        </div>
 
      </div>
    </div><!-- /mid -->
 
 
    <!-- RIGHT: Persistent fever path -->
    <div class="section-panel {rp} col">
      <div class="section-hdr hdr-persistent">Persistent fever or remains clinically unstable</div>
 
      {yn("p_stable", "p_unstable", "Stable", "Unstable")}
 
      <div class="two-col mt4">
 
        <div class="col">
          {qcard("p_stable", "Clinically stable", sub="Continue empiric therapy")}
          {arr("p_stable", "p_cont")}
          {action("p_cont", "cont", "Continue empiric antibiotics")}
        </div>
 
        <div class="col">
          <div class="q-card urgent {c('p_unstable')}">
            <strong>Clinically unstable:</strong>
            <ul>
              <li>Consider aminoglycoside</li>
              <li>Liaise with ID re MRO</li>
              <li>Repeat peripheral &amp; central cultures</li>
            </ul>
          </div>
          {arr("p_unstable", "imaging_box")}
          <div class="bullet-card {c('imaging_box')}">
            <strong style="font-size:10px;">Consider investigation:</strong>
            <ul>
              <li>Liaise with ID</li>
              <li>CT chest &#177; abdo/pelvis/sinus</li>
              <li>MRI brain if CNS signs</li>
              <li>Non-infective causes</li>
            </ul>
          </div>
        </div>
 
      </div>
    </div><!-- /right -->
 
  </div><!-- /three-col -->
 
  <!-- LEGEND -->
  <div class="legend">
    <div class="legend-item">
      <div class="legend-swatch" style="background:#219150;"></div>Stop antibiotics</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#1D5FA8;"></div>Continue empiric</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#0F7A62;"></div>Target antibiotics</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#FFF8DC;border:1.5px solid #C49A00;"></div>Consider ceasing</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#E4F1F9;border:1.5px solid #7BB8D4;"></div>Decision / condition</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#FCDFDA;border:1.5px solid #C0392B;"></div>Urgent / unstable</div>
    <div class="legend-item">
      <div class="legend-swatch" style="background:#7D3C98;border-radius:50px;"></div>Recurrent fever</div>
    <div class="legend-item">
      <div class="badge yes" style="width:18px;height:18px;font-size:11px;box-shadow:none;">&#10003;</div>Yes / resolved</div>
    <div class="legend-item">
      <div class="badge no" style="width:18px;height:18px;font-size:11px;box-shadow:none;">&#10005;</div>No / ongoing / unstable</div>
  </div>
 
  <div class="footer">Auckland Te Toka Tumai Antimicrobial Stewardship &mdash;
  Based on Auckland Te Toka Tumai Neutropaenic Sepsis Management Guidelines. Not a substitute for clinical judgement.</div>
</div>

<div id="copyStatus" style="
  font-family:var(--font);font-size:12px;font-weight:700;
  text-align:center;padding:8px;color:#2BBBAD;
  display:none;"></div>

<script>
async function copyDiagram() {{
  const btn = document.getElementById('copyBtn');
  const el = document.querySelector('.infographic');
  btn.disabled = true;
  btn.textContent = 'Capturing\u2026';
  try {{
    const canvas = await html2canvas(el, {{ backgroundColor: '#F7F3EE', scale: 2 }});
    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
    await navigator.clipboard.write([new ClipboardItem({{ 'image/png': blob }})]);
    btn.innerHTML = '&#10003; Copied!';
  }} catch (e) {{
    try {{
      const canvas = await html2canvas(el, {{ backgroundColor: '#F7F3EE', scale: 2 }});
      const url = canvas.toDataURL('image/png');
      window.open(url, '_blank');
      btn.textContent = 'Opened in new tab \u2014 right-click to copy';
    }} catch (e2) {{
      btn.textContent = 'Copy failed \u2014 try again';
    }}
  }}
  setTimeout(() => {{ btn.innerHTML = '&#128203; Copy diagram to clipboard'; btn.disabled = false; }}, 2500);
}}
</script>

</body></html>"""
