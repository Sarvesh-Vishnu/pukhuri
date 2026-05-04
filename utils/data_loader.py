"""Cached loaders for the snapshot data files in /data."""
from __future__ import annotations

import json
from math import asin, cos, radians, sin, sqrt
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# CGWB groundwater categorisation thresholds (Stage of Extraction %)
GW_CATEGORY_COLOR = {
    "Safe": "#2ca02c",
    "Semi-Critical": "#ff7f0e",
    "Critical": "#d62728",
    "Over-Exploited": "#7e1f86",
}

# Industry rule-of-thumb water-use factor: hyperscale air-cooled DCs typically
# consume ~1.8 L per kWh of IT energy (Uptime Institute / Lawrence Berkeley NL).
# IT load (MW) × 24 h × 1.8 L/kWh = litres/day.
DC_WATER_L_PER_KWH = 1.8


@st.cache_data(show_spinner=False)
def load_states() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "state_water_profile.csv")
    for col in ("primary_contaminants", "major_basins", "major_rivers"):
        df[col] = df[col].fillna("").apply(_split_semis)
    return df


@st.cache_data(show_spinner=False)
def load_districts() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "district_water_profile.csv")
    df["primary_contaminants"] = df["primary_contaminants"].fillna("").apply(_split_semis)
    return df


@st.cache_data(show_spinner=False)
def load_contaminants() -> dict:
    return _load_json("contaminants.json")


@st.cache_data(show_spinner=False)
def load_authorities() -> dict:
    return _load_json("authorities.json")


@st.cache_data(show_spinner=False)
def load_schemes() -> dict:
    return _load_json("schemes.json")


@st.cache_data(show_spinner=False)
def load_groundwater_stress() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "groundwater_stress.csv")
    df["color"] = df["category"].map(GW_CATEGORY_COLOR).fillna("#999999")
    return df


@st.cache_data(show_spinner=False)
def load_reservoirs() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "reservoirs.csv")
    df["purpose"] = df["purpose"].fillna("").apply(_split_semis)
    return df


@st.cache_data(show_spinner=False)
def load_data_centres() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "data_centres.csv")
    return df


def estimated_dc_water_l_per_day(it_load_mw: float) -> float:
    """Industry rule-of-thumb: ~1.8 L water per kWh of IT energy for air-cooled DCs."""
    if pd.isna(it_load_mw):
        return 0.0
    return float(it_load_mw) * 1000.0 * 24.0 * DC_WATER_L_PER_KWH


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def nearest_data_centres(lat: float, lon: float, top_n: int = 3) -> pd.DataFrame:
    df = load_data_centres().copy()
    df["distance_km"] = df.apply(lambda r: haversine_km(lat, lon, r["lat"], r["lon"]), axis=1)
    return df.sort_values("distance_km").head(top_n).reset_index(drop=True)


def _load_json(name: str) -> dict:
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def _split_semis(value: str) -> list[str]:
    return [v.strip() for v in str(value).split(";") if v.strip()]


def get_district_or_state_profile(state: str, district: str | None) -> dict:
    """Return a unified profile dict, falling back to state-level if district not in dataset."""
    states = load_states()
    state_row = states[states["state"] == state]
    if state_row.empty:
        return {}
    s = state_row.iloc[0].to_dict()

    profile = {
        "level": "state",
        "state": state,
        "district": None,
        "lat": s["lat"],
        "lon": s["lon"],
        "dominant_source": s["dominant_source"],
        "primary_contaminants": s["primary_contaminants"],
        "major_basins": s["major_basins"],
        "major_rivers": s["major_rivers"],
        "jjm_coverage_pct": s.get("jjm_coverage_pct"),
        "notes": s.get("notes", ""),
        "classification": "mixed",
    }

    if district:
        districts = load_districts()
        d_row = districts[(districts["state"] == state) & (districts["district"] == district)]
        if not d_row.empty:
            d = d_row.iloc[0].to_dict()
            profile.update(
                level="district",
                district=district,
                lat=d["lat"],
                lon=d["lon"],
                dominant_source=d["dominant_source"],
                primary_contaminants=d["primary_contaminants"],
                classification=d["classification"],
                notes=d.get("notes", ""),
            )
    return profile
