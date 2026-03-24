"""
OPAT Last Dose Calculator
Auckland Te Toka Tumai Antimicrobial Stewardship
"""
 
from datetime import date
 
import streamlit as st
 
from opat import calculate_last_dose, calculate_line_removal
from opat.calculator import METHODS, CIVI, IVB, PO
 
st.title("\U0001f4c5 OPAT Last Dose Calculator")
st.caption("Auckland Te Toka Tumai Antimicrobial Stewardship \u2014 Calculate last dose and line removal dates")
st.markdown("---")
 
col_input, col_result = st.columns([1, 1.5], gap="large")
 
with col_input:
    st.subheader("Treatment Details")
 
    method = st.selectbox(
        "**Administration method**",
        METHODS,
        help="CIVI = Continuous infusor, IVB = IV bolus, PO = Oral therapy",
    )
 
    start_date = st.date_input(
        "**Start date**",
        value=date.today(),
        format="DD/MM/YYYY",
    )
 
    dot = st.number_input(
        "**Days of therapy (DOT)**",
        min_value=1,
        max_value=365,
        value=14,
        step=1,
    )
 
with col_result:
    st.subheader("Results")
 
    last_dose = calculate_last_dose(start_date, dot)
    line_removal = calculate_line_removal(last_dose, method)
 
    st.markdown(
        f"""<div style="
          background:#fff; border-radius:12px; padding:16px 20px;
          box-shadow:0 2px 8px rgba(0,0,0,0.08);
          border-left:4px solid #2BBBAD;
          font-family:'Nunito',sans-serif; margin-bottom:12px;">
          <div style="font-size:13px;font-weight:600;color:#5A7A8A;margin-bottom:4px;">
            Last Dose Date</div>
          <div style="font-size:22px;font-weight:800;color:#163344;">
            {last_dose.strftime('%A %d %B %Y')}</div>
          <div style="font-size:11px;color:#5A7A8A;margin-top:4px;">
            {start_date.strftime('%d-%m-%Y')} + {dot} days \u2212 1 = {last_dose.strftime('%d-%m-%Y')}</div>
        </div>""",
        unsafe_allow_html=True,
    )
 
    if line_removal is not None:
        label = "Line removal day (day after last dose)" if method == CIVI else "Line removal day (same as last dose)"
        st.markdown(
            f"""<div style="
              background:#fff; border-radius:12px; padding:16px 20px;
              box-shadow:0 2px 8px rgba(0,0,0,0.08);
              border-left:4px solid #1D5FA8;
              font-family:'Nunito',sans-serif; margin-bottom:12px;">
              <div style="font-size:13px;font-weight:600;color:#5A7A8A;margin-bottom:4px;">
                {label}</div>
              <div style="font-size:22px;font-weight:800;color:#163344;">
                {line_removal.strftime('%A %d %B %Y')}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """<div style="
              background:#fff; border-radius:12px; padding:16px 20px;
              box-shadow:0 2px 8px rgba(0,0,0,0.08);
              border-left:4px solid #8A9AA8;
              font-family:'Nunito',sans-serif; margin-bottom:12px;">
              <div style="font-size:13px;font-weight:600;color:#5A7A8A;margin-bottom:4px;">
                Line Removal</div>
              <div style="font-size:18px;font-weight:800;color:#8A9AA8;">
                N/A \u2014 Oral therapy</div>
            </div>""",
            unsafe_allow_html=True,
        )
 
st.markdown("---")
st.caption(
    "Auckland Te Toka Tumai Antimicrobial Stewardship. "
    "Not a substitute for clinical judgement."
)
