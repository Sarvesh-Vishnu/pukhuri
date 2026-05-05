"""Groundwater stress, reservoirs, data centres, and sectoral water demand."""
from __future__ import annotations

import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster

from utils.data_loader import (
    GW_CATEGORY_COLOR,
    estimated_dc_water_l_per_day,
    get_district_groundwater,
    get_district_or_state_profile,
    load_data_centres,
    load_district_groundwater_stress,
    load_districts,
    load_groundwater_stress,
    load_reservoirs,
    load_states,
    nearest_data_centres,
)
from utils.theme import init_page, page_header, render_map

init_page(title="Groundwater & Demand", icon="📉")

# India water demand split — NITI Aayog CWMI / Min. of Jal Shakti basin reports.
SECTORAL_DEMAND = pd.DataFrame(
    {
        "sector": ["Irrigation", "Domestic", "Industrial", "Energy & power", "Other"],
        "share_pct": [78, 6, 5, 8, 3],
    }
)


def stress_map(focus_state: str | None) -> folium.Map:
    gws = load_groundwater_stress()
    states_df = load_states()[["state", "lat", "lon"]]
    merged = states_df.merge(gws, on="state", how="left")

    center, zoom = (22.0, 80.0), 5
    if focus_state:
        row = merged[merged.state == focus_state]
        if not row.empty:
            center = (row.iloc[0]["lat"], row.iloc[0]["lon"])
            zoom = 6

    m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron", control_scale=True)

    for _, r in merged.iterrows():
        if pd.isna(r.get("stage_of_extraction_pct")):
            continue
        radius = max(8.0, min(28.0, float(r["stage_of_extraction_pct"]) / 6.0))
        color = r.get("color") or "#999999"
        notes = r.get("notes", "") if not pd.isna(r.get("notes", "")) else ""
        popup = folium.Popup(
            f"""
            <div style='font-family:sans-serif;font-size:13px;width:240px'>
              <b>{r['state']}</b><br>
              Stage of GW extraction: <b>{int(r['stage_of_extraction_pct'])}%</b><br>
              Category: <b style='color:{color}'>{r['category']}</b><br>
              <span style='color:#555'>{notes}</span>
            </div>
            """,
            max_width=260,
        )
        folium.CircleMarker(
            location=(r["lat"], r["lon"]),
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.55,
            weight=1,
            popup=popup,
            tooltip=f"{r['state']} — {int(r['stage_of_extraction_pct'])}% ({r['category']})",
        ).add_to(m)

    legend = """
    <div style="position:fixed;bottom:20px;left:20px;z-index:9999;background:rgba(255,255,255,0.92);
                padding:10px 14px;border-radius:8px;border:1px solid #ccc;font-size:12px;font-family:sans-serif">
      <b>CGWB groundwater stage</b><br>
      <span style="color:#2ca02c">●</span> Safe (&lt;70%)
      &nbsp;<span style="color:#ff7f0e">●</span> Semi-Critical (70–90%)<br>
      <span style="color:#d62728">●</span> Critical (90–100%)
      &nbsp;<span style="color:#7e1f86">●</span> Over-Exploited (&gt;100%)<br>
      <i>Bubble size scales with stage of extraction</i>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend))
    return m


def reservoirs_dc_map(focus_state: str | None, show_reservoirs: bool, show_dcs: bool) -> folium.Map:
    res = load_reservoirs()
    dcs = load_data_centres()

    center, zoom = (22.0, 80.0), 5
    if focus_state:
        sub = res[res.state == focus_state]
        if not sub.empty:
            center = (sub["lat"].mean(), sub["lon"].mean())
            zoom = 7

    m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron", control_scale=True)

    if show_reservoirs:
        cluster_r = MarkerCluster(name="Reservoirs (CWC)", show=True).add_to(m)
        for _, r in res.iterrows():
            popup = folium.Popup(
                f"""
                <div style='font-family:sans-serif;font-size:13px;width:240px'>
                  <b>{r['name']}</b><br>
                  River: {r['river']} · {r['state']}<br>
                  Live storage: <b>{r['live_storage_bcm']} BCM</b><br>
                  Purpose: {', '.join(r['purpose'])}<br>
                  <span style='color:#555'>{r.get('notes', '')}</span>
                </div>
                """,
                max_width=260,
            )
            folium.Marker(
                location=(r["lat"], r["lon"]),
                tooltip=f"💧 {r['name']} ({r['river']})",
                popup=popup,
                icon=folium.Icon(color="blue", icon="tint", prefix="fa"),
            ).add_to(cluster_r)

    if show_dcs:
        cluster_d = MarkerCluster(name="Data centres", show=True).add_to(m)
        for _, d in dcs.iterrows():
            color = {"operational": "darkgreen", "under_construction": "orange", "announced": "gray"}.get(d["status"], "gray")
            water_lpd = estimated_dc_water_l_per_day(d.get("it_load_mw"))
            water_str = f"{water_lpd/1_000_000:.2f} ML/day (estimate)" if water_lpd else "n/a"
            popup = folium.Popup(
                f"""
                <div style='font-family:sans-serif;font-size:13px;width:260px'>
                  <b>{d['name']}</b><br>
                  Operator: {d['operator']}<br>
                  {d['city']}, {d['state']} · <i>{d['status'].replace('_',' ')}</i><br>
                  IT load: <b>{d['it_load_mw']} MW</b><br>
                  Estimated water draw: <b>{water_str}</b><br>
                  <span style='color:#555'>{d.get('source_note','')}</span>
                </div>
                """,
                max_width=280,
            )
            folium.Marker(
                location=(d["lat"], d["lon"]),
                tooltip=f"🖥️ {d['name']} ({d['status']})",
                popup=popup,
                icon=folium.Icon(color=color, icon="server", prefix="fa"),
            ).add_to(cluster_d)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def stress_table() -> None:
    gws = load_groundwater_stress().sort_values("stage_of_extraction_pct", ascending=False)
    show = gws[["state", "stage_of_extraction_pct", "category", "notes"]].rename(
        columns={
            "state": "State / UT",
            "stage_of_extraction_pct": "Stage of GW extraction (%)",
            "category": "CGWB category",
            "notes": "Notes",
        }
    )

    def _row_style(row):
        color = GW_CATEGORY_COLOR.get(row["CGWB category"], "#999999")
        return [f"background-color: {color}22"] * len(row)

    st.dataframe(
        show.style.apply(_row_style, axis=1),
        use_container_width=True,
        hide_index=True,
    )


def neighbour_dc_panel() -> None:
    state = st.session_state.get("state")
    district = st.session_state.get("district")
    if not state:
        st.info("Pick a state in the sidebar to see your nearest data centres.", icon=":material/place:")
        return

    profile = get_district_or_state_profile(state, district)
    if not profile:
        return
    lat, lon = profile["lat"], profile["lon"]
    near = nearest_data_centres(lat, lon, top_n=3)
    if near.empty:
        st.info("No data centres in snapshot near this location.")
        return

    title = f"{district + ', ' if district else ''}{state}"
    st.markdown(f"### Data centres nearest to {title}")
    for _, d in near.iterrows():
        water_lpd = estimated_dc_water_l_per_day(d.get("it_load_mw"))
        water_str = f"~**{water_lpd/1_000_000:.2f} ML/day**" if water_lpd else "—"
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.markdown(f"**{d['name']}**  \n{d['operator']} · {d['city']}, {d['state']}")
            c2.metric("Distance", f"{d['distance_km']:.0f} km")
            c2.metric("Status", d["status"].replace("_", " "))
            c3.metric("IT load", f"{d['it_load_mw']} MW")
            c3.markdown(f"Estimated draw: {water_str}")
            if d.get("source_note"):
                st.caption(d["source_note"])

    st.caption(
        "Water-draw figures are *estimates only* — IT-load × 24 h × 1.8 L/kWh "
        "(industry rule-of-thumb, Uptime Institute). Actual consumption depends on cooling design, "
        "climate, and Water Use Effectiveness (WUE), which most Indian operators do not yet publish."
    )


def sectoral_demand_panel() -> None:
    st.markdown("### India's water demand split")
    st.caption("Annual share of total water withdrawal — NITI Aayog CWMI / Min. of Jal Shakti basin reports.")
    chart_df = SECTORAL_DEMAND.set_index("sector")
    st.bar_chart(chart_df, height=240, use_container_width=True, color="#0284c7")
    st.markdown(
        "- **Irrigation absorbs ~78%** of all water withdrawn — most efficiency gains have to come from "
        "the agricultural side (drip/sprinkler under PMKSY, crop diversification away from paddy in Punjab/Haryana).\n"
        "- Domestic use is ~6% — household conservation matters morally and locally, but is not where the "
        "national volumetric crisis is decided.\n"
        "- Industrial + power is ~13% combined — and the **fastest-growing component**, with data centres now adding "
        "a non-trivial draw in already-stressed basins (Krishna, Cauvery, Yamuna)."
    )


def district_gw_panel() -> None:
    """Show per-district stage of extraction when the user has a district selected."""
    state = st.session_state.get("state")
    district = st.session_state.get("district")
    if not state:
        return
    info = get_district_groundwater(state, district)
    if not info:
        return
    if info["level"] == "district":
        title = f"{info['district']}, {info['state']}"
        category = info["category"]
        color = info["color"]
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.markdown(f"#### {title}")
            c1.markdown(
                f"<span class='pukhuri-badge' style='background:{color}22;color:{color};"
                f"border-color:{color};'>{category}</span>",
                unsafe_allow_html=True,
            )
            c2.metric("Stage of extraction", f"{int(info['stage_of_extraction_pct'])}%")
            c3.metric("CGWB year", info["assessment_year"])
            if info.get("notes"):
                st.caption(info["notes"])
    elif district:
        st.info(
            f"No district-level CGWB stage data for {district} in our snapshot — "
            f"showing state-level for {state} below.",
            icon=":material/info:",
        )


def main() -> None:
    page_header(
        "Groundwater, reservoirs, data centres & demand",
        illustration_key="aquifer",
        caption=(
            "Three layers: CGWB groundwater stage of extraction (state-level + ~60 documented districts), "
            "major reservoirs that buffer surface supply (CWC), and India's data-centre footprint — much "
            "of which sits in the same water-stressed corridors."
        ),
    )

    state = st.session_state.get("state")

    tab_gw, tab_res_dc, tab_demand = st.tabs(
        ["Groundwater stress", "Reservoirs & Data centres", "Sectoral demand"]
    )

    with tab_gw:
        st.markdown(
            "CGWB classifies a block as **Over-Exploited** when annual extraction exceeds annual recharge "
            "(>100%), **Critical** at 90–100%, **Semi-Critical** at 70–90%, and **Safe** below 70%. "
            "Source: *Dynamic Ground Water Resources of India 2022* (CGWB, published 2023)."
        )

        district_gw_panel()

        render_map(stress_map(state), height=520)
        st.markdown("##### Ranked table — state level")
        stress_table()
        with st.expander("District-level snapshot (~60 documented districts)", icon=":material/expand_more:"):
            ddf = load_district_groundwater_stress().sort_values("stage_of_extraction_pct", ascending=False)
            show = ddf[["district", "state", "stage_of_extraction_pct", "category", "notes"]].rename(
                columns={
                    "district": "District",
                    "state": "State",
                    "stage_of_extraction_pct": "Stage of GW extraction (%)",
                    "category": "CGWB category",
                    "notes": "Notes",
                }
            )

            def _row_style(row):
                color = GW_CATEGORY_COLOR.get(row["CGWB category"], "#999999")
                return [f"background-color: {color}22"] * len(row)

            st.dataframe(
                show.style.apply(_row_style, axis=1),
                use_container_width=True,
                hide_index=True,
            )
        st.caption(
            "Source: CGWB *Dynamic Ground Water Resources of India 2022*. State averages can hide "
            "sharply-stressed districts (e.g. North Gujarat is critical even though Gujarat's average "
            "is Safe). Use as a directional indicator, not a verdict."
        )

    with tab_res_dc:
        c1, c2 = st.columns(2)
        show_res = c1.checkbox("Show reservoirs (CWC)", value=True)
        show_dc = c2.checkbox("Show data centres", value=True)
        render_map(reservoirs_dc_map(state, show_res, show_dc), height=560)

        st.divider()
        neighbour_dc_panel()

        st.divider()
        with st.expander("What's in these layers", icon=":material/info:"):
            st.markdown(
                """
- **Reservoirs.** ~40 major reservoirs from the CWC weekly bulletin universe. We list each one's
  *full-reservoir-level live storage capacity* in BCM (verified from public dam-safety records).
  We deliberately do **not** snapshot live storage % — for current week numbers go straight to
  [CWC's bulletin](https://cwc.gov.in/) (published every Thursday).
- **Data centres.** Operating + publicly-announced sites only (drawn from press releases, MeitY
  notifications, and operator websites). Coordinates are city/area-level. IT-load (MW) is what
  operators publish; water draw is computed via the industry rule-of-thumb ~1.8 L per kWh of IT
  energy. The actual range is 0.5–4 L/kWh depending on cooling. Treat as order-of-magnitude only.
- **Why this overlay matters.** Hyderabad, Chennai, Bengaluru, Mumbai, Pune, and the Delhi-NCR
  belt account for ≈90% of India's data-centre capacity — and four of those six are in
  Critical/Over-Exploited groundwater regions, or import surface water from already-stressed
  basins (Krishna, Cauvery, Yamuna).
                """.strip()
            )

    with tab_demand:
        sectoral_demand_panel()


main()
