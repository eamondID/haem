"""
Auckland City Infection Team Tools — Auckland Te Toka Tumai Antimicrobial Stewardship
Clinical decision support tools for ID.
"""
 
import streamlit as st
 
st.set_page_config(
    page_title="Auckland City Infection Team Tools",
    page_icon="\U0001f9ec",
    layout="wide",
)
 
st.title("\U0001f9ec Auckland City Infection Team Tools")
st.caption("Auckland Te Toka Tumai \u2014 Clinical Decision Support")
st.markdown("---")
 
st.markdown(
    """
    ### Available Tools
 
    Use the sidebar to navigate between tools.
 
    - **Neutropenic Sepsis Management** \u2014 Interactive decision pathway for 72-hour review
    - **OPAT Calculator** \u2014 Last dose and line removal date calculator
    """
)
