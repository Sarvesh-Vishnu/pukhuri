"""Contaminants & Restoration — guide page."""
from __future__ import annotations

import streamlit as st

from utils.data_loader import (
    get_district_or_state_profile,
    load_contaminants,
    load_schemes,
)
from utils.i18n import t
from utils.theme import init_page, page_header

init_page(title="Contaminants & Restoration", icon="🧪")


def best_practices_section() -> None:
    st.markdown(f"### {t('best_practices')}")
    st.markdown(
        """
- **Test before you trust.** Free testing is available at District Public Health Labs (under PHED) and
  via Field Test Kits (FTKs) distributed under Jal Jeevan Mission. ASHA workers in many states are
  trained for fluoride, arsenic, iron, nitrate, hardness, and bacterial load.
- **For boiling-eligible threats only.** Boiling for 1 minute at a rolling boil reliably kills microbes —
  but **does not remove** fluoride, arsenic, nitrate, uranium, or salinity (it can *concentrate* them).
- **Match the filter to the contaminant.**
  - *Microbial only:* boiling, chlorination, UV, or SODIS — RO is overkill.
  - *Iron / hardness:* aeration + sand filter, or activated carbon.
  - *Fluoride / arsenic / uranium / high TDS:* RO with the right membrane, **certified for the contaminant**.
  - *Nitrate:* RO or ion exchange. Boiling makes it worse.
- **Don't waste RO reject water.** A typical domestic RO wastes 3 L for every 1 L purified. Plumb the
  reject line into a storage tank for mopping, gardens, or flushing.
- **Maintain wells & overhead tanks.** Annual chlorination of dug wells, half-yearly cleaning of
  overhead tanks, and 15 m+ setback from septic tanks are the cheapest microbial controls.
- **Rainwater harvesting where viable.** First-flush diverters + filtration brings rooftop water near
  drinking standard in non-industrial areas. Many states subsidise installation.
- **Report & demand testing.** You have a right to know what's in your tap water. File for a test
  report under the Right to Public Services Act in your state, or escalate via CPGRAMS.
        """.strip()
    )


def render_contaminant(key: str, info: dict) -> None:
    with st.expander(f"{info['name']}  ·  {info['symbol']}", expanded=False):
        c1, c2 = st.columns(2)
        c1.metric("BIS acceptable (mg/L)", info["bis_acceptable_mg_l"])
        c2.metric("BIS permissible (mg/L)", info["bis_permissible_mg_l"])

        st.markdown(f"**Origin** · {info['natural_origin']}")

        st.markdown(f"**{t('health_effects')}**")
        for h in info["health_effects"]:
            st.markdown(f"- {h}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**{t('treatment_household')}**")
            for tt in info["treatment_household"]:
                st.markdown(f"- {tt}")
        with col_b:
            st.markdown(f"**{t('treatment_community')}**")
            for tt in info["treatment_community"]:
                st.markdown(f"- {tt}")

        if info.get("restoration_programmes"):
            st.markdown("**Government restoration programmes targeting this contaminant**")
            for p in info["restoration_programmes"]:
                st.markdown(f"- {p}")


def schemes_section() -> None:
    st.markdown("### National restoration & water-security programmes")
    schemes = load_schemes()
    for s in schemes["national"]:
        with st.expander(s["name"]):
            st.markdown(f"**Ministry** · {s['ministry']}")
            st.markdown(f"**Purpose** · {s['purpose']}")
            st.markdown(f"**Applies to** · `{s['applies']}`")
            st.markdown(f"[Official portal →]({s['url']})")
    st.caption(f"Schemes snapshot: {schemes['_meta']['snapshot_date']} · Source: {schemes['_meta']['source']}")


def main() -> None:
    lang = st.session_state.get("lang", "en")
    page_header(
        t("nav_contaminants", lang),
        illustration_key="lab",
        caption=(
            "Each contaminant has its BIS IS 10500:2012 drinking-water limit, its origin, the health "
            "effects of chronic exposure, what works at home and at scheme level, and the government "
            "programmes that target it."
        ),
    )

    contaminants = load_contaminants()
    order = ["arsenic", "fluoride", "uranium", "nitrate", "salinity", "iron", "microbial"]

    state = st.session_state.get("state")
    district = st.session_state.get("district")
    if state:
        prof = get_district_or_state_profile(state, district)
        user_contaminants = prof.get("primary_contaminants", [])
        if user_contaminants:
            location_label = f"{district + ', ' if district else ''}{state}"
            st.success(
                f"For **{location_label}**, the snapshot flags: "
                + ", ".join(user_contaminants)
                + ". Their entries are listed first below.",
                icon=":material/place:",
            )
            order = [c for c in user_contaminants if c in contaminants] + [
                c for c in order if c not in user_contaminants
            ]

    st.divider()
    st.markdown(f"### {t('bis_limits', lang)} & treatment by contaminant")
    for key in order:
        info = contaminants.get(key)
        if info:
            render_contaminant(key, info)

    st.divider()
    best_practices_section()

    st.divider()
    schemes_section()

    st.divider()
    st.caption(
        f"Data source: {contaminants['_meta']['source']}  ·  "
        f"Snapshot date: {contaminants['_meta']['snapshot_date']}"
    )


main()
