"""
engine/geothermal.py

Geothermal H₂S Abatement Digital Twin Simulation Engine

Calculates:
  • NCG (Non-Condensable Gas) flow
  • H₂S outlet concentration after abatement
  • NCG extraction system power draw
  • Power penalty as % of plant output
  • Regulatory compliance status
  • H₂S reduction achieved (%)
"""

from constants import (
    NCG_POWER_COEFF,
    STEAM_TO_KW_COEFF,
    HOT_DAY_TEMP_THRESHOLD,
    HOT_DAY_ABATEMENT_LOSS,
    ABATEMENT_DROP_LOSS,
)


def simulate_geothermal(inputs: dict) -> dict:
    """
    Simulate a geothermal H₂S abatement system.

    Parameters
    ----------
    inputs : dict

    Expected keys:
        steam_flow_proxy, ncg_fraction, h2s_in_ppm,
        abatement_efficiency, permit_limit_ppm,
        ambient_temp, upset_event, hot_day, abatement_drop

    Returns
    -------
    dict
    """

    steam_flow          = float(inputs["steam_flow_proxy"])
    ncg_fraction        = float(inputs["ncg_fraction"])
    h2s_in_ppm          = float(inputs["h2s_in_ppm"])
    abatement_eff       = float(inputs["abatement_efficiency"])
    permit_limit_ppm    = float(inputs["permit_limit_ppm"])
    ambient_temp        = float(inputs["ambient_temp"])

    # ----------------------------------
    # Scenario modifiers
    # ----------------------------------

    if inputs.get("upset_event", False):
        steam_flow  *= 1.20
        h2s_in_ppm  = min(h2s_in_ppm * 1.40, 2000)

    if inputs.get("hot_day", False) and ambient_temp > HOT_DAY_TEMP_THRESHOLD:
        abatement_eff = max(70.0, abatement_eff - HOT_DAY_ABATEMENT_LOSS)

    if inputs.get("abatement_drop", False):
        abatement_eff = max(70.0, abatement_eff - ABATEMENT_DROP_LOSS)

    # ----------------------------------
    # NCG flow
    # ----------------------------------

    ncg_flow = steam_flow * ncg_fraction / 100

    # ----------------------------------
    # H₂S outlet concentration
    # ----------------------------------

    h2s_out_ppm = h2s_in_ppm * (1 - abatement_eff / 100)

    # ----------------------------------
    # Extraction system power
    # ----------------------------------

    extraction_power_kw = NCG_POWER_COEFF * ncg_flow

    # ----------------------------------
    # Power penalty (% of estimated plant output)
    # ----------------------------------

    plant_power_kw = steam_flow * STEAM_TO_KW_COEFF

    if plant_power_kw > 0:
        power_penalty_percent = (extraction_power_kw / plant_power_kw) * 100
    else:
        power_penalty_percent = 0.0

    power_penalty_percent = min(power_penalty_percent, 20.0)

    # ----------------------------------
    # Compliance
    # ----------------------------------

    compliance = (
        "Compliant"
        if h2s_out_ppm <= permit_limit_ppm
        else "Non-Compliant"
    )

    # ----------------------------------
    # H₂S reduction achieved
    # ----------------------------------

    if h2s_in_ppm > 0:
        h2s_reduction = ((h2s_in_ppm - h2s_out_ppm) / h2s_in_ppm) * 100
    else:
        h2s_reduction = 0.0

    # ----------------------------------
    # Output
    # ----------------------------------

    return {
        "ncg_flow":               round(ncg_flow, 2),
        "h2s_in_ppm":             round(h2s_in_ppm, 2),   # echoed for charts
        "h2s_out_ppm":            round(h2s_out_ppm, 2),
        "extraction_power_kw":    round(extraction_power_kw, 2),
        "power_penalty_percent":  round(power_penalty_percent, 2),
        "compliance":             compliance,
        "h2s_reduction":          round(h2s_reduction, 2),
    }
