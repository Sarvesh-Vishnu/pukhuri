"""Translation dictionary. English + Hindi + Tamil + Assamese.

Translation falls back to English for any missing key, so partial language
packs don't break the UI.

The Tamil and Assamese packs were drafted carefully but should ideally be
reviewed by a native speaker before being treated as final — flag issues at
the repo's GitHub mirror.
"""
from __future__ import annotations

LANGS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "Neer — Know Your Water",
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
        "app_title": "नीर — अपना पानी जानें",
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
    # ---- Tamil ----------------------------------------------------------
    "ta": {
        "app_title": "நீர் — உங்கள் தண்ணீரை அறியுங்கள்",
        "app_tagline": (
            "உங்கள் தண்ணீர் எங்கிருந்து வருகிறது? அதில் என்ன உள்ளது? "
            "ஏதாவது தவறு நடந்தால் யாரிடம் பேசுவீர்கள்?"
        ),
        "nav_map": "வரைபடம் & மூலம்",
        "nav_contaminants": "மாசுக்கள் & மறுசீரமைப்பு",
        "nav_grievance": "முறையீட்டு வரைவாளர்",
        "nav_groundwater": "நிலத்தடி நீர் & தேவை",
        "select_state": "மாநிலம் / யூ.டி.",
        "select_district": "மாவட்டம் (விருப்பத்தேர்வு)",
        "snapshot_warning": (
            "இந்த தளம் CGWB, CPCB, BIS 10500:2012, ஜல் ஜீவன் மிஷன், AMRUT, நமாமி கங்கே "
            "மற்றும் மாநில PHED இணையதளங்களின் பொது தரவுகளின் ஒரு தொகுக்கப்பட்ட **ஸ்னாப்ஷாட்** "
            "ஐ பயன்படுத்துகிறது. ஸ்னாப்ஷாட் தேதி மற்றும் மூலங்கள் ஒவ்வொரு பக்கத்தின் கீழும் "
            "பட்டியலிடப்பட்டுள்ளன. அவசர காலம் அல்லது தற்போதைய நீரின் தரத்திற்கு, உங்கள் "
            "உள்ளூர் அதிகாரத்தை நேரடியாக தொடர்பு கொள்ளவும்."
        ),
        "contaminants_label": "அறியப்பட்ட மாசுக்கள்",
        "source_label": "முக்கிய மூலம்",
        "basin_label": "ஆற்றுப்படுகை",
        "rivers_label": "முக்கிய ஆறுகள்",
        "jjm_coverage": "JJM (கிராமப்புற குழாய்) கவரேஜ்",
        "no_district_data": (
            "இந்த மாவட்டத்திற்கு மாவட்ட-நிலை ஸ்னாப்ஷாட் இன்னும் இல்லை — மாநில-நிலை சுயவிவரத்தைக் காட்டுகிறோம்."
        ),
        "issue_type": "என்ன பிரச்சினை?",
        "issue_no_supply": "தண்ணீர் சப்ளை இல்லை / குறுக்கீடு",
        "issue_quality": "தண்ணீரின் தரம் / மாசுபாடு",
        "issue_leakage": "கசிவு / குழாய் வெடிப்பு / வீணாதல்",
        "issue_billing": "பில்லிங் / இணைப்பு / மீட்டரிங்",
        "issue_other": "மற்றவை",
        "draft_complaint": "என் முறையீட்டை தயார் செய்க",
        "copy_complaint": "கிளிப்போர்டிற்கு நகலெடுக்கவும்",
        "download_pdf": "PDF ஆக பதிவிறக்கம் செய்க",
        "best_practices": "வீட்டு பயன்பாட்டிற்கான சிறந்த நடைமுறைகள்",
        "treatment_household": "வீட்டு சிகிச்சை விருப்பங்கள்",
        "treatment_community": "சமூக / திட்ட-நிலை சிகிச்சை",
        "health_effects": "உடல்நலன் விளைவுகள்",
        "bis_limits": "BIS 10500:2012 வரம்புகள் (குடிநீர்)",
        "data_sources": "தரவு மூலங்கள் & ஸ்னாப்ஷாட் தேதி",
    },
    # ---- Assamese ------------------------------------------------------
    "as": {
        "app_title": "পুখুৰী — আপোনাৰ পানীক জানক",
        "app_tagline": (
            "আপোনাৰ পানী ক'ৰপৰা আহে? তাত কি আছে? কিবা এটা ভুল হ'লে আপুনি কাৰ লগত কথা পাতে?"
        ),
        "nav_map": "মানচিত্ৰ আৰু উৎস",
        "nav_contaminants": "প্ৰদূষক আৰু পুনৰুদ্ধাৰ",
        "nav_grievance": "অভিযোগ প্ৰাৰূপক",
        "nav_groundwater": "ভূগৰ্ভস্থ পানী আৰু চাহিদা",
        "select_state": "ৰাজ্য / কেন্দ্ৰীয় শাসিত প্ৰদেশ",
        "select_district": "জিলা (বিকল্পীয়)",
        "snapshot_warning": (
            "এই ছাইটে CGWB, CPCB, BIS 10500:2012, জল জীৱন মিছন, AMRUT, নমামি গংগে "
            "আৰু ৰাজ্যিক PHED ৱেবছাইটসমূহৰপৰা পোৱা ৰাজহুৱা ডেটাৰ এটা সংকলিত **স্নেপশ্বট** "
            "ব্যৱহাৰ কৰে। স্নেপশ্বটৰ তাৰিখ আৰু উৎস প্ৰতিটো পৃষ্ঠাৰ তলত তালিকাভুক্ত আছে। "
            "জৰুৰীকালীন অৱস্থা বা বৰ্তমানৰ পানীৰ মান জানিবলৈ, আপোনাৰ স্থানীয় কৰ্তৃপক্ষৰ "
            "লগত পোনপটীয়াকৈ যোগাযোগ কৰক।"
        ),
        "contaminants_label": "জ্ঞাত প্ৰদূষক",
        "source_label": "মুখ্য উৎস",
        "basin_label": "নদী অববাহিকা",
        "rivers_label": "মুখ্য নদীসমূহ",
        "jjm_coverage": "JJM (গ্ৰাম্য টেপ) কভাৰেজ",
        "no_district_data": (
            "এই জিলাৰ বাবে এতিয়াও জিলা-স্তৰৰ স্নেপশ্বট নাই — ৰাজ্য-স্তৰৰ প্ৰফাইল দেখুৱাইছোঁ।"
        ),
        "issue_type": "সমস্যা কি?",
        "issue_no_supply": "পানী যোগান নাই / বাধাগ্ৰস্ত",
        "issue_quality": "পানীৰ গুণাগুণ / প্ৰদূষণ",
        "issue_leakage": "লিকেজ / পাইপ ফাটি যোৱা / অপচয়",
        "issue_billing": "বিলিং / সংযোগ / মিটাৰিং",
        "issue_other": "অন্যান্য",
        "draft_complaint": "মোৰ অভিযোগ প্ৰাৰূপ কৰক",
        "copy_complaint": "ক্লিপবৰ্ডলৈ কপি কৰক",
        "download_pdf": "PDF হিচাপে ডাউনল'ড কৰক",
        "best_practices": "ঘৰুৱা ব্যৱহাৰৰ বাবে শ্ৰেষ্ঠ অভ্যাস",
        "treatment_household": "ঘৰুৱা চিকিৎসা বিকল্পসমূহ",
        "treatment_community": "সামূহিক / আঁচনি-স্তৰৰ চিকিৎসা",
        "health_effects": "স্বাস্থ্যৰ ওপৰত প্ৰভাৱ",
        "bis_limits": "BIS 10500:2012 সীমাসমূহ (পানযোগ্য পানী)",
        "data_sources": "তথ্য উৎস আৰু স্নেপশ্বট তাৰিখ",
    },
}

LANG_LABELS = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "ta": "தமிழ் (Tamil)",
    "as": "অসমীয়া (Assamese)",
}


def t(key: str, lang: str = "en") -> str:
    """Look up a translation; fall back to English then to the key itself."""
    return LANGS.get(lang, {}).get(key) or LANGS["en"].get(key, key)
