"""
engine/health.py

Digital Twin Health Score Calculator

Combines Oil & Gas and Geothermal results into a
single 0–100 health score with a human-readable status.
"""


def calculate_health_score(
    oil_gas_results: dict,
    geothermal_results: dict,
) -> dict:
    """
    Compute a 0–100 health score for the combined Digital Twin.

    Scoring logic
    -------------
    Oil & Gas (50 % weight):
        Based directly on recovery_rate (0–100 %).

    Geothermal (50 % weight):
        60 % from H₂S reduction achieved.
        40 % from power penalty (lower is better, cap at 20 %).
        Non-compliance applies a 40 % penalty to the geo score.

    Parameters
    ----------
    oil_gas_results    : dict — output of simulate_oil_gas()
    geothermal_results : dict — output of simulate_geothermal()

    Returns
    -------
    dict
        score  : float   (0–100)
        status : str     ("Healthy" | "Moderate" | "At Risk" | "Critical")
    """

    # ── Oil & Gas score ───────────────────────────────────
    recovery_rate = oil_gas_results.get("recovery_rate", 0)
    og_score = min(float(recovery_rate), 100.0)

    # ── Geothermal score ──────────────────────────────────
    h2s_reduction    = geothermal_results.get("h2s_reduction", 0)
    power_penalty    = geothermal_results.get("power_penalty_percent", 0)
    compliance       = geothermal_results.get("compliance", "Non-Compliant")

    reduction_score  = min(float(h2s_reduction), 100.0)
    penalty_score    = max(0.0, (20.0 - float(power_penalty)) / 20.0) * 100.0

    geo_score = reduction_score * 0.60 + penalty_score * 0.40

    if compliance == "Non-Compliant":
        geo_score *= 0.60   # significant penalty for regulatory breach

    geo_score = min(geo_score, 100.0)

    # ── Combined ──────────────────────────────────────────
    combined = round((og_score * 0.50) + (geo_score * 0.50), 1)
    combined = min(combined, 100.0)

    # ── Status label ──────────────────────────────────────
    if combined >= 80:
        status = "Healthy"
    elif combined >= 60:
        status = "Moderate"
    elif combined >= 40:
        status = "At Risk"
    else:
        status = "Critical"

    return {
        "score":  combined,
        "status": status,
    }
