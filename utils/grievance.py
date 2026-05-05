"""Grievance routing + complaint drafting.

Returns the right authority for a (state, classification, issue_type) tuple, plus
a ready-to-copy complaint draft. We never auto-submit — the user copies and files
on the linked portal so accountability for the submission stays with the citizen.

Also produces a PDF version of the drafted complaint (`pdf_complaint`) so the
user can sign + scan + post, or print and walk it into a Jan Sunwai office.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import date
from textwrap import dedent

from .data_loader import load_authorities

ISSUE_TYPES = {
    "no_supply": "No water supply / interruption",
    "quality": "Water quality / contamination",
    "leakage": "Leakage / pipe burst / wastage",
    "billing": "Billing / connection / metering",
    "other": "Other",
}


@dataclass
class RoutingResult:
    primary_name: str
    primary_portal: str
    escalation_name: str
    escalation_portal: str
    grievance_portal_name: str
    grievance_portal_url: str
    rationale: str


def route(state: str, classification: str, issue_type: str) -> RoutingResult:
    auth = load_authorities()
    state_data = auth["states"].get(state)
    nat = auth["national"]

    if not state_data:
        return RoutingResult(
            primary_name="State authority not in snapshot",
            primary_portal="",
            escalation_name=nat["cpgrams"]["name"],
            escalation_portal=nat["cpgrams"]["portal"],
            grievance_portal_name=nat["cpgrams"]["name"],
            grievance_portal_url=nat["cpgrams"]["portal"],
            rationale=(
                "Your state's PHED contact is not in the snapshot. CPGRAMS routes any "
                "central or state grievance — file there and tag the relevant ministry."
            ),
        )

    is_urban = classification in ("urban", "mixed")
    primary_key = "urban" if is_urban else "rural"
    primary = state_data[primary_key]

    if issue_type == "quality":
        escalation = nat["pollution"] if "industrial" in primary.get("name", "").lower() else nat["rural_water" if not is_urban else "urban_water"]
        rationale = (
            f"For water-quality issues in a {primary_key} area of {state}, the first stop is "
            f"**{primary['name']}**. Escalate to **{escalation['name']}** if not resolved in 30 days, "
            "and to CPGRAMS if still unresolved."
        )
    elif issue_type == "no_supply":
        escalation = nat["urban_water"] if is_urban else nat["rural_water"]
        rationale = (
            f"Supply interruptions in {state} are owned by **{primary['name']}**. "
            f"Escalation: **{escalation['name']}** (Ministry of Jal Shakti / MoHUA)."
        )
    elif issue_type == "leakage":
        escalation = nat["urban_water"] if is_urban else nat["rural_water"]
        rationale = (
            f"Leakage / pipe-burst in {state}: file with **{primary['name']}** (operations & maintenance owner). "
            "Escalate via the state grievance portal if not resolved in 7 days."
        )
    elif issue_type == "billing":
        escalation = nat["urban_water"]
        rationale = (
            f"Billing / connection / metering issues are handled by the supply-owning utility — "
            f"**{primary['name']}**. State grievance portal handles any non-resolution."
        )
    else:
        escalation = nat["cpgrams"]
        rationale = (
            f"Generic water issue in {state}: start with **{primary['name']}**, then state grievance portal, "
            "then CPGRAMS as universal escalation."
        )

    grievance_portal = state_data.get("grievance", {})
    return RoutingResult(
        primary_name=primary["name"],
        primary_portal=primary.get("portal", ""),
        escalation_name=escalation["name"],
        escalation_portal=escalation.get("portal", ""),
        grievance_portal_name=grievance_portal.get("name", nat["cpgrams"]["name"]),
        grievance_portal_url=grievance_portal.get("portal", nat["cpgrams"]["portal"]),
        rationale=rationale,
    )


def draft_complaint(
    *,
    name: str,
    address: str,
    state: str,
    district: str,
    issue_type: str,
    description: str,
    contaminants: list[str] | None = None,
    duration_days: int | None = None,
    consumer_no: str | None = None,
    primary_authority: str = "",
) -> str:
    today = date.today().strftime("%d %B %Y")
    issue_label = ISSUE_TYPES.get(issue_type, issue_type)

    cont_line = ""
    if issue_type == "quality" and contaminants:
        cont_line = (
            f"\nSuspected/known contaminants in our area (per public CGWB/CPCB data and "
            f"local observation): **{', '.join(contaminants)}**.\n"
            "I request testing under BIS 10500:2012 parameters and remedial action.\n"
        )

    duration_line = ""
    if duration_days and issue_type in ("no_supply", "leakage"):
        duration_line = f"\nThe issue has persisted for **{duration_days} day(s)**.\n"

    consumer_line = f"\nConsumer / Connection No.: {consumer_no}" if consumer_no else ""

    return _compose_letter(
        name=name,
        address=address,
        state=state,
        district=district,
        issue_label=issue_label,
        description=description,
        cont_line=cont_line,
        duration_line=duration_line,
        consumer_line=consumer_line,
        primary_authority=primary_authority,
        today=today,
    )


def _compose_letter(
    *,
    name: str,
    address: str,
    state: str,
    district: str,
    issue_label: str,
    description: str,
    cont_line: str,
    duration_line: str,
    consumer_line: str,
    primary_authority: str,
    today: str,
) -> str:
    body = dedent(
        f"""\
        To,
        The Engineer-in-Charge,
        {primary_authority or '[Authority]'}
        {state}

        Date: {today}

        Subject: Complaint regarding {issue_label.lower()} — {district}, {state}

        Sir / Madam,

        I, {name}, resident of:
        {address}
        District: {district}, State: {state}{consumer_line}

        wish to formally lodge a complaint regarding the following issue under your jurisdiction:
        {duration_line}{cont_line}
        Description of the issue:
        {description.strip()}

        I request the following:
        1. Immediate inspection of the affected supply / source.
        2. Written acknowledgement of this complaint with a unique grievance ID.
        3. Time-bound resolution as per the citizen-charter / SLA of your department.
        4. In case of contamination, water-quality test results from a NABL-accredited lab to be shared.

        I reserve the right to escalate this matter under the Right to Public Services / RTI Act and
        through CPGRAMS (pgportal.gov.in) and state grievance portals if no satisfactory action is
        taken within the prescribed period.

        Yours faithfully,
        {name}
        (Contact details to be filled before submission)
        """
    )
    return body


# ---------------------------------------------------------------------------
# PDF generation


def pdf_complaint(
    *,
    body_text: str,
    primary_authority: str,
    state: str,
    district: str,
    issue_type: str,
    grievance_portal_name: str,
    grievance_portal_url: str,
) -> bytes:
    """Render the drafted complaint to a printable A4 PDF.

    Uses fpdf2's built-in Helvetica (Latin-1 only) — fine for the English template.
    Non-Latin characters are dropped with a `?` to avoid Unicode crashes; if the
    user wants Devanagari/Tamil, drop a TTF in assets/fonts/ and register it.
    """
    from fpdf import FPDF  # local import keeps cold-start fast on map-only pages

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header band
    pdf.set_fill_color(2, 132, 199)  # accent
    pdf.rect(0, 0, 210, 18, style="F")
    pdf.set_xy(10, 5)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Pukhuri  -  Drafted Water Grievance", ln=True)

    pdf.set_y(22)
    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Helvetica", "", 10)

    # Body — strip the few markdown asterisks fpdf can't render natively
    safe_body = (
        body_text.replace("**", "")
        .replace("—", "-")
        .replace("–", "-")
        .replace("’", "'")
    )
    safe_body = _latin1_safe(safe_body)
    for line in safe_body.splitlines():
        pdf.multi_cell(0, 5.2, line if line.strip() else " ")

    # Routing footer
    pdf.ln(4)
    pdf.set_draw_color(220, 220, 220)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "Where to file this complaint", ln=True)
    pdf.set_font("Helvetica", "", 9)
    for label, value in [
        ("Primary authority", primary_authority),
        ("State", state),
        ("District", district),
        ("Issue type", ISSUE_TYPES.get(issue_type, issue_type)),
        ("State grievance portal", grievance_portal_name),
        ("Portal URL", grievance_portal_url),
        ("Universal escalation", "CPGRAMS  -  https://pgportal.gov.in/"),
    ]:
        pdf.cell(45, 5, _latin1_safe(label) + ":", border=0)
        pdf.multi_cell(0, 5, _latin1_safe(str(value)))

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(
        0, 4, _latin1_safe(
            "Generated by Pukhuri (jal darpan / pukhuri.hf.space). "
            "This PDF is a draft - sign by hand before filing. Pukhuri does not auto-submit "
            "grievances; the citizen always signs and files."
        )
    )

    out = pdf.output(dest="S")
    if isinstance(out, str):
        out = out.encode("latin-1", errors="replace")
    return bytes(out)


def _latin1_safe(text: str) -> str:
    """fpdf2 Helvetica only supports Latin-1; replace anything outside that range."""
    return text.encode("latin-1", errors="replace").decode("latin-1")
