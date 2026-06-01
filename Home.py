"""Water on Paper — series cover.

The landing page hosts the full *Water on Paper* editorial scrollytelling
microsite (the static design bundle under `static/water_on_paper/`) inside a
single Streamlit `components.html` iframe. The four deep-tool pages (Map,
Contaminants, Grievance, Groundwater) live as siblings under `pages/` and
share the same Spline Sans / Instrument Serif design tokens via theme.py.

The essay's Chapter 06 "Neer — know your water" panel has a deep-dive button
that escapes the iframe (`target="_top"`) into the Streamlit Map page, so the
transition from the editorial to the tool happens in-place.
"""
from __future__ import annotations

import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Water on Paper — Neer",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ESSAY_DIR = Path(__file__).resolve().parent / "static" / "water_on_paper"
ASSETS = ESSAY_DIR / "assets"


@st.cache_data(show_spinner=False)
def _build_essay_html() -> str:
    """Inline the static bundle (HTML + CSS + JS) into a single string."""
    html = (ESSAY_DIR / "index.html").read_text(encoding="utf-8")
    css = (ASSETS / "styles.css").read_text(encoding="utf-8")
    data_js = (ASSETS / "data.js").read_text(encoding="utf-8")
    charts_js = (ASSETS / "charts.js").read_text(encoding="utf-8")
    map_js = (ASSETS / "map.js").read_text(encoding="utf-8")
    main_js = (ASSETS / "main.js").read_text(encoding="utf-8")

    # Inline the stylesheet
    html = html.replace(
        '<link rel="stylesheet" href="assets/styles.css" />',
        f"<style>\n{css}\n</style>",
    )
    # Strip external <script src="assets/*.js"> tags — we re-inject them inline
    # in the correct load order (data → charts → map → main) before </body>.
    html = re.sub(r'<script src="assets/[^"]+"></script>\s*', "", html)
    inlined = (
        f"<script>\n{data_js}\n</script>\n"
        f"<script>\n{charts_js}\n</script>\n"
        f"<script>\n{map_js}\n</script>\n"
        f"<script>\n{main_js}\n</script>\n"
    )
    html = html.replace("</body>", f"{inlined}</body>")
    return html


# ---------------------------------------------------------------------------
# Streamlit chrome — strip everything that interferes with the editorial.
st.markdown(
    """
    <style>
      [data-testid="stHeader"], [data-testid="stDecoration"],
      #MainMenu, footer, [data-testid="stStatusWidget"] { display: none !important; }
      .stApp { background: #f9f4ec !important; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stMainBlockContainer"] { padding: 0 !important; }
      [data-testid="stSidebar"][aria-expanded="false"] { width: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# The essay itself — full-bleed iframe. 920 px is one comfortable viewport;
# the embed scrolls internally so each chapter's animations fire naturally.
components.html(_build_essay_html(), height=920, scrolling=True)

# A quiet footer breadcrumb under the iframe so multipage navigation is still
# discoverable for users who collapse the sidebar.
st.markdown(
    """
    <div style="text-align:center;padding:28px 16px 36px;
                color:#80828a;font-family:'Spline Sans Mono', ui-monospace, monospace;
                font-size:0.78rem;letter-spacing:0.06em;">
      Continue into <b style="color:#2c5878">Neer</b> · the full tool ↓ &nbsp;·&nbsp;
      <a href="/Map_and_Source"            target="_self" style="color:#3f86c0;text-decoration:none">Map &amp; Source</a> &nbsp;·&nbsp;
      <a href="/Contaminants_and_Restoration" target="_self" style="color:#3f86c0;text-decoration:none">Contaminants</a> &nbsp;·&nbsp;
      <a href="/Grievance_Drafter"         target="_self" style="color:#3f86c0;text-decoration:none">Grievance</a> &nbsp;·&nbsp;
      <a href="/Groundwater_and_Demand"    target="_self" style="color:#3f86c0;text-decoration:none">Groundwater</a>
    </div>
    """,
    unsafe_allow_html=True,
)
