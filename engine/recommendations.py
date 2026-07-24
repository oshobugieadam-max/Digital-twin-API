"""
engine/recommendations.py

Engineering Recommendations Generator

Analyses simulation outputs and original inputs to produce
a prioritised list of actionable recommendations.
"""

_PRIORITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def generate_recommendations(
    oil_gas_results: dict,
    geothermal_results: dict,
    inputs: dict,
) -> list:
    """
    Generate prioritised engineering recommendations.

    Parameters
    ----------
    oil_gas_results    : dict
    geothermal_results : dict
    inputs             : dict — original simulation inputs

    Returns
    -------
    list of dict
        Each dict: { priority, category, message }
    """

    recs = []

    # ──────────────────────────────────────────────────────
    # Oil & Gas checks
    # ──────────────────────────────────────────────────────

    recovery_rate     = oil_gas_results.get("recovery_rate", 0)
    gas_flared        = oil_gas_results.get("gas_flared", 0)
    compressor_power  = oil_gas_results.get("compressor_power_kw", 0)

    if inputs.get("compressor_trip", False):
        recs.append({
            "priority": "Critical",
            "category": "Oil & Gas",
            "message": (
                "Compressor trip active — plant is operating at reduced uptime. "
                "Schedule immediate maintenance inspection before restarting."
            ),
        })

    if recovery_rate < 60:
        recs.append({
            "priority": "High",
            "category": "Oil & Gas",
            "message": (
                f"Recovery rate is {recovery_rate:.1f} % — below the 60 % threshold. "
                "Review fuel gas demand alignment and compressor availability."
            ),
        })

    if gas_flared > 500:
        recs.append({
            "priority": "High",
            "category": "Oil & Gas",
            "message": (
                f"{gas_flared:.0f} kg/h is being flared. "
                "Consider expanding FGRU capacity or rerouting excess gas to fuel."
            ),
        })

    if compressor_power > 400:
        recs.append({
            "priority": "Medium",
            "category": "Oil & Gas",
            "message": (
                f"Compressor draw is high at {compressor_power:.0f} kW. "
                "Review compression ratio — consider staging or reducing discharge pressure."
            ),
        })

    if inputs.get("upset_event", False):
        recs.append({
            "priority": "Medium",
            "category": "Oil & Gas",
            "message": (
                "Upset event in progress — flare gas flow is elevated by ~30 %. "
                "Monitor downstream equipment capacity and increase inspection frequency."
            ),
        })

    # ──────────────────────────────────────────────────────
    # Geothermal checks
    # ──────────────────────────────────────────────────────

    compliance       = geothermal_results.get("compliance", "Non-Compliant")
    h2s_out          = geothermal_results.get("h2s_out_ppm", 0)
    power_penalty    = geothermal_results.get("power_penalty_percent", 0)
    permit_limit     = float(inputs.get("permit_limit_ppm", 50))

    if compliance == "Non-Compliant":
        recs.append({
            "priority": "Critical",
            "category": "Geothermal",
            "message": (
                f"H₂S outlet ({h2s_out:.1f} ppm) exceeds permit limit "
                f"({permit_limit:.0f} ppm). Immediate corrective action required — "
                "risk of regulatory shutdown."
            ),
        })

    if inputs.get("abatement_drop", False):
        recs.append({
            "priority": "High",
            "category": "Geothermal",
            "message": (
                "Abatement efficiency has dropped significantly. "
                "Inspect scrubber packing, chemical dosing rates, and sump levels."
            ),
        })

    if power_penalty > 10:
        recs.append({
            "priority": "Medium",
            "category": "Geothermal",
            "message": (
                f"NCG extraction is imposing a {power_penalty:.1f} % power penalty. "
                "Evaluate vacuum pump sizing and consider staged NCG compression."
            ),
        })

    if inputs.get("hot_day", False):
        recs.append({
            "priority": "Low",
            "category": "Geothermal",
            "message": (
                "Hot ambient conditions are reducing abatement performance. "
                "Monitor H₂S outlet closely and consider pre-cooling NCG inlet stream."
            ),
        })

    # ──────────────────────────────────────────────────────
    # All-clear fallback
    # ──────────────────────────────────────────────────────

    if not recs:
        recs.append({
            "priority": "Low",
            "category": "General",
            "message": (
                "All systems operating within normal parameters. "
                "Continue routine monitoring and scheduled preventive maintenance."
            ),
        })

    # Sort Critical → High → Medium → Low
    recs.sort(key=lambda r: _PRIORITY_ORDER.get(r["priority"], 9))

    return recs
