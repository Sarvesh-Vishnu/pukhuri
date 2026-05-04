"""Map & Source — district markers + selected-district profile."""
from __future__ import annotations

import folium
from folium.plugins import MarkerCluster

import streamlit as st

from utils.data_loader import (
    get_district_or_state_profile,
    load_contaminants,
    load_districts,
    load_states,
)
from utils.i18n import t
from utils.theme import init_page, render_map

init_page(title="Map & Source", icon="🗺️")

CONTAMINANT_COLORS = {
    "arsenic": "#7e1f86",
    "fluoride": "#d62728",
    "nitrate": "#ff7f0e",
    "uranium": "#8c564b",
    "salinity": "#1f77b4",
    "iron": "#bcbd22",
    "microbial": "#2ca02c",
    "default": "#6c757d",
}


def primary_marker_color(contaminants: list[str]) -> str:
    priority = ["arsenic", "uranium", "fluoride", "nitrate", "salinity", "iron", "microbial"]
    for c in priority:
        if c in contaminants:
            return CONTAMINANT_COLORS[c]
    return CONTAMINANT_COLORS["default"]


def build_map(districts_df, focus_state: str | None, focus_district: str | None) -> folium.Map:
    if focus_state and focus_district:
        row = districts_df[(districts_df.state == focus_state) & (districts_df.district == focus_district)]
        center = (row.iloc[0]["lat"], row.iloc[0]["lon"]) if not row.empty else (22.0, 80.0)
        zoom = 8
    elif focus_state:
        sub = districts_df[districts_df.state == focus_state]
        if not sub.empty:
            center = (sub["lat"].mean(), sub["lon"].mean())
            zoom = 6
        else:
            center, zoom = (22.0, 80.0), 5
    else:
        center, zoom = (22.0, 80.0), 5

    m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron", control_scale=True)
    cluster = MarkerCluster(name="Districts", show=True).add_to(m)

    for _, r in districts_df.iterrows():
        color = primary_marker_color(r["primary_contaminants"])
        contaminants_str = ", ".join(r["primary_contaminants"]) or "no major issues in snapshot"
        popup_html = f"""
        <div style='font-family:sans-serif;font-size:13px;width:240px'>
            <b>{r['district']}, {r['state']}</b><br>
            <i>{r['classification'].title()} · {r['dominant_source'].replace('_',' ').title()}</i><br>
            <b>Contaminants:</b> {contaminants_str}<br>
            <span style='color:#555'>{r.get('notes', '')}</span>
        </div>
        """
        folium.CircleMarker(
            location=(r["lat"], r["lon"]),
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=1,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{r['district']} — {contaminants_str}",
        ).add_to(cluster)

    if focus_state and focus_district:
        row = districts_df[(districts_df.state == focus_state) & (districts_df.district == focus_district)]
        if not row.empty:
            r = row.iloc[0]
            folium.Marker(
                location=(r["lat"], r["lon"]),
                tooltip=f"📍 {r['district']}",
                icon=folium.Icon(color="darkblue", icon="info-sign"),
            ).add_to(m)

    legend_html = """
    <div style="position:fixed;bottom:20px;left:20px;z-index:9999;background:rgba(255,255,255,0.92);
                padding:10px 14px;border-radius:8px;border:1px solid #ccc;font-size:12px;font-family:sans-serif">
      <b>Marker colour = primary contaminant</b><br>
      <span style="color:#7e1f86">●</span> Arsenic
      &nbsp;<span style="color:#8c564b">●</span> Uranium
      &nbsp;<span style="color:#d62728">●</span> Fluoride<br>
      <span style="color:#ff7f0e">●</span> Nitrate
      &nbsp;<span style="color:#1f77b4">●</span> Salinity
      &nbsp;<span style="color:#bcbd22">●</span> Iron
      &nbsp;<span style="color:#2ca02c">●</span> Microbial
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    return m


def render_profile(state: str, district: str | None) -> None:
    profile = get_district_or_state_profile(state, district)
    if not profile:
        st.info("Pick a state from the sidebar to see its profile.")
        return

    contaminants = load_contaminants()
    lang = st.session_state.get("lang", "en")
    title = f"{profile['district']}, {profile['state']}" if profile["district"] else profile["state"]
    st.markdown(f"### {title}")

    if profile["level"] == "state" and district:
        st.caption(t("no_district_data", lang))

    col_a, col_b, col_c = st.columns(3)
    col_a.metric(t("source_label", lang), profile["dominant_source"].replace("_", " ").title())
    col_b.metric(t("contaminants_label", lang), ", ".join(profile["primary_contaminants"]) or "—")
    if profile.get("jjm_coverage_pct") is not None:
        col_c.metric(t("jjm_coverage", lang), f"{profile['jjm_coverage_pct']}%")

    if profile.get("major_basins"):
        st.markdown(f"**{t('basin_label', lang)}** · {', '.join(profile['major_basins'])}")
    if profile.get("major_rivers"):
        st.markdown(f"**{t('rivers_label', lang)}** · {', '.join(profile['major_rivers'])}")
    if profile.get("notes"):
        st.markdown(f"> {profile['notes']}")

    if profile["primary_contaminants"]:
        st.markdown("##### What each contaminant means here")
        for c in profile["primary_contaminants"]:
            info = contaminants.get(c)
            if not info:
                continue
            with st.expander(f"{info['name']}  ·  {info['symbol']}"):
                st.markdown(f"**{t('bis_limits', lang)}**")
                st.markdown(
                    f"- Acceptable: **{info['bis_acceptable_mg_l']} mg/L**  "
                    f"· Permissible: **{info['bis_permissible_mg_l']} mg/L**"
                )
                st.markdown(f"**Origin** · {info['natural_origin']}")
                st.markdown(f"**{t('health_effects', lang)}**")
                for h in info["health_effects"]:
                    st.markdown(f"- {h}")
                st.page_link(
                    "pages/2_Contaminants_and_Restoration.py",
                    label=f"See treatment & restoration options for {info['name']}",
                )


def main() -> None:
    st.markdown("# Map & Source")
    st.caption(
        "Markers cluster by zoom. Click a district to see its primary contaminants. "
        "Pick a state and district from the sidebar for the detailed profile below."
    )

    districts_df = load_districts()
    load_states()  # warms the cache

    state = st.session_state.get("state")
    district = st.session_state.get("district")

    fmap = build_map(districts_df, state, district)
    render_map(fmap, height=560)

    st.divider()
    if state:
        render_profile(state, district)
    else:
        st.info("Pick a state in the sidebar to see its water profile here.")


main()
