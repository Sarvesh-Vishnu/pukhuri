"""Theme + shared chrome (sidebar) for all Neer pages.

`init_page(...)` is called at the very top of every page. It:
1. Configures st.set_page_config (title, icon, layout).
2. Initialises session state defaults + syncs with URL query params.
3. Injects base CSS and the active theme (light/dark).
4. Renders the shared sidebar (theme toggle, language, state, district).

Maps are rendered via `render_map()` to avoid the streamlit-folium dependency,
which has Python 3.13 / serialization issues on Hugging Face Spaces.
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from .data_loader import load_districts, load_states
from .i18n import LANG_LABELS, t

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PHOTOS_DIR = ASSETS_DIR / "photos"

# Basemap for every folium map, defined once so a provider change is a one-line fix.
# CARTO's "cartodbpositron" began serving "API KEY REQUIRED" watermark tiles, so we
# use Esri's keyless World Light Gray Base — same quiet light-grey look.
MAP_TILES = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
)
MAP_ATTR = (
    "Tiles &copy; Esri &mdash; Esri, HERE, Garmin, &copy; OpenStreetMap "
    "contributors, and the GIS User Community"
)


def _flatten_html(s: str) -> str:
    """Collapse multi-line indented HTML to a single line.

    Streamlit's markdown treats lines indented by 4+ spaces as code blocks even when
    `unsafe_allow_html=True` is set. Flattening keeps `<pre><code>` from being injected
    around our hero / card markup.
    """
    return re.sub(r"\n\s*", "", s).strip()


def _img_data_uri(path: Path) -> str | None:
    """Read an image and return a base64 data URI, or None if missing."""
    if not path.exists():
        return None
    suffix = path.suffix.lstrip(".").lower()
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    return f"data:image/{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


@st.cache_data(show_spinner=False)
def _cached_img_uri(path_str: str) -> str | None:
    return _img_data_uri(Path(path_str))

# ---------------------------------------------------------------------------
# CSS

_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Spline+Sans:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stText {
    font-family: 'Spline Sans', ui-sans-serif, system-ui, -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}
code, pre, kbd { font-family: 'Spline Sans Mono', ui-monospace, monospace !important; }
[data-testid="stCaptionContainer"], .stCaption,
[data-testid="stMetricLabel"], .pukhuri-badge {
    font-family: 'Spline Sans Mono', ui-monospace, monospace !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 0.78rem !important;
}

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    font-feature-settings: 'liga' !important;
    -webkit-font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased;
    display: inline-block;
}

#MainMenu, footer, [data-testid="stStatusWidget"] { visibility: hidden; height: 0; }
[data-testid="stToolbar"] { right: 0.5rem; }

/* Streamlit's auto header/decoration reserve a chunk of space at the top —
   hide them so the hero/title sits flush with the viewport. */
[data-testid="stHeader"], header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
    visibility: hidden !important;
}
[data-testid="stDecoration"] { display: none !important; }
.stApp > header { height: 0 !important; }

/* Display headings use Instrument Serif (matches Water on Paper essay) */
h1, h2 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    font-weight: 400 !important;
    letter-spacing: -0.015em !important;
    line-height: 1.0 !important;
}
h3, h4 {
    font-family: 'Spline Sans', ui-sans-serif, sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.25 !important;
}
h1 { font-size: 3rem !important; margin-bottom: 0.4em !important; }
h2 { font-size: 2rem !important; margin-top: 2rem !important; }
h3 { font-size: 1.2rem !important; }

p, li { line-height: 1.65; }

.block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
    padding: 0.45rem 1rem !important;
}
.stButton > button:hover { transform: translateY(-1px); }

.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    color: #ffffff !important;
}

[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea, .stNumberInput input {
    border-radius: 8px !important;
    border-color: var(--border-color) !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--border-color); }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; }

[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-weight: 500; }

[data-testid="stExpander"] {
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
}
[data-testid="stExpander"] summary { font-weight: 500; }

[data-testid="stPageLink"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.15s ease;
    color: var(--accent) !important;
    font-weight: 500 !important;
    display: inline-flex !important;
    align-items: center;
}
[data-testid="stPageLink"] *,
[data-testid="stPageLink"] p,
[data-testid="stPageLink"] span {
    color: var(--accent) !important;
}
[data-testid="stPageLink"]:hover {
    border-color: var(--accent) !important;
    transform: translateX(2px);
    background: var(--bg-secondary) !important;
}

/* Custom feature card */
.pukhuri-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 1.5rem 1.5rem 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
}
.pukhuri-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}
.pukhuri-card h3 {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
    color: var(--text-primary) !important;
}
.pukhuri-card p {
    color: var(--text-secondary) !important;
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}
.pukhuri-card .icon {
    color: var(--accent);
    margin-bottom: 0.65rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background: var(--bg-banner);
}
.pukhuri-card .icon .material-symbols-outlined {
    font-size: 24px !important;
}

.pukhuri-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: var(--bg-banner);
    color: var(--accent);
    border: 1px solid var(--border-color);
}

.pukhuri-banner {
    background: var(--bg-banner);
    border-left: 3px solid var(--accent);
    padding: 0.85rem 1rem;
    border-radius: 6px;
    color: var(--text-primary) !important;
    font-size: 0.92rem;
    margin: 1rem 0 1.5rem 0;
}
.pukhuri-banner strong { color: var(--text-primary) !important; }

/* Hero */
.pukhuri-hero {
    position: relative;
    background: linear-gradient(135deg, var(--hero-from) 0%, var(--hero-to) 100%);
    border-radius: 18px;
    padding: 2.25rem 2rem 2rem 2rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
    border: 1px solid var(--border-color);
}
.pukhuri-hero h1 {
    color: #ffffff !important;
    margin: 0 0 0.5rem 0 !important;
    font-size: 2.5rem !important;
}
.pukhuri-hero .subtitle {
    color: rgba(255,255,255,0.92) !important;
    font-size: 1.05rem;
    max-width: 720px;
    line-height: 1.55;
}
.pukhuri-hero .badge-row { margin-top: 1rem; }
.pukhuri-hero .pukhuri-badge {
    background: rgba(255,255,255,0.16);
    color: #ffffff;
    border-color: rgba(255,255,255,0.25);
}
.pukhuri-hero svg.bg-art {
    position: absolute;
    right: -40px;
    bottom: -40px;
    opacity: 0.18;
    pointer-events: none;
}

/* Photo hero — same shape as the SVG hero but with a real image background */
.pukhuri-hero--photo {
    background-size: cover !important;
    background-position: center !important;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.pukhuri-hero--photo .hero-credit {
    margin-top: 1rem;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.78);
}
.pukhuri-hero--photo .hero-credit a {
    color: rgba(255,255,255,0.95) !important;
    text-decoration: underline;
}

/* Page-level photo banner (smaller than hero) */
.pukhuri-page-photo {
    background-size: cover;
    background-position: center;
    border-radius: 14px;
    padding: 1.75rem 1.75rem 1.5rem 1.75rem;
    margin-bottom: 0.5rem;
    border: 1px solid var(--border-color);
    color: #ffffff;
    min-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.pukhuri-page-photo h1 {
    color: #ffffff !important;
    margin: 0 0 0.4rem 0 !important;
    font-size: 1.85rem !important;
}
.pukhuri-page-photo .page-caption {
    color: rgba(255,255,255,0.92) !important;
    font-size: 0.95rem;
    max-width: 760px;
    line-height: 1.5;
}

/* Sidebar */
[data-testid="stSidebar"] { border-right: 1px solid var(--border-color); }
[data-testid="stSidebar"] hr { margin: 0.75rem 0 !important; }

hr { border-color: var(--border-color) !important; opacity: 0.6; }
</style>
"""

_LIGHT = """
<style>
:root {
    /* Water on Paper — paper & ink palette */
    --bg-primary: #f9f4ec;       /* paper */
    --bg-secondary: #f1ebe0;     /* paper-2 (sidebar / panels) */
    --bg-card: #f9f4ec;          /* card */
    --bg-banner: rgba(63,134,192,0.12);  /* water-mist */
    --text-primary: #2b2d33;     /* ink */
    --text-secondary: #54565d;   /* ink-soft */
    --text-faint: #80828a;       /* ink-faint */
    --accent: #3f86c0;           /* water */
    --accent-hover: #2c5878;     /* water-deep */
    --border-color: #e4dccd;     /* paper-edge */
    --hero-from: #3f86c0;
    --hero-to: #2c5878;
    --clay: #c06a3f;             /* clay — scarcity/alarm */
}
.stApp { background: var(--bg-primary) !important; }
[data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
</style>
"""

_DARK = """
<style>
:root {
    /* Water on Paper — water-ink dark palette (matches section.dark in essay) */
    --bg-primary: #22394e;       /* water-ink */
    --bg-secondary: #1a2c3d;     /* darker variant */
    --bg-card: #2c5878;          /* water-deep panel */
    --bg-banner: rgba(63,134,192,0.18);
    --text-primary: #f9f4ec;     /* paper */
    --text-secondary: #c8b8a0;   /* soft paper */
    --text-faint: #80828a;
    --accent: #5fa5d8;           /* lifted water for contrast */
    --accent-hover: #7ec0e8;
    --border-color: #34536c;
    --hero-from: #2c5878;
    --hero-to: #22394e;
    --clay: #d97f4a;
}
.stApp, body {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
[data-testid="stSidebar"] *, .stMarkdown, .stMarkdown p, .stMarkdown li,
h1, h2, h3, h4, h5, h6, label {
    color: var(--text-primary) !important;
}
.stCaption, [data-testid="stCaptionContainer"], small,
.pukhuri-card p {
    color: var(--text-secondary) !important;
}

/* Page links: high-contrast in dark */
[data-testid="stPageLink"] {
    background: var(--bg-banner) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
}
[data-testid="stPageLink"] *,
[data-testid="stPageLink"] p,
[data-testid="stPageLink"] span,
[data-testid="stPageLink"] a {
    color: var(--accent) !important;
    font-weight: 500 !important;
}
[data-testid="stPageLink"]:hover {
    background: var(--bg-secondary) !important;
}

/* Inputs */
[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea,
.stNumberInput input, [data-baseweb="popover"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}
[data-baseweb="select"] [data-baseweb="tag"] { background: var(--bg-secondary) !important; }
[data-baseweb="menu"] { background: var(--bg-card) !important; }
[data-baseweb="menu"] li { color: var(--text-primary) !important; }
[data-baseweb="menu"] li:hover { background: var(--bg-secondary) !important; }

code, pre { background: var(--bg-secondary) !important; color: #cbd5e1 !important; }

[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
}
[data-testid="stAlert"] * { color: var(--text-primary) !important; }
[data-testid="stAlert"] svg { fill: var(--accent) !important; }

/* Streamlit success/info/warning/error band colors (left accent) */
[data-baseweb="notification"] { background: var(--bg-card) !important; }
[data-baseweb="notification"] * { color: var(--text-primary) !important; }

/* Markdown blockquote */
[data-testid="stMarkdownContainer"] blockquote,
.stMarkdown blockquote {
    background: var(--bg-card) !important;
    border-left: 3px solid var(--accent) !important;
    color: var(--text-secondary) !important;
    padding: 0.5rem 1rem !important;
    border-radius: 4px;
}

/* Dataframe cells / headers */
[data-testid="stDataFrame"], [data-testid="stDataFrame"] * {
    background-color: transparent !important;
    color: var(--text-primary) !important;
}
[data-testid="stDataFrame"] [role="row"]:nth-child(odd) { background: var(--bg-card) !important; }
[data-testid="stDataFrame"] [role="columnheader"] {
    background: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
}

/* Bar chart axis text */
.vega-embed text, .vega-embed .role-axis-label text {
    fill: var(--text-secondary) !important;
}

/* Tabs */
.stTabs [aria-selected="true"] { color: var(--accent) !important; }
.stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; }

/* Toggle switch (dark mode toggle itself) */
[data-baseweb="checkbox"] [role="checkbox"] { background: var(--bg-card) !important; }

/* Expander body text */
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] *,
[data-testid="stExpander"] li, [data-testid="stExpander"] p {
    color: var(--text-primary) !important;
}

/* Captions inside expanders / containers */
[data-testid="stCaptionContainer"] * { color: var(--text-secondary) !important; }

/* Generic `b`/`strong` */
strong, b { color: var(--text-primary) !important; }

/* Table inside markdown (used on Contaminants/Groundwater pages) */
[data-testid="stMarkdownContainer"] table { color: var(--text-primary) !important; }
[data-testid="stMarkdownContainer"] th { background: var(--bg-secondary) !important; color: var(--text-secondary) !important; }
[data-testid="stMarkdownContainer"] td { border-color: var(--border-color) !important; }

/* Anchor link icon next to headings */
h1 a, h2 a, h3 a, h4 a { color: var(--accent) !important; }

/* Number input arrows */
.stNumberInput button { background: var(--bg-secondary) !important; color: var(--text-primary) !important; }

/* Banner — make sure nested elements stay on the dark card */
.pukhuri-banner, .pukhuri-banner * {
    color: var(--text-primary) !important;
    background: transparent !important;
}
.pukhuri-banner { background: var(--bg-banner) !important; }

/* Cards in dark — ensure inner text picks up */
.pukhuri-card, .pukhuri-card * { color: var(--text-primary) !important; }
.pukhuri-card p { color: var(--text-secondary) !important; }
</style>
"""


# ---------------------------------------------------------------------------
# Public helpers


def init_page(*, title: str, icon: str = "💧", layout: str = "wide") -> None:
    """Single-call setup for every page."""
    st.set_page_config(
        page_title=f"{title} — Neer",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": None,
            "Report a bug": None,
            "About": "Neer — know your water in India. A Water on Paper companion.",
        },
    )
    _init_state()
    _sync_from_query_params()
    _inject_css()
    _render_sidebar()


def render_map(fmap, *, height: int = 560) -> None:
    """Render a folium.Map without the streamlit-folium dependency."""
    components.html(fmap._repr_html_(), height=height + 8, scrolling=False)


def feature_card(*, icon: str, title: str, body: str, page: str, link_label: str) -> None:
    """A clean feature card with a Material Symbols icon and a page link."""
    icon_html = f'<span class="material-symbols-outlined">{icon}</span>'
    html = (
        '<div class="pukhuri-card">'
        f'<div class="icon">{icon_html}</div>'
        f'<h3>{title}</h3>'
        f'<p>{body}</p>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
    st.page_link(page, label=link_label)


def section_banner(text: str) -> None:
    st.markdown(f'<div class="pukhuri-banner">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Inline SVG illustrations
#
# We use inline SVG (not external images) so they:
# - work offline / on any deploy target
# - inherit theme colours via currentColor / CSS vars
# - never 404
#
# Each function returns a self-contained <svg> string. Pass to st.markdown
# with unsafe_allow_html=True or wrap with `illustration(...)` for sizing.

ILLUSTRATIONS: dict[str, str] = {
    # A handpump silhouette + water — for Map / source pages
    "handpump": """<svg viewBox="0 0 240 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="170" width="240" height="30" fill="var(--bg-banner)"/>
        <path d="M40 170 L40 90 L60 90 L60 170 Z" fill="var(--accent)" opacity="0.9"/>
        <path d="M60 110 L130 110 L130 100 L60 100 Z" fill="var(--accent)" opacity="0.7"/>
        <path d="M130 80 L160 60 L170 70 L140 90 Z" fill="var(--accent)" opacity="0.85"/>
        <circle cx="50" cy="80" r="14" fill="var(--accent)"/>
        <path d="M48 130 Q 60 145 50 165 Q 40 145 48 130 Z" fill="#38bdf8" opacity="0.85"/>
        <path d="M44 158 Q 50 168 56 158" stroke="#0ea5e9" stroke-width="2" fill="none"/>
    </svg>""",
    # Test tube / lab — for Contaminants
    "lab": """<svg viewBox="0 0 240 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="170" width="240" height="30" fill="var(--bg-banner)"/>
        <path d="M90 30 L90 130 a25 25 0 0 0 50 0 L140 30 Z" fill="none" stroke="var(--accent)" stroke-width="3"/>
        <path d="M90 100 L140 100 L140 130 a25 25 0 0 1 -50 0 Z" fill="var(--accent)" opacity="0.6"/>
        <circle cx="105" cy="115" r="3" fill="#ffffff" opacity="0.8"/>
        <circle cx="120" cy="125" r="2" fill="#ffffff" opacity="0.6"/>
        <line x1="80" y1="30" x2="150" y2="30" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>
        <path d="M170 60 l 8 0 l 0 8 l 8 0 l 0 8 l -8 0 l 0 8 l -8 0 l 0 -8 l -8 0 l 0 -8 l 8 0 Z" fill="var(--accent)" opacity="0.5"/>
    </svg>""",
    # Document with stamp — for Grievance
    "document": """<svg viewBox="0 0 240 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="170" width="240" height="30" fill="var(--bg-banner)"/>
        <rect x="60" y="20" width="120" height="150" rx="6" fill="var(--bg-card)" stroke="var(--border-color)" stroke-width="2"/>
        <line x1="80" y1="50" x2="160" y2="50" stroke="var(--text-secondary)" stroke-width="3" stroke-linecap="round"/>
        <line x1="80" y1="70" x2="160" y2="70" stroke="var(--text-secondary)" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <line x1="80" y1="85" x2="140" y2="85" stroke="var(--text-secondary)" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <line x1="80" y1="100" x2="155" y2="100" stroke="var(--text-secondary)" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
        <circle cx="155" cy="135" r="20" fill="none" stroke="var(--accent)" stroke-width="2" opacity="0.85"/>
        <text x="155" y="140" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" font-weight="700" fill="var(--accent)">FILED</text>
    </svg>""",
    # Aquifer cross-section — for Groundwater
    "aquifer": """<svg viewBox="0 0 240 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="240" height="60" fill="var(--bg-banner)" opacity="0.6"/>
        <path d="M0 60 Q 60 50 120 60 T 240 60 L 240 80 L 0 80 Z" fill="#a3a3a3" opacity="0.5"/>
        <path d="M0 80 Q 60 70 120 80 T 240 80 L 240 130 L 0 130 Z" fill="var(--accent)" opacity="0.55"/>
        <path d="M0 130 L 240 130 L 240 200 L 0 200 Z" fill="#737373" opacity="0.4"/>
        <rect x="105" y="20" width="6" height="100" fill="#475569"/>
        <rect x="100" y="14" width="16" height="10" fill="#475569"/>
        <line x1="108" y1="120" x2="108" y2="135" stroke="#0ea5e9" stroke-width="3"/>
        <text x="120" y="100" font-family="Inter,sans-serif" font-size="10" fill="#ffffff" opacity="0.85">aquifer</text>
        <text x="120" y="160" font-family="Inter,sans-serif" font-size="10" fill="#ffffff" opacity="0.7">bedrock</text>
    </svg>""",
}


def illustration(key: str, *, height: int = 160) -> None:
    """Render one of the named inline SVG illustrations."""
    svg = ILLUSTRATIONS.get(key)
    if not svg:
        return
    st.markdown(
        _flatten_html(
            f'<div style="height:{height}px;display:flex;align-items:center;'
            f'justify-content:center;margin:0 0 1rem 0;">{svg}</div>'
        ),
        unsafe_allow_html=True,
    )


def page_header(
    title: str,
    *,
    illustration_key: str | None = None,
    caption: str | None = None,
    photo: str | None = None,
    photo_credit: str | None = None,
    photo_credit_url: str | None = None,
) -> None:
    """Consistent page header.

    Priority: photo (if `photo` resolves) > inline-SVG illustration > plain title.
    """
    photo_uri = _cached_img_uri(str(PHOTOS_DIR / photo)) if photo else None

    if photo_uri:
        bg = (
            "linear-gradient(120deg, rgba(2,28,56,0.6) 0%, rgba(2,77,135,0.45) 100%), "
            f"url('{photo_uri}')"
        )
        cap_html = f'<div class="page-caption">{caption}</div>' if caption else ""
        html = (
            f'<div class="pukhuri-page-photo" style="background-image:{bg};">'
            f'<h1>{title}</h1>'
            f'{cap_html}'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)
        if photo_credit:
            credit = (
                f"[{photo_credit}]({photo_credit_url})"
                if photo_credit_url
                else photo_credit
            )
            st.caption(f"Photo: {credit}")
        return

    if illustration_key and illustration_key in ILLUSTRATIONS:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"# {title}")
            if caption:
                st.caption(caption)
        with c2:
            st.markdown(
                _flatten_html(
                    f'<div style="height:120px;display:flex;align-items:center;'
                    f'justify-content:flex-end;">{ILLUSTRATIONS[illustration_key]}</div>'
                ),
                unsafe_allow_html=True,
            )
    else:
        st.markdown(f"# {title}")
        if caption:
            st.caption(caption)


def hero(
    *,
    title: str,
    subtitle: str,
    badge: str | None = None,
    photo: str | None = "hero.jpg",
    photo_credit: str | None = None,
    photo_credit_url: str | None = None,
) -> None:
    """Decorative hero block.

    If `photo` resolves to an existing file in `assets/photos/`, render with that as a
    full-bleed background; otherwise fall back to the inline SVG water motif.
    """
    badge_html = (
        f'<div class="badge-row"><span class="pukhuri-badge">{badge}</span></div>'
        if badge
        else ""
    )
    photo_uri = _cached_img_uri(str(PHOTOS_DIR / photo)) if photo else None

    if photo_uri:
        credit_html = ""
        if photo_credit:
            credit_inner = (
                f'<a href="{photo_credit_url}" target="_blank" rel="noopener">{photo_credit}</a>'
                if photo_credit_url
                else photo_credit
            )
            credit_html = f'<div class="hero-credit">Photo: {credit_inner}</div>'
        bg = (
            "linear-gradient(135deg, rgba(2,28,56,0.62) 0%, rgba(2,77,135,0.55) 100%), "
            f"url('{photo_uri}')"
        )
        html = (
            f'<div class="pukhuri-hero pukhuri-hero--photo" style="background-image:{bg};">'
            f'<h1>{title}</h1>'
            f'<div class="subtitle">{subtitle}</div>'
            f'{badge_html}'
            f'{credit_html}'
            '</div>'
        )
    else:
        art = (
            '<svg class="bg-art" width="380" height="380" viewBox="0 0 380 380" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="dropG" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>'
            '<stop offset="100%" stop-color="#ffffff" stop-opacity="0.4"/>'
            '</linearGradient></defs>'
            '<path d="M190 30 C 110 130, 70 200, 70 250 a120 120 0 0 0 240 0 C 310 200, 270 130, 190 30 Z" fill="url(#dropG)"/>'
            '<path d="M40 320 Q 95 295 150 320 T 260 320 T 360 320" stroke="#ffffff" stroke-width="3" stroke-opacity="0.45" fill="none"/>'
            '<path d="M20 350 Q 80 325 140 350 T 250 350 T 360 350" stroke="#ffffff" stroke-width="2" stroke-opacity="0.3" fill="none"/>'
            '</svg>'
        )
        html = (
            '<div class="pukhuri-hero">'
            f'{art}'
            f'<h1>{title}</h1>'
            f'<div class="subtitle">{subtitle}</div>'
            f'{badge_html}'
            '</div>'
        )
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Internal


def _init_state() -> None:
    st.session_state.setdefault("dark_mode", False)
    st.session_state.setdefault("lang", "en")
    st.session_state.setdefault("state", None)
    st.session_state.setdefault("district", None)


def _sync_from_query_params() -> None:
    """Read `?state=&district=&lang=&dark=` deep-links into session state.

    Runs **once per session** (guarded by `_qp_synced`). After that, session state
    is the source of truth — otherwise toggles get clobbered on rerun by the URL
    that we ourselves last pushed there.
    """
    if st.session_state.get("_qp_synced"):
        return
    st.session_state["_qp_synced"] = True

    qp = st.query_params
    if "state" in qp and not st.session_state.get("state"):
        st.session_state["state"] = qp.get("state")
    if "district" in qp and not st.session_state.get("district"):
        st.session_state["district"] = qp.get("district")
    if "lang" in qp:
        lang = qp.get("lang")
        if lang in {"en", "hi", "ta", "as"}:
            st.session_state["lang"] = lang
    if "dark" in qp:
        st.session_state["dark_mode"] = qp.get("dark") in {"1", "true", "yes"}


def _push_query_params() -> None:
    """Mirror selected state/district to URL so the link is shareable."""
    qp = {}
    if st.session_state.get("state"):
        qp["state"] = st.session_state["state"]
    if st.session_state.get("district"):
        qp["district"] = st.session_state["district"]
    if st.session_state.get("lang") and st.session_state["lang"] != "en":
        qp["lang"] = st.session_state["lang"]
    if st.session_state.get("dark_mode"):
        qp["dark"] = "1"
    try:
        st.query_params.clear()
        for k, v in qp.items():
            st.query_params[k] = v
    except Exception:
        pass  # query_params API varies slightly across versions


def _inject_css() -> None:
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    st.markdown(_DARK if st.session_state.get("dark_mode") else _LIGHT, unsafe_allow_html=True)


def _render_sidebar() -> None:
    states_df = load_states()
    districts_df = load_districts()

    with st.sidebar:
        st.markdown("### Neer · नीर")
        st.caption("Know your water — India · Water on Paper series")
        st.page_link("Home.py", label="← Water on Paper (essay)", icon=":material/menu_book:")

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
        st.session_state["lang"] = lang_choice

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
            districts_for_state = sorted(
                districts_df[districts_df["state"] == st.session_state["state"]]["district"].tolist()
            )
            d_opts = ["—"] + districts_for_state
            cur_d = st.session_state.get("district") or "—"
            d = st.selectbox(
                "District (type to search)",
                d_opts,
                index=d_opts.index(cur_d) if cur_d in d_opts else 0,
                label_visibility="collapsed",
                placeholder="Type to search…",
                key="_district_select",
            )
            st.session_state["district"] = None if d == "—" else d

        st.divider()
        st.caption(
            "Districts in our snapshot only. Others fall back to state-level. "
            "Absence ≠ safety — always test your own water."
        )

        # Push state to URL after widgets resolve.
        _push_query_params()
