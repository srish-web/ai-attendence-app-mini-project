import streamlit as st


def style_background_home():
    st.markdown("""
    <style>
        .stApp {
            background: #F4F7FC !important;
        }

        /* Style only the direct home-page columns; avoid affecting every dashboard column. */
        .stApp div[data-testid="stColumn"] {
            min-width: 0;
        }
    </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
    <style>
        :root {
            color-scheme: light;
        }

        .stApp {
            background: #F4F7FC !important;
            color: #17233F !important;
        }

        [data-testid="stAppViewContainer"] {
            background: #F4F7FC !important;
        }

        [data-testid="stMain"] {
            background: #F4F7FC !important;
        }

        /* Use the full browser width instead of Streamlit's narrow centered layout. */
        section.main > div,
        [data-testid="stMainBlockContainer"],
        .block-container {
            max-width: 100% !important;
            width: 100% !important;
        }

        [data-testid="stMainBlockContainer"] {
            padding: 1.6rem clamp(1rem, 3vw, 3rem) 2.5rem !important;
        }

        /* Keep columns flexible and prevent the old global white-column cards. */
        [data-testid="stColumn"] {
            min-width: 0 !important;
        }

        /* Streamlit top bar */
        [data-testid="stHeader"] {
            background: rgba(244, 247, 252, 0.92) !important;
        }

        /* Main headings */
        h1, h2, h3, h4, h5, h6 {
            color: #14213D !important;
            letter-spacing: -0.025em !important;
        }

        h1 {
            font-size: clamp(2rem, 3vw, 2.8rem) !important;
            font-weight: 750 !important;
            line-height: 1.15 !important;
        }

        h2 {
            font-size: clamp(1.5rem, 2.2vw, 2rem) !important;
            font-weight: 700 !important;
        }

        h3 {
            font-size: 1.25rem !important;
            font-weight: 650 !important;
        }

        p, label, span, div, input, textarea, button {
            font-family: 'Outfit', 'Inter', sans-serif;
        }

        /* Buttons */
        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button,
        [data-testid="stPopover"] > button {
            min-height: 2.65rem !important;
            border-radius: 0.75rem !important;
            padding: 0.55rem 1.05rem !important;
            font-weight: 600 !important;
            border: 1px solid #2F67F6 !important;
            background: #2F67F6 !important;
            color: #FFFFFF !important;
            box-shadow: 0 3px 8px rgba(47, 103, 246, 0.10) !important;
            transition: background 0.18s ease, box-shadow 0.18s ease,
                        transform 0.18s ease !important;
        }

        .stButton > button *,
        .stFormSubmitButton > button *,
        .stDownloadButton > button *,
        [data-testid="stPopover"] > button * {
            color: inherit !important;
            fill: currentColor !important;
            opacity: 1 !important;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover {
            background: #1F54DB !important;
            border-color: #1F54DB !important;
            color: #FFFFFF !important;
            box-shadow: 0 7px 18px rgba(47, 103, 246, 0.20) !important;
            transform: translateY(-1px);
        }

        .stButton > button[kind="secondary"],
        .stFormSubmitButton > button[kind="secondary"],
        .stDownloadButton > button[kind="secondary"],
        button[data-testid="baseButton-secondary"] {
            background: #FFFFFF !important;
            color: #233451 !important;
            border: 1px solid #D9E1EF !important;
            box-shadow: none !important;
        }

        .stButton > button[kind="secondary"] *,
        .stFormSubmitButton > button[kind="secondary"] *,
        .stDownloadButton > button[kind="secondary"] *,
        button[data-testid="baseButton-secondary"] * {
            color: #233451 !important;
            fill: #233451 !important;
        }

        .stButton > button[kind="secondary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {
            background: #EDF2FB !important;
            border-color: #C7D4E8 !important;
        }

        .stButton > button[kind="tertiary"],
        button[data-testid="baseButton-tertiary"] {
            background: #17233F !important;
            color: #FFFFFF !important;
            border-color: #17233F !important;
            box-shadow: none !important;
        }

        .stButton > button[kind="tertiary"] *,
        button[data-testid="baseButton-tertiary"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        .stButton > button:disabled {
            opacity: 0.45 !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }

        /* Form controls */
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stTextArea textarea {
            min-height: 2.7rem !important;
            border-radius: 0.7rem !important;
            border: 1px solid #D8E1EF !important;
            background: #FFFFFF !important;
            color: #17233F !important;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stTimeInput input:focus,
        .stTextArea textarea:focus {
            border-color: #2F67F6 !important;
            box-shadow: 0 0 0 3px rgba(47, 103, 246, 0.12) !important;
        }

        div[data-baseweb="select"] > div {
            min-height: 2.7rem !important;
            border-radius: 0.7rem !important;
            border-color: #D8E1EF !important;
            background: #FFFFFF !important;
        }

        /* Metrics and data tables */
        div[data-testid="stMetric"] {
            background: #FFFFFF !important;
            padding: 1.15rem 1.25rem !important;
            border: 1px solid #E2E8F2 !important;
            border-radius: 1rem !important;
            box-shadow: 0 4px 16px rgba(24, 39, 75, 0.035) !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #71809B !important;
        }

        div[data-testid="stMetricValue"] {
            color: #2F67F6 !important;
            font-weight: 750 !important;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            border: 1px solid #E1E7F0 !important;
            border-radius: 0.85rem !important;
            overflow: hidden !important;
            background: #FFFFFF !important;
        }

        /* Dividers and status messages */
        hr {
            border-color: #DFE6F0 !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 0.8rem !important;
            border: 1px solid #E0E7F1 !important;
        }

        /* Sidebar, if used by other screens */
        section[data-testid="stSidebar"] {
            background: #111E3B !important;
            border-right: 1px solid #243251 !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #F8FAFC !important;
        }

        /* Keep the layout usable on smaller screens. */
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 0.85rem 2rem !important;
            }

            h1 {
                font-size: 1.9rem !important;
            }

            h2 {
                font-size: 1.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        #MainMenu, footer {
            visibility: hidden;
        }

        html, body, [class*="css"] {
            font-family: 'Outfit', 'Inter', sans-serif !important;
        }

        .stApp {
            background: #F4F7FC !important;
        }

        /* A subtle page entrance without affecting Streamlit widget behavior. */
        [data-testid="stMainBlockContainer"] {
            animation: attendlyFadeIn 0.28s ease-out;
        }

        @keyframes attendlyFadeIn {
            from { opacity: 0.85; }
            to { opacity: 1; }
        }

        /* Keep images neatly framed in the photo gallery. */
        [data-testid="stImage"] img {
            border-radius: 0.8rem !important;
        }

        /* Improve tab-like navigation buttons and general spacing. */
        .stButton {
            min-width: 0;
        }

        /* Links */
        a {
            color: #2F67F6 !important;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 9px;
            height: 9px;
        }

        ::-webkit-scrollbar-thumb {
            background: #C9D4E5;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #F4F7FC;
        }
    </style>
    """, unsafe_allow_html=True)
