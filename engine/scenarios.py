"""
engine/scenarios.py

Preset scenario configurations for demo, testing, and frontend dropdowns.
Each scenario is a complete SimulationRequest-compatible dict.
"""

SCENARIOS: dict[str, dict] = {

    "normal_operation": {
        "flare_gas_flow":       1200,
        "suction_pressure":     1.0,
        "discharge_pressure":   6.0,
        "compressor_efficiency": 65,
        "fuel_gas_demand":      900,
        "uptime":               92,
        "steam_flow_proxy":     8000,
        "ncg_fraction":         2.5,
        "h2s_in_ppm":           500,
        "abatement_efficiency": 95,
        "permit_limit_ppm":     50,
        "ambient_temp":         25,
        "upset_event":          False,
        "compressor_trip":      False,
        "hot_day":              False,
        "abatement_drop":       False,
    },

    "compressor_trip": {
        "flare_gas_flow":       1200,
        "suction_pressure":     1.0,
        "discharge_pressure":   6.0,
        "compressor_efficiency": 65,
        "fuel_gas_demand":      900,
        "uptime":               92,
        "steam_flow_proxy":     8000,
        "ncg_fraction":         2.5,
        "h2s_in_ppm":           500,
        "abatement_efficiency": 95,
        "permit_limit_ppm":     50,
        "ambient_temp":         25,
        "upset_event":          False,
        "compressor_trip":      True,
        "hot_day":              False,
        "abatement_drop":       False,
    },

    "hot_day_abatement_stress": {
        "flare_gas_flow":       1500,
        "suction_pressure":     1.0,
        "discharge_pressure":   7.0,
        "compressor_efficiency": 60,
        "fuel_gas_demand":      1000,
        "uptime":               88,
        "steam_flow_proxy":     10000,
        "ncg_fraction":         4.0,
        "h2s_in_ppm":           800,
        "abatement_efficiency": 90,
        "permit_limit_ppm":     50,
        "ambient_temp":         36,
        "upset_event":          False,
        "compressor_trip":      False,
        "hot_day":              True,
        "abatement_drop":       True,
    },

    "full_upset": {
        "flare_gas_flow":       2000,
        "suction_pressure":     1.0,
        "discharge_pressure":   8.0,
        "compressor_efficiency": 55,
        "fuel_gas_demand":      1200,
        "uptime":               70,
        "steam_flow_proxy":     12000,
        "ncg_fraction":         6.0,
        "h2s_in_ppm":           1000,
        "abatement_efficiency": 85,
        "permit_limit_ppm":     50,
        "ambient_temp":         38,
        "upset_event":          True,
        "compressor_trip":      True,
        "hot_day":              True,
        "abatement_drop":       True,
    },
}


def get_scenario(name: str) -> dict:
    """
    Return a scenario dict by name.

    Raises
    ------
    KeyError if scenario name is not found.
    """
    if name not in SCENARIOS:
        available = list(SCENARIOS.keys())
        raise KeyError(
            f"Scenario '{name}' not found. Available: {available}"
        )
    return SCENARIOS[name].copy()


def list_scenarios() -> list[str]:
    """Return all available scenario names."""
    return list(SCENARIOS.keys())
