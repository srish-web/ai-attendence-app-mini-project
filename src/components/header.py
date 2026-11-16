import streamlit as st

# Single source for the app name and logo (also used by the teacher sidebar).
APP_NAME = "Attende Tracker"
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/5850/5850276.png"


def header_home():
    st.markdown(
        f'<div class="at-hero">'
        f'<img src="{LOGO_URL}" alt="" />'
        f'<h1>{APP_NAME}</h1>'
        f'<p>Attendance made simple with face and voice recognition.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def header_dashboard():
    st.markdown(
        f'<div class="at-brand"><img src="{LOGO_URL}" alt="" />{APP_NAME}</div>',
        unsafe_allow_html=True,
    )
