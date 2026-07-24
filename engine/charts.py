"""
engine/charts.py

Chart Data Builder

Converts simulation results into chart-ready payloads
for the frontend: { title, labels, values }.
"""


def build_charts(
    oil_gas_results: dict,
    geothermal_results: dict,
    inputs: dict,
) -> list:
    """
    Build chart data for the frontend.

    Parameters
    ----------
    oil_gas_results    : dict
    geothermal_results : dict
    inputs             : dict — original simulation inputs (for permit line)

    Returns
    -------
    list of dict
        Each dict: { title, labels, values }
    """

    charts = []

    # ── 1. Gas Balance ────────────────────────────────────
    charts.append({
        "title":  "Gas Balance (kg/h)",
        "labels": ["Recovered", "Flared"],
        "values": [
            oil_gas_results.get("gas_recovered", 0),
            oil_gas_results.get("gas_flared", 0),
        ],
    })

    # ── 2. CO₂ Avoided ───────────────────────────────────
    charts.append({
        "title":  "CO₂ Avoided (kg/h)",
        "labels": ["CO₂ Avoided"],
        "values": [
            oil_gas_results.get("co2_avoided", 0),
        ],
    })

    # ── 3. H₂S Abatement ─────────────────────────────────
    charts.append({
        "title":  "H₂S Concentration (ppm)",
        "labels": ["Inlet", "Outlet", "Permit Limit"],
        "values": [
            geothermal_results.get("h2s_in_ppm", 0),   # echoed from engine
            geothermal_results.get("h2s_out_ppm", 0),
            float(inputs.get("permit_limit_ppm", 50)),
        ],
    })

    # ── 4. Power Consumption ──────────────────────────────
    charts.append({
        "title":  "Power Consumption (kW)",
        "labels": ["Compressor", "NCG Extraction"],
        "values": [
            oil_gas_results.get("compressor_power_kw", 0),
            geothermal_results.get("extraction_power_kw", 0),
        ],
    })

    # ── 5. Recovery vs Target ─────────────────────────────
    charts.append({
        "title":  "Recovery Rate (%)",
        "labels": ["Actual", "Target"],
        "values": [
            oil_gas_results.get("recovery_rate", 0),
            80.0,   # engineering target
        ],
    })

    return charts
