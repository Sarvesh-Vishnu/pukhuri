"""Pukhuri — Know Your Water (India). Streamlit entrypoint.

Run: `streamlit run Home.py` from the water-india/ directory.
"""
from __future__ import annotations

import streamlit as st

from utils.theme import feature_card, init_page, section_banner

init_page(title="Home", icon="💧")


def main() -> None:
    col_title, col_meta = st.columns([3, 1])
    with col_title:
        st.markdown("# Pukhuri")
        st.markdown(
            "<p style='font-size:1.1rem;color:var(--text-secondary);margin-top:-0.4rem;'>"
            "Know your water — India.</p>",
            unsafe_allow_html=True,
        )
    with col_meta:
        st.markdown(
            "<div style='text-align:right;margin-top:0.5rem;'>"
            "<span class='pukhuri-badge'>Snapshot · 2024</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p style='font-size:1.05rem;color:var(--text-secondary);max-width:780px;'>"
        "Where does your water come from? What's in it? Who do you talk to when something's wrong? "
        "A district-level guide to India's drinking water — sources, contaminants, restoration, and "
        "grievance routing — built on public CGWB, CPCB, BIS, and CWC data."
        "</p>",
        unsafe_allow_html=True,
    )

    section_banner(
        "<strong>Snapshot, not live.</strong> Curated from CGWB, CPCB, BIS 10500:2012, Jal Jeevan Mission, "
        "AMRUT, Namami Gange, CWC reservoir bulletin, and state PHED websites. Snapshot date and per-row "
        "sources are listed at the bottom of each page. For an emergency or current-day water quality, "
        "contact your local authority directly."
    )

    # Feature grid — 2x2
    col1, col2 = st.columns(2, gap="large")
    with col1:
        feature_card(
            icon=":material/explore:",
            title="Map & Source",
            body=(
                "Pick your state and district to see your dominant water source, "
                "the river basin you're in, and which districts have known contamination."
            ),
            page="pages/1_Map_and_Source.py",
            link_label="Open the map",
        )
        feature_card(
            icon=":material/science:",
            title="Contaminants & Restoration",
            body=(
                "What fluoride, arsenic, nitrate, iron, salinity, uranium and microbial contamination "
                "do to health — and how households, communities, and government schemes treat each."
            ),
            page="pages/2_Contaminants_and_Restoration.py",
            link_label="Read the guide",
        )
    with col2:
        feature_card(
            icon=":material/trending_down:",
            title="Groundwater, Reservoirs & Data Centres",
            body=(
                "How stressed your state's groundwater is (CGWB), the reservoirs that buffer your supply (CWC), "
                "and the data-centre footprint sitting on top — much of it in already-stressed corridors."
            ),
            page="pages/4_Groundwater_and_Demand.py",
            link_label="See the stress map",
        )
        feature_card(
            icon=":material/edit_note:",
            title="Grievance Drafter",
            body=(
                "Draft a formal water complaint to the right authority for your state — rural PHED, urban "
                "water board, or grievance portal — with CPGRAMS as the universal escalation."
            ),
            page="pages/3_Grievance_Drafter.py",
            link_label="Draft a complaint",
        )

    st.markdown("## Why this site")
    st.markdown(
        """
- **Built for India.** Data comes from the Central Ground Water Board (CGWB), Central Pollution Control
  Board (CPCB), Bureau of Indian Standards (IS 10500:2012), Jal Jeevan Mission dashboard, and state
  Public Health Engineering Department (PHED) websites.
- **District-level honesty.** Going below district level (block / village) requires data we don't have.
  If your district has known contamination, we surface it from CGWB Year Books. If a district isn't in
  our snapshot, that **does not mean it's safe** — it means we don't have district-level evidence yet.
  Always test your own water before relying on it.
- **Snapshot, not live.** Government APIs are unreliable; CGWB and CWC publish at known cadences anyway.
  We snapshot the data and tell you when.
- **No automation of grievances.** We draft and route — *you* file. Accountability for a government
  complaint should always rest with the citizen who signs it.
        """.strip()
    )

    with st.expander("Data sources & snapshot date", icon=":material/library_books:"):
        st.markdown(
            """
- **Snapshot date:** 2024-01-01 (state/contaminants/authorities/districts).
- **Bureau of Indian Standards** — IS 10500:2012, *Drinking Water Specification*.
- **CGWB** — Ground Water Year Book of India (annual); *Dynamic Ground Water Resources of India 2022*
  (state stress); National Aquifer Mapping (NAQUIM) reports.
- **CWC** — Weekly Reservoir Storage Bulletin (Central Water Commission); capacity figures from public
  dam-safety records.
- **CPCB** — Water Quality Monitoring Network; designated best-use river classification.
- **Jal Jeevan Mission dashboard** — `ejalshakti.gov.in/jjmreport/JJMIndia.aspx` (rural FHTC coverage).
- **NITI Aayog** — Composite Water Management Index reports (state water profile context).
- **State PHED / Water Supply Boards** — public websites; per-state links in `data/authorities.json`.
- **CPGRAMS** — `pgportal.gov.in` (universal grievance escalation).
- **Data centres** — operator press releases, MeitY data-centre policy notifications, and state IT/ITeS
  investment portals (Maharashtra, Tamil Nadu, Telangana, Karnataka, Uttar Pradesh, Gujarat). Operating
  + publicly-announced sites only. Water-draw figures are estimates: IT-load × 24 h × 1.8 L/kWh
  (industry rule-of-thumb, Uptime Institute).

Coordinates for districts, reservoirs, and data centres are approximate (district-HQ / area-level,
~2 decimal places) — for map markers, not survey-grade.
            """.strip()
        )

    st.markdown(
        "<div style='margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border-color);"
        "color:var(--text-secondary);font-size:0.85rem;'>"
        "<strong>পুখুৰী</strong> <em>(pukhuri)</em> — Assamese for the traditional village pond. "
        "Open source, MIT licensed."
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
else:
    main()
