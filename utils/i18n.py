"""Translation stub. English filled in for v1.

Hindi (hi), Tamil (ta), and a North-East language (Assamese, as) are stubbed —
add translations to LANGS[<code>] to enable. Falls back to English for missing keys.
"""
from __future__ import annotations

LANGS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "Pukhuri — Know Your Water",
        "app_tagline": "Where does your water come from? What's in it? Who do you talk to when something's wrong?",
        "nav_map": "Map & Source",
        "nav_contaminants": "Contaminants & Restoration",
        "nav_grievance": "Grievance Drafter",
        "select_state": "State / UT",
        "select_district": "District (optional)",
        "snapshot_warning": (
            "This site uses a curated **snapshot** of public-domain data from CGWB, "
            "CPCB, BIS 10500:2012, Jal Jeevan Mission, AMRUT, Namami Gange, and state PHED websites. "
            "Snapshot date and sources are listed at the bottom of each page. "
            "For an emergency or current-day water quality, contact your local authority directly."
        ),
        "contaminants_label": "Known contaminants",
        "source_label": "Dominant source",
        "basin_label": "River basin",
        "rivers_label": "Major rivers",
        "jjm_coverage": "JJM (rural tap) coverage",
        "no_district_data": "No district-level snapshot for this district yet — showing state-level profile.",
        "issue_type": "What is the issue?",
        "issue_no_supply": "No water supply / interruption",
        "issue_quality": "Water quality / contamination",
        "issue_leakage": "Leakage / pipe burst / wastage",
        "issue_billing": "Billing / connection / metering",
        "issue_other": "Other",
        "draft_complaint": "Draft my complaint",
        "copy_complaint": "Copy to clipboard",
        "best_practices": "Best practices for households",
        "treatment_household": "Household treatment options",
        "treatment_community": "Community / scheme-level treatment",
        "health_effects": "Health effects",
        "bis_limits": "BIS 10500:2012 limits (drinking water)",
        "data_sources": "Data sources & snapshot date",
    },
    "hi": {},
    "ta": {},
    "as": {},
}

LANG_LABELS = {
    "en": "English",
    "hi": "हिन्दी (Hindi) — coming soon",
    "ta": "தமிழ் (Tamil) — coming soon",
    "as": "অসমীয়া (Assamese) — coming soon",
}


def t(key: str, lang: str = "en") -> str:
    return LANGS.get(lang, {}).get(key) or LANGS["en"].get(key, key)
