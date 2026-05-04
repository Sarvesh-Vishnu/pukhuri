"""Grievance Drafter — routes a complaint to the right authority and drafts the letter."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from utils.data_loader import (
    get_district_or_state_profile,
    load_authorities,
    load_districts,
    load_states,
)
from utils.grievance import ISSUE_TYPES, draft_complaint, route
from utils.i18n import t

st.set_page_config(page_title="Grievance Drafter — Pukhuri", page_icon="✍️", layout="wide")


def copy_button(text: str) -> None:
    safe = text.replace("`", "\\`").replace("\\", "\\\\")
    components.html(
        f"""
        <button id="copybtn"
            style="padding:8px 14px;border-radius:6px;border:1px solid #0a6cb1;
                   background:#0a6cb1;color:white;cursor:pointer;font-size:14px">
          📋 Copy complaint to clipboard
        </button>
        <span id="copystatus" style="margin-left:10px;color:#2ca02c;font-family:sans-serif"></span>
        <script>
          const btn = document.getElementById('copybtn');
          btn.addEventListener('click', async () => {{
            try {{
              await navigator.clipboard.writeText(`{safe}`);
              document.getElementById('copystatus').innerText = '✓ Copied. Now paste it on the portal below.';
            }} catch (e) {{
              document.getElementById('copystatus').innerText = '✗ Could not copy — select and copy manually.';
            }}
          }});
        </script>
        """,
        height=50,
    )


def main() -> None:
    lang = st.session_state.get("lang", "en")
    st.title(f"✍️ {t('nav_grievance', lang)}")
    st.markdown(
        "Tell us where you live, what the issue is, and a brief description. "
        "We route to the right department for your state, draft a formal letter, and link "
        "to the portal you should file it on. **We do not auto-submit** — the citizen always signs and files."
    )

    states_df = load_states()
    districts_df = load_districts()
    auth = load_authorities()

    with st.form("grievance_form"):
        c1, c2 = st.columns(2)
        with c1:
            state = st.selectbox(
                t("select_state", lang),
                sorted(states_df["state"].unique().tolist()),
                index=sorted(states_df["state"].unique().tolist()).index(st.session_state["state"])
                if st.session_state.get("state") in states_df["state"].unique()
                else 0,
            )
            d_opts = ["(not in list / use state-level)"] + sorted(
                districts_df[districts_df["state"] == state]["district"].tolist()
            )
            cur_d = st.session_state.get("district")
            d_idx = d_opts.index(cur_d) if cur_d in d_opts else 0
            district_choice = st.selectbox(t("select_district", lang), d_opts, index=d_idx)
            district = None if district_choice.startswith("(") else district_choice

            classification_default = "urban"
            if district:
                row = districts_df[(districts_df.state == state) & (districts_df.district == district)]
                if not row.empty:
                    classification_default = row.iloc[0]["classification"]
            classification = st.radio(
                "Area type",
                options=["urban", "rural", "mixed"],
                index=["urban", "rural", "mixed"].index(classification_default),
                horizontal=True,
            )

            issue_key = st.selectbox(
                t("issue_type", lang),
                options=list(ISSUE_TYPES.keys()),
                format_func=lambda k: ISSUE_TYPES[k],
            )
        with c2:
            name = st.text_input("Your name *", placeholder="As you'd sign on a letter")
            address = st.text_area(
                "Your address *",
                placeholder="House no, street, locality, PIN",
                height=90,
            )
            consumer_no = st.text_input(
                "Connection / Consumer / Tap-ID No. (optional)",
                placeholder="If you have a piped supply, your bill / FHTC ID helps",
            )
            duration = None
            if issue_key in ("no_supply", "leakage"):
                duration = st.number_input("Days the issue has persisted", min_value=0, max_value=365, value=3)

        description = st.text_area(
            "Describe the issue in 3-5 sentences *",
            placeholder=(
                "Be specific: when it started, what's visible (colour / smell / taste), what tests "
                "have been done, who you've already contacted."
            ),
            height=140,
        )

        contaminants = []
        if issue_key == "quality":
            profile = get_district_or_state_profile(state, district)
            default_cont = profile.get("primary_contaminants", [])
            contaminants = st.multiselect(
                "Suspected contaminants (pre-filled from CGWB snapshot for your area)",
                options=["fluoride", "arsenic", "nitrate", "iron", "salinity", "uranium", "microbial"],
                default=default_cont,
            )

        submitted = st.form_submit_button("Route & draft my complaint", type="primary")

    if not submitted:
        st.info("Fill in the form above and click **Route & draft my complaint**.")
        return

    if not (name and address and description):
        st.error("Please fill in name, address, and description before drafting.")
        return

    routing = route(state, classification, issue_key)
    st.success("✅ Routed. Here's where this complaint should go:")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 1️⃣ File with (primary)")
        st.markdown(f"**{routing.primary_name}**")
        if routing.primary_portal:
            st.markdown(f"[Open portal →]({routing.primary_portal})")
    with col_b:
        st.markdown("#### 2️⃣ Escalation if unresolved")
        st.markdown(f"**{routing.escalation_name}**")
        if routing.escalation_portal:
            st.markdown(f"[Open portal →]({routing.escalation_portal})")

    st.markdown(f"#### 3️⃣ State grievance portal")
    st.markdown(f"**{routing.grievance_portal_name}** — [Open →]({routing.grievance_portal_url})")
    st.markdown(
        f"#### 4️⃣ Universal escalation: CPGRAMS — "
        f"[{auth['national']['cpgrams']['portal']}]({auth['national']['cpgrams']['portal']})"
    )

    st.info(routing.rationale)

    st.markdown("---")
    st.markdown("### 📝 Drafted complaint")
    body = draft_complaint(
        name=name,
        address=address,
        state=state,
        district=district or "—",
        issue_type=issue_key,
        description=description,
        contaminants=contaminants,
        duration_days=duration,
        consumer_no=consumer_no or None,
        primary_authority=routing.primary_name,
    )

    st.text_area("Complaint (editable before copying)", value=body, height=460, key="draft_text")
    copy_button(body)

    st.caption(
        "After filing, save the grievance ID issued by the portal. If unresolved within the SLA "
        "(typically 30 days for state portals, 60 days for CPGRAMS), escalate up the chain."
    )


main()
