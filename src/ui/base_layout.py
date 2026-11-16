import streamlit as st

_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=DM+Sans:wght@400;500;600;700&display=swap');"
)

_BASE_CSS = """
:root {
    --at-bg: #FFFFFF;
    --at-subtle: #F7F8F9;
    --at-border: #E3E7EB;
    --at-border-strong: #CDD3DA;
    --at-text: #16191D;
    --at-muted: #5F6B76;
    --at-accent: #0F766E;
    --at-accent-hover: #0B5F59;
    --at-accent-soft: #E7F4F2;
    --at-danger: #B42318;
    --at-danger-soft: #FDEEEC;
    color-scheme: light;
}

#MainMenu, footer { visibility: hidden; }

/* ---------- Page ---------- */
html, body, .stApp, .stApp button, .stApp input, .stApp textarea {
    font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
/* Never let the text font override Streamlit's icon font. */
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--at-bg) !important;
    color: var(--at-text) !important;
}
[data-testid="stHeader"] { background: transparent !important; }

[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    margin: 0 auto !important;
    padding: 2rem 1.5rem 3rem !important;
}
[data-testid="stColumn"] { min-width: 0 !important; }

/* ---------- Typography ---------- */
h1, h2, h3, h4 {
    color: var(--at-text) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 2rem !important; line-height: 1.2 !important; }
h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.15rem !important; }

[data-testid="stCaptionContainer"] { color: var(--at-muted) !important; }
[data-testid="stWidgetLabel"] p { font-weight: 500 !important; color: var(--at-text) !important; }
a { color: var(--at-accent) !important; }
hr { border-color: var(--at-border) !important; margin: 1.25rem 0 !important; }

/* ---------- Buttons ---------- */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button,
[data-testid="stPopover"] > button {
    min-height: 2.5rem;
    padding: 0.45rem 1rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: none !important;
    transition: background-color .15s ease, border-color .15s ease, color .15s ease !important;
}
button[kind^="primary"] *,
button[kind^="secondary"] *,
button[kind="tertiary"] * {
    color: inherit !important;
    fill: currentColor !important;
}
.stButton > button,
.stButton > button p,
.stButton > button span {
    white-space: nowrap !important;
}

/* Primary */
button[kind^="primary"],
button[data-testid^="stBaseButton-primary"] {
    background: var(--at-accent) !important;
    border: 1px solid var(--at-accent) !important;
    color: #FFFFFF !important;
}
button[kind^="primary"]:hover:not(:disabled),
button[data-testid^="stBaseButton-primary"]:hover:not(:disabled) {
    background: var(--at-accent-hover) !important;
    border-color: var(--at-accent-hover) !important;
    color: #FFFFFF !important;
}

/* Secondary */
button[kind^="secondary"],
button[data-testid^="stBaseButton-secondary"] {
    background: #FFFFFF !important;
    border: 1px solid var(--at-border-strong) !important;
    color: var(--at-text) !important;
}
button[kind^="secondary"]:hover:not(:disabled),
button[data-testid^="stBaseButton-secondary"]:hover:not(:disabled) {
    background: var(--at-subtle) !important;
    border-color: #9AA5B1 !important;
    color: var(--at-text) !important;
}

/* Tertiary = destructive */
button[kind="tertiary"],
button[data-testid="stBaseButton-tertiary"] {
    background: #FFFFFF !important;
    border: 1px solid #EBC3BF !important;
    color: var(--at-danger) !important;
}
button[kind="tertiary"]:hover:not(:disabled),
button[data-testid="stBaseButton-tertiary"]:hover:not(:disabled) {
    background: var(--at-danger-soft) !important;
    border-color: var(--at-danger) !important;
    color: var(--at-danger) !important;
}

button:focus-visible {
    outline: 2px solid var(--at-accent) !important;
    outline-offset: 2px !important;
}
.stButton > button:disabled,
.stDownloadButton > button:disabled {
    opacity: 0.45 !important;
    cursor: not-allowed !important;
}

/* ---------- Inputs ---------- */
div[data-baseweb="input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid var(--at-border-strong) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
div[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--at-accent) !important;
    box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15) !important;
}
input, textarea { color: var(--at-text) !important; }

/* ---------- Data, media, feedback ---------- */
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border: 1px solid var(--at-border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
div[data-testid="stAlert"] { border-radius: 8px !important; }
[data-testid="stImage"] img,
[data-testid="stCameraInput"] video { border-radius: 10px !important; }
div[data-testid="stDialog"] div[role="dialog"] { border-radius: 14px !important; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--at-subtle) !important;
    border-right: 1px solid var(--at-border) !important;
}

/* Teacher navigation: quiet list, active item gets a soft teal tint. */
[class*="st-key-teacher_nav_"] button[kind="secondary"] {
    background: transparent !important;
    border-color: transparent !important;
    color: var(--at-muted) !important;
    justify-content: flex-start !important;
}
[class*="st-key-teacher_nav_"] button[kind="secondary"]:hover:not(:disabled) {
    background: #ECEFF2 !important;
    border-color: transparent !important;
    color: var(--at-text) !important;
}
[class*="st-key-teacher_nav_"] button[kind="primary"] {
    background: var(--at-accent-soft) !important;
    border-color: transparent !important;
    color: var(--at-accent) !important;
    justify-content: flex-start !important;
}
[class*="st-key-teacher_nav_"] button[kind="primary"]:hover:not(:disabled) {
    background: #D6ECE8 !important;
    border-color: transparent !important;
    color: var(--at-accent) !important;
}

/* ---------- Reusable pieces (header, footer, cards) ---------- */
.at-brand {
    display: flex; align-items: center; gap: .6rem;
    font-weight: 700; font-size: 1.1rem; letter-spacing: -0.01em;
    color: var(--at-text);
}
.at-brand img { height: 28px; width: 28px; object-fit: contain; }

.at-hero { text-align: center; padding: 1rem 0 2rem; }
.at-hero img { height: 56px; margin-bottom: .75rem; }
.at-hero h1 { margin: 0 !important; padding: 0 !important; }
.at-hero p { color: var(--at-muted); margin: .4rem 0 0; font-size: 1.02rem; }

.at-label { font-size: .8rem; color: var(--at-muted); }
.at-user { font-weight: 600; color: var(--at-text); overflow-wrap: anywhere; margin-bottom: .75rem; }

.at-footer {
    margin-top: 3rem; padding-top: 1rem;
    border-top: 1px solid var(--at-border);
    display: flex; flex-wrap: wrap; justify-content: center;
    gap: .25rem 1rem; text-align: center;
    font-size: .82rem; color: var(--at-muted);
}
.at-footer strong { color: var(--at-text); font-weight: 600; }

.at-subject-name {
    font-size: 1.1rem; font-weight: 600; line-height: 1.3;
    letter-spacing: -0.01em; color: var(--at-text); overflow-wrap: anywhere;
}
.at-subject-meta {
    display: flex; flex-wrap: wrap; align-items: center; gap: .6rem;
    margin: .5rem 0 1rem; font-size: .88rem; color: var(--at-muted);
}
.at-code {
    background: var(--at-accent-soft); color: var(--at-accent);
    padding: 2px 8px; border-radius: 6px;
    font-weight: 600; font-size: .82rem; letter-spacing: .02em;
}
.at-stats { display: flex; flex-wrap: wrap; gap: 2rem; margin-bottom: .5rem; }
.at-stat b { display: block; font-size: 1.4rem; font-weight: 600; line-height: 1.1; color: var(--at-text); }
.at-stat span { font-size: .8rem; color: var(--at-muted); }

@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding: 1rem 1rem 2rem !important; }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.3rem !important; }
}
"""


def _inject(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def style_base_layout():
    """Full theme: fonts, colours, buttons, inputs, sidebar. Call on every screen."""
    _inject(_FONT_IMPORT + _BASE_CSS)


def style_background_home():
    """Narrow, centred column for the landing page."""
    _inject(
        ".stApp [data-testid='stMainBlockContainer'] "
        "{ max-width: 760px !important; padding-top: 3rem !important; }"
    )


def style_background_dashboard(max_width: str = "1080px"):
    """Content width for dashboards. Pass a smaller value (e.g. '520px') for login pages."""
    _inject(
        "[data-testid='stMainBlockContainer'] "
        f"{{ max-width: {max_width} !important; }}"
    )