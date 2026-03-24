"""
Neutropenic Sepsis Management — BMJ Infographic Style
Auckland Te Toka Tumai Antimicrobial Stewardship
"""
 
import streamlit as st
import streamlit.components.v1 as components
 
from pathway import determine_pathway, get_recommendations, build_html
 
# Minimal scoped CSS — avoids corrupting Streamlit icon rendering
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #F7F3EE; }
  [data-testid="stSidebar"] { background: #FFFFFF; }
</style>
""", unsafe_allow_html=True)
 
st.title("\U0001f9ec Neutropenic Sepsis Management")
st.caption("Auckland Te Toka Tumai Antimicrobial Stewardship \u2014 Interactive Decision Support Tool")
st.markdown("---")
 
col_form, col_chart = st.columns([1, 3.2], gap="large")
 
with col_form:
    st.subheader("Patient Assessment")
 
    fever_resolved = st.radio(
        "**Fever status at 72-hour review**",
        ["Resolved (afebrile >48 h, clinically stable)",
         "Persistent / recurrent fever"],
    ) == "Resolved (afebrile >48 h, clinically stable)"
 
    neutro_resolved = st.radio(
        "**Neutropenia status**",
        ["Resolved", "Ongoing"],
        index=1,
    ) == "Resolved"
 
    micro_defined = st.checkbox(
        "**Microbiologically or clinically defined infection**",
        value=False,
    )
 
    stable = st.radio(
        "**Clinical stability**",
        ["Clinically stable", "Clinically unstable"],
        disabled=(fever_resolved or micro_defined),
        help="Only relevant for persistent fever without a defined infection source",
    ) == "Clinically stable"
 
    enterocolitis = st.checkbox(
        "**Enterocolitis or significant mucositis**",
        value=False,
        disabled=(neutro_resolved and not micro_defined),
    )
 
    allo_sct = st.checkbox(
        "**Allo-SCT patient**",
        value=False,
        disabled=(enterocolitis or neutro_resolved),
        help="Relevant when: ongoing neutropenia, no enterocolitis, resolved fever",
    )
 
    st.markdown("---")
    copy_clicked = st.button("\U0001f4cb Copy diagram to clipboard", use_container_width=True)
    st.caption(
        "\u2139\ufe0f All decisions should be made in clinical context. "
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
 
    components.html(build_html(AN, auto_copy=copy_clicked), height=870, scrolling=True)
 
# ── Recommendations ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("\U0001f4cb Recommended Actions")
 
recs = get_recommendations(AN)
if recs:
    cols = st.columns(min(len(recs), 3))
    for i, (icon, title, detail) in enumerate(recs):
        with cols[i % len(cols)]:
            st.markdown(
                f"""<div style="
                  background:#fff; border-radius:12px; padding:12px 14px;
                  box-shadow:0 2px 8px rgba(0,0,0,0.08);
                  border-left:4px solid #2BBBAD;
                  font-family:'Nunito',sans-serif; margin-bottom:8px;">
                  <div style="font-size:14px;font-weight:800;color:#163344;margin-bottom:4px;">
                    {icon} {title}</div>
                  <div style="font-size:12px;color:#3A5060;line-height:1.5;">{detail}</div>
                </div>""",
                unsafe_allow_html=True,
            )
else:
    st.info("Select patient parameters above to see tailored recommendations.")
 
st.markdown("---")
st.caption(
    "Based on Auckland Te Toka Tumai Neutropenic Sepsis Management Guidelines. "
    "Not a substitute for clinical judgement."
)
