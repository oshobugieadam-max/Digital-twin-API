"""
constants.py
Engineering constants for the Digital Twin simulation engine.
"""

# ── Oil & Gas ──────────────────────────────────────────────
COMPRESSOR_POWER_COEFF = 0.5    # kW per (kg/h) per ln(P_ratio)
CO2_FACTOR             = 2.75   # kg CO₂ per kg gas recovered

# ── Geothermal ────────────────────────────────────────────
NCG_POWER_COEFF          = 0.08   # kW per kg/h NCG extracted
STEAM_TO_KW_COEFF        = 0.20   # kW per kg/h steam (proxy)
HOT_DAY_TEMP_THRESHOLD   = 30     # °C above which abatement degrades
HOT_DAY_ABATEMENT_LOSS   = 5      # percentage points lost on hot days
ABATEMENT_DROP_LOSS      = 20     # percentage points lost on abatement_drop event
