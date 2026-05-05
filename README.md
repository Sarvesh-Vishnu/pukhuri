---
title: Pukhuri — Know Your Water (India)
emoji: 💧
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.40.0
app_file: Home.py
python_version: "3.11"
pinned: false
license: mit
short_description: Water source, contaminants, and grievance routing for India.
---

# Pukhuri — Know Your Water

> **পুখুৰী** *(pukhuri)* — Assamese for the traditional village pond. Every Assamese home historically had one for drinking, bathing, and fish — a family-scale relationship with water that this app tries to bring back.

An interactive Streamlit app that tells a user in India:

1. **Where their water comes from** (river basin, dominant source, major rivers/reservoirs).
2. **What's in it** — known contaminants for their state/district, with BIS 10500:2012 limits, health
   effects, household and community treatment options, and the government schemes that target each.
3. **How stressed the system is** — CGWB groundwater stage of extraction by state, CWC reservoir
   inventory, and the Indian data-centre pipeline overlaid on the same map.
4. **Who to complain to** — routes a complaint to the right state PHED / urban water board / state
   grievance portal, drafts a formal letter, and links to CPGRAMS as universal escalation.
   No auto-submit by design — the citizen always signs and files.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open <http://localhost:8501>.

## Deploying to Hugging Face Spaces

This repo is HF-Spaces-ready. The YAML frontmatter at the top of this README is the Spaces config.

1. Create a new Space at <https://huggingface.co/new-space>: SDK = `streamlit`, hardware = CPU basic (free).
2. `git clone` your Space, copy the contents of `water-india/` into it, and push.
3. The Space auto-builds and serves at `https://huggingface.co/spaces/<you>/<space-name>`.

Alternatives that also work without code changes:
- **Streamlit Community Cloud** — connect your GitHub repo directly.
- **Render** (free tier) — `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`.

## Data sources & snapshot

This app uses a curated **snapshot** of public-domain Indian water data — government APIs are unreliable;
CGWB/CWC publish at known cadences anyway. Snapshot dates and per-row source notes live next to each dataset.

| Dataset | Source | File |
|---|---|---|
| State water profile | CGWB, CPCB, JJM dashboard | `data/state_water_profile.csv` |
| Districts (curated affected + major urban) | CGWB Year Books, peer-reviewed literature | `data/district_water_profile.csv` |
| Contaminants (BIS limits, treatment) | BIS IS 10500:2012, WHO GDWQ, CGWB | `data/contaminants.json` |
| Authorities & grievance portals | State PHED websites, CPGRAMS | `data/authorities.json` |
| National schemes | Min. Jal Shakti, MoHUA, NMCG | `data/schemes.json` |
| Groundwater stress (state) | CGWB *Dynamic Ground Water Resources 2022* | `data/groundwater_stress.csv` |
| Major reservoirs | CWC weekly bulletin universe, dam-safety records | `data/reservoirs.csv` |
| Data-centre pipeline | Operator press releases, MeitY notifications, state IT portals | `data/data_centres.csv` |

**Honest caveats:**
- District snapshot includes ~150 districts (well-documented contamination + major urban). Districts not
  in the snapshot fall back to state-level data with an explicit notice. Absence ≠ safety — *test your water*.
- Coordinates are approximate (district-HQ / area-level, ~2 decimal places).
- We deliberately don't fake live reservoir storage % or live water-quality readings — for those, go to
  CWC's bulletin / your state PHED directly.
- Data-centre water draws are computed from published IT load via the industry rule-of-thumb (~1.8 L/kWh).
  Real consumption depends on cooling design and climate. Treat as order-of-magnitude.
- Grievance flow drafts and links — **never auto-files**. Citizen signs and submits.

## Languages

English in v1. Hindi (`hi`), Tamil (`ta`), and Assamese (`as`) are stubbed in `utils/i18n.py` and fall
back to English when picked. To enable a language, fill the corresponding dict in `LANGS`.

## Licence

MIT — see [`LICENSE`](LICENSE).
