"""Theme + shared chrome (sidebar) for all Pukhuri pages.

`init_page(...)` is called at the very top of every page. It:
1. Configures st.set_page_config (title, icon, layout).
2. Initialises session state defaults.
3. Injects base CSS and the active theme (light/dark).
4. Renders the shared sidebar (theme toggle, language, state, district).

Pages then just render their own body.

Maps are rendered via `render_map()` to avoid the streamlit-folium dependency,
which has Python 3.13 / serialization issues on Hugging Face Spaces.
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from .data_loader import load_districts, load_states
from .i18n import LANG_LABELS, t

# ---------------------------------------------------------------------------
# CSS

_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stText {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}
code, pre, kbd { font-family: 'JetBrains Mono', ui-monospace, monospace !important; }

/* Hide Streamlit chrome for a cleaner look */
#MainMenu, footer, [data-testid="stStatusWidget"] { visibility: hidden; height: 0; }
[data-testid="stToolbar"] { right: 0.5rem; }

/* Headings */
h1, h2, h3, h4 {
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}
h1 { font-size: 2.25rem !important; }
h2 { font-size: 1.5rem !important; margin-top: 2rem !important; }
h3 { font-size: 1.15rem !important; }

/* Body text */
p, li { line-height: 1.65; }

/* Block container — tighter top padding */
.block-container { padding-top: 2.5rem !important; padding-bottom: 4rem !important; max-width: 1200px; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
    padding: 0.45rem 1rem !important;
}
.stButton > button:hover { transform: translateY(-1px); }

/* Primary button accent */
.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
}

/* Inputs / Selects / Textareas */
[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea, .stNumberInput input {
    border-radius: 8px !important;
    border-color: var(--border-color) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--border-color); }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-weight: 500; }

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
}
[data-testid="stExpander"] summary { font-weight: 500; }

/* Page links */
[data-testid="stPageLink"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.15s ease;
}
[data-testid="stPageLink"]:hover {
    border-color: var(--accent) !important;
    transform: translateX(2px);
}

/* Custom feature card */
.pukhuri-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
    height: 100%;
}
.pukhuri-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}
.pukhuri-card h3 { margin-top: 0 !important; margin-bottom: 0.5rem !important; }
.pukhuri-card p { color: var(--text-secondary); margin-bottom: 0.75rem; font-size: 0.95rem; }
.pukhuri-card .icon { font-size: 1.4rem; margin-bottom: 0.5rem; display: inline-block; }

/* Badge */
.pukhuri-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
}

/* Snapshot banner */
.pukhuri-banner {
    background: var(--bg-banner);
    border-left: 3px solid var(--accent);
    padding: 0.85rem 1rem;
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 0.92rem;
    margin: 1rem 0 1.5rem 0;
}

/* Sidebar tweaks */
[data-testid="stSidebar"] { border-right: 1px solid var(--border-color); }
[data-testid="stSidebar"] hr { margin: 0.75rem 0 !important; }

/* Dividers */
hr { border-color: var(--border-color) !important; opacity: 0.6; }
</style>
"""

_LIGHT = """
<style>
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f6f8fc;
    --bg-card: #ffffff;
    --bg-banner: #f0f7ff;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --accent: #0284c7;
    --border-color: #e5e9f0;
}
.stApp { background: var(--bg-primary) !important; }
[data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
</style>
"""

_DARK = """
<style>
:root {
    --bg-primary: #0b1120;
    --bg-secondary: #131b2e;
    --bg-card: #161f36;
    --bg-banner: #14233e;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --accent: #38bdf8;
    --border-color: #243049;
}
.stApp, body { background: var(--bg-primary) !important; color: var(--text-primary) !important; }
.stApp * { color-scheme: dark; }
[data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
[data-testid="stSidebar"] *, .stMarkdown, .stMarkdown p, .stMarkdown li,
h1, h2, h3, h4, h5, h6, label, .stCaption {
    color: var(--text-primary) !important;
}
.stCaption, [data-testid="stCaptionContainer"], .pukhuri-card p { color: var(--text-secondary) !important; }

/* Inputs */
[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea,
.stNumberInput input, [data-baseweb="popover"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}
[data-baseweb="select"] [data-baseweb="tag"] { background: var(--bg-secondary) !important; }
[data-baseweb="menu"] { background: var(--bg-card) !important; }
[data-baseweb="menu"] li:hover { background: var(--bg-secondary) !important; }

/* Code */
code, pre { background: var(--bg-secondary) !important; color: #cbd5e1 !important; }

/* Streamlit alerts */
[data-testid="stAlert"] { background: var(--bg-card) !important; border: 1px solid var(--border-color) !important; }

/* Dataframes */
[data-testid="stDataFrame"] { background: var(--bg-card) !important; }

/* Tab underline accent */
.stTabs [aria-selected="true"] { color: var(--accent) !important; }
</style>
"""


# ---------------------------------------------------------------------------
# Public helpers


def init_page(*, title: str, icon: str = "💧", layout: str = "wide") -> None:
    """Single-call setup for every page."""
    st.set_page_config(
        page_title=f"{title} — Pukhuri",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded",
        menu_items={"Get help": None, "Report a bug": None, "About": "Pukhuri — know your water in India."},
    )
    _init_state()
    _inject_css()
    _render_sidebar()


def render_map(fmap, *, height: int = 560) -> None:
    """Render a folium.Map without the streamlit-folium dependency.

    streamlit-folium has serialization issues on Python 3.13 (HF Spaces default).
    We fall back to a plain components.html embed of the folium iframe HTML —
    which is exactly what folium_static used to do internally.
    """
    components.html(fmap._repr_html_(), height=height + 8, scrolling=False)


def feature_card(*, icon: str, title: str, body: str, page: str, link_label: str) -> None:
    """A clean feature card with a page link below."""
    st.markdown(
        f"""
        <div class="pukhuri-card">
            <div class="icon">{icon}</div>
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(page, label=link_label)


def section_banner(text: str) -> None:
    """Snapshot/disclaimer banner styled with the theme."""
    st.markdown(f'<div class="pukhuri-banner">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Internal


def _init_state() -> None:
    st.session_state.setdefault("dark_mode", False)
    st.session_state.setdefault("lang", "en")
    st.session_state.setdefault("state", None)
    st.session_state.setdefault("district", None)


def _inject_css() -> None:
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    st.markdown(_DARK if st.session_state.get("dark_mode") else _LIGHT, unsafe_allow_html=True)


def _render_sidebar() -> None:
    states_df = load_states()
    districts_df = load_districts()

    with st.sidebar:
        st.markdown("### Pukhuri")
        st.caption("Know your water — India")

        st.toggle(
            "Dark mode",
            key="dark_mode",
            help="Switch between light and dark themes (per session).",
        )
        st.divider()

        st.markdown("**Language**")
        lang_keys = list(LANG_LABELS.keys())
        lang_choice = st.selectbox(
            "Language",
            options=lang_keys,
            index=lang_keys.index(st.session_state["lang"]) if st.session_state["lang"] in lang_keys else 0,
            format_func=lambda c: LANG_LABELS[c],
            label_visibility="collapsed",
            key="_lang_select",
        )
        st.session_state["lang"] = lang_choice if lang_choice == "en" else "en"
        if lang_choice != "en":
            st.caption("Translation pack pending — falling back to English.")

        st.markdown(f"**{t('select_state', st.session_state['lang'])}**")
        state_options = ["—"] + sorted(states_df["state"].unique().tolist())
        cur_state = st.session_state.get("state") or "—"
        state = st.selectbox(
            "State",
            state_options,
            index=state_options.index(cur_state) if cur_state in state_options else 0,
            label_visibility="collapsed",
            key="_state_select",
        )
        st.session_state["state"] = None if state == "—" else state

        if st.session_state.get("state"):
            st.markdown(f"**{t('select_district', st.session_state['lang'])}**")
            d_opts = ["—"] + sorted(
                districts_df[districts_df["state"] == st.session_state["state"]]["district"].tolist()
            )
            cur_d = st.session_state.get("district") or "—"
            d = st.selectbox(
                "District",
                d_opts,
                index=d_opts.index(cur_d) if cur_d in d_opts else 0,
                label_visibility="collapsed",
                key="_district_select",
            )
            st.session_state["district"] = None if d == "—" else d

        st.divider()
        st.caption(
            "Districts in our snapshot only. Others fall back to state-level. "
            "Absence ≠ safety — always test your own water."
        )
