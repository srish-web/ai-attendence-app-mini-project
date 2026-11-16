import streamlit as st


def _footer():
    st.markdown(
        '<div class="at-footer">'
        '<strong>Mini Project: Team 80</strong>'
        '<span>Srishty Gupta, Srishti Chaturvedi, Sonakshi Tripathi</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def footer_home():
    _footer()


def footer_dashboard():
    _footer()
