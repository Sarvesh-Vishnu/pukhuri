"""Pukhuri — Know Your Water (India). Streamlit entrypoint.

Run: `streamlit run app.py` from the water-india/ directory.
"""
from __future__ import annotations

import streamlit as st

from utils.data_loader import load_districts, load_states
from utils.i18n import LANG_LABELS, t

st.set_page_config(
    page_title="Pukhuri — Know Your Water",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session() -> None:
    st.session_state.setdefault("lang", "en")
    st.session_state.setdefault("state", None)
    st.session_state.setdefault("district", None)


def sidebar_selectors() -> None:
    states_df = load_states()
    districts_df = load_districts()

    with st.sidebar:
        st.markdown("### 🌐 Language")
        lang_code = st.selectbox(
            "Language",
            options=list(LANG_LABELS.keys()),
            format_func=lambda c: LANG_LABELS[c],
            index=list(LANG_LABELS.keys()).index(st.session_state["lang"]),
            label_visibility="collapsed",
        )
        st.session_state["lang"] = lang_code if lang_code == "en" else "en"
        if lang_code != "en":
            st.caption("Translation pack not yet bundled — falling back to English.")

        st.markdown("---")
        st.markdown(f"### 📍 {t('select_state', st.session_state['lang'])}")

        state_options = ["—"] + sorted(states_df["state"].unique().tolist())
        cur_state_idx = state_options.index(st.session_state["state"]) if st.session_state["state"] in state_options else 0
        state = st.selectbox("State", state_options, index=cur_state_idx, label_visibility="collapsed")
        st.session_state["state"] = None if state == "—" else state

        if st.session_state["state"]:
            d_opts = ["—"] + sorted(
                districts_df[districts_df["state"] == st.session_state["state"]]["district"].tolist()
            )
            cur_d_idx = d_opts.index(st.session_state["district"]) if st.session_state["district"] in d_opts else 0
            st.markdown(f"### 🏘️ {t('select_district', st.session_state['lang'])}")
            d = st.selectbox("District", d_opts, index=cur_d_idx, label_visibility="collapsed")
            st.session_state["district"] = None if d == "—" else d

        st.markdown("---")
        st.caption(
            "Districts shown are the ones in our curated snapshot. "
            "If your district is not listed, you'll see state-level information."
        )


def main() -> None:
    init_session()
    sidebar_selectors()
    lang = st.session_state["lang"]

    st.title(f"💧 {t('app_title', lang)}")
    st.markdown(f"#### {t('app_tagline', lang)}")
    st.warning(t("snapshot_warning", lang))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🗺️ Map & Source")
        st.markdown(
            "Pick your state and district to see your dominant water source, "
            "the river basin you're in, and which districts have known contamination issues."
        )
        st.page_link("pages/1_Map_and_Source.py", label="Open the map →", icon="🗺️")

        st.markdown("### 🧪 Contaminants & Restoration")
        st.markdown(
            "Learn what fluoride, arsenic, nitrate, iron, salinity, uranium and microbial contamination "
            "do to health — and how households, communities, and government schemes treat each."
        )
        st.page_link("pages/2_Contaminants_and_Restoration.py", label="Read the guide →", icon="🧪")
    with col2:
        st.markdown("### 📉 Groundwater, Reservoirs & Data Centres")
        st.markdown(
            "See how stressed your state's groundwater is (CGWB), the reservoirs that buffer your supply (CWC), "
            "and the data-centre footprint sitting on top — much of it in already-stressed corridors."
        )
        st.page_link("pages/4_Groundwater_and_Demand.py", label="See the stress map →", icon="📉")

        st.markdown("### ✍️ Grievance Drafter")
        st.markdown(
            "Draft a formal water complaint addressed to the right authority for your state — "
            "rural PHED, urban water board, or state grievance portal — with CPGRAMS as the escalation path."
        )
        st.page_link("pages/3_Grievance_Drafter.py", label="Draft a complaint →", icon="✍️")

    st.markdown("---")
    st.subheader("Why this site")
    st.markdown(
        """
- **Built for India.** Data comes from the Central Ground Water Board (CGWB), the Central Pollution
  Control Board (CPCB), the Bureau of Indian Standards (IS 10500:2012), the Jal Jeevan Mission
  dashboard, and state Public Health Engineering Department (PHED) websites.
- **District-level honesty.** Going below district level (block / village) requires data we don't have.
  If your district has known contamination, we surface it from CGWB Ground Water Year Book reports.
  If a district isn't in our snapshot, that **does not mean it's safe** — it means we don't have
  district-level evidence of contamination for it. Always test your own water before relying on it.
- **Snapshot, not live.** Government APIs are unreliable; CGWB publishes annually anyway. We snapshot
  the data and tell you when. Re-snapshot scripts live in `scripts/`.
- **No automation of grievances.** We draft and route — *you* file. Accountability for a government
  complaint should always rest with the citizen who signs it.
        """.strip()
    )

    with st.expander("📚 Data sources & snapshot date"):
        st.markdown(
            """
- **Snapshot date:** 2024-01-01 (state/contaminants/authorities), 2024-01-01 (district profile).
- **Bureau of Indian Standards** — IS 10500:2012, *Drinking Water Specification* (acceptable & permissible limits).
- **CGWB** — Ground Water Year Book of India (annual); *Dynamic Ground Water Resources of India 2022* (state stress); National Aquifer Mapping (NAQUIM) reports.
- **CWC** — Weekly Reservoir Storage Bulletin (Central Water Commission), capacity figures from dam-safety records.
- **CPCB** — Water Quality Monitoring Network; designated best-use river classification.
- **Jal Jeevan Mission dashboard** — `ejalshakti.gov.in/jjmreport/JJMIndia.aspx` (rural FHTC coverage).
- **NITI Aayog** — Composite Water Management Index reports (state water profile context).
- **State PHED / Water Supply Boards** — public websites, see `data/authorities.json` for per-state links.
- **CPGRAMS** — `pgportal.gov.in` (universal grievance escalation route).
- **Data centres** — operator press releases, MeitY data-centre policy notifications, and state IT/ITeS investment portals (Maharashtra, Tamil Nadu, Telangana, Karnataka, Uttar Pradesh, Gujarat). Operating + publicly-announced sites only. Water-draw figures are estimates: IT-load × 24 h × 1.8 L/kWh (industry rule-of-thumb, Uptime Institute).

Coordinates for districts, reservoirs, and data centres are approximate (district HQ / area-level, ~2 decimal places) for map markers, not survey-grade.
            """.strip()
        )


if __name__ == "__main__":
    main()
