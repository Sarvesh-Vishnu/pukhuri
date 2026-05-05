"""Translation dictionary. English + Hindi shipped; Tamil/Assamese stubbed.

Translation falls back to English for any missing key, so partial language
packs don't break the UI.
"""
from __future__ import annotations

LANGS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "Pukhuri — Know Your Water",
        "app_tagline": "Where does your water come from? What's in it? Who do you talk to when something's wrong?",
        "nav_map": "Map & Source",
        "nav_contaminants": "Contaminants & Restoration",
        "nav_grievance": "Grievance Drafter",
        "nav_groundwater": "Groundwater & Demand",
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
        "download_pdf": "Download as PDF",
        "best_practices": "Best practices for households",
        "treatment_household": "Household treatment options",
        "treatment_community": "Community / scheme-level treatment",
        "health_effects": "Health effects",
        "bis_limits": "BIS 10500:2012 limits (drinking water)",
        "data_sources": "Data sources & snapshot date",
    },
    # ---- Hindi ----------------------------------------------------------
    "hi": {
        "app_title": "पुखुरी — अपना पानी जानें",
        "app_tagline": (
            "आपका पानी कहाँ से आता है? उसमें क्या है? कुछ गलत होने पर आप किससे बात करते हैं?"
        ),
        "nav_map": "मानचित्र और स्रोत",
        "nav_contaminants": "संदूषक और पुनर्स्थापना",
        "nav_grievance": "शिकायत प्रारूपक",
        "nav_groundwater": "भूजल और माँग",
        "select_state": "राज्य / केंद्र शासित प्रदेश",
        "select_district": "ज़िला (वैकल्पिक)",
        "snapshot_warning": (
            "यह साइट CGWB, CPCB, BIS 10500:2012, जल जीवन मिशन, AMRUT, नमामि गंगे "
            "और राज्य PHED वेबसाइटों से सार्वजनिक डेटा का एक संकलित **स्नैपशॉट** उपयोग करती है। "
            "स्नैपशॉट दिनांक और स्रोत प्रत्येक पृष्ठ के नीचे सूचीबद्ध हैं। "
            "किसी आपातकाल या वर्तमान पानी की गुणवत्ता के लिए, अपने स्थानीय प्राधिकरण से सीधे संपर्क करें।"
        ),
        "contaminants_label": "ज्ञात संदूषक",
        "source_label": "मुख्य स्रोत",
        "basin_label": "नदी बेसिन",
        "rivers_label": "प्रमुख नदियाँ",
        "jjm_coverage": "JJM (ग्रामीण नल) कवरेज",
        "no_district_data": (
            "इस ज़िले के लिए अभी ज़िला-स्तरीय स्नैपशॉट उपलब्ध नहीं है — राज्य-स्तरीय प्रोफ़ाइल दिखा रहे हैं।"
        ),
        "issue_type": "समस्या क्या है?",
        "issue_no_supply": "पानी की आपूर्ति नहीं / बाधित",
        "issue_quality": "पानी की गुणवत्ता / संदूषण",
        "issue_leakage": "रिसाव / पाइप फटना / बर्बादी",
        "issue_billing": "बिलिंग / कनेक्शन / मीटरिंग",
        "issue_other": "अन्य",
        "draft_complaint": "मेरी शिकायत तैयार करें",
        "copy_complaint": "क्लिपबोर्ड पर कॉपी करें",
        "download_pdf": "PDF के रूप में डाउनलोड करें",
        "best_practices": "घरेलू उपयोग के लिए सर्वोत्तम प्रथाएँ",
        "treatment_household": "घरेलू उपचार विकल्प",
        "treatment_community": "सामुदायिक / योजना-स्तरीय उपचार",
        "health_effects": "स्वास्थ्य प्रभाव",
        "bis_limits": "BIS 10500:2012 सीमाएँ (पीने का पानी)",
        "data_sources": "डेटा स्रोत और स्नैपशॉट दिनांक",
    },
    "ta": {},
    "as": {},
}

LANG_LABELS = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "ta": "தமிழ் (Tamil) — coming soon",
    "as": "অসমীয়া (Assamese) — coming soon",
}


def t(key: str, lang: str = "en") -> str:
    """Look up a translation; fall back to English then to the key itself."""
    return LANGS.get(lang, {}).get(key) or LANGS["en"].get(key, key)
