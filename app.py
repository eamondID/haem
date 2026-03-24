"""
Haem Tools — ADHB Antimicrobial Stewardship
Clinical decision support tools for haematology.
"""
 
import streamlit as st
 
st.set_page_config(
    page_title="Haem Tools",
    page_icon="\U0001f9ec",
    layout="wide",
)
 
st.title("\U0001f9ec Haem Tools")
st.caption("ADHB Antimicrobial Stewardship \u2014 Clinical Decision Support")
st.markdown("---")
 
st.markdown(
    """
    ### Available Tools
 
    Use the sidebar to navigate between tools.
 
    - **Neutropaenic Sepsis Management** \u2014 Interactive decision pathway for 72-hour review
    - **OPAT Calculator** \u2014 Last dose and line removal date calculator
    """
)
