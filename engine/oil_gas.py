"""
engine/oil_gas.py
Oil & Gas FGRU Digital Twin Simulation Engine
"""

from math import log

from constants import (
    COMPRESSOR_POWER_COEFF,
    CO2_FACTOR,
)


def simulate_oil_gas(inputs: dict) -> dict:

    flare_gas            = float(inputs["flare_gas_flow"])
    suction_pressure     = float(inputs["suction_pressure"])
    discharge_pressure   = float(inputs["discharge_pressure"])
    compressor_efficiency = float(inputs["compressor_efficiency"])
    fuel_demand          = float(inputs["fuel_gas_demand"])
    uptime               = float(inputs["uptime"])

    if inputs.get("upset_event", False):
        flare_gas *= 1.30

    if inputs.get("compressor_trip", False):
        uptime = 60.0

    recovered_gas = (
        min(flare_gas, fuel_demand) * uptime / 100
    )

    flared_gas = (
        max(0, flare_gas - min(flare_gas, fuel_demand)) * uptime / 100
    )

    if flare_gas > 0:
        recovery_rate = (recovered_gas / (flare_gas * uptime / 100)) * 100
    else:
        recovery_rate = 0.0

    if discharge_pressure <= suction_pressure:
        compressor_power = 0.0
    else:
        compressor_power = (
            COMPRESSOR_POWER_COEFF
            * recovered_gas
            * log(discharge_pressure / suction_pressure)
            / (compressor_efficiency / 100)
        )

    co2_avoided = recovered_gas * CO2_FACTOR

    if recovery_rate >= 80:
        status = "Excellent"
    elif recovery_rate >= 60:
        status = "Good"
    elif recovery_rate >= 40:
        status = "Warning"
    else:
        status = "Critical"

    return {
        "gas_recovered":        round(recovered_gas, 2),
        "gas_flared":           round(flared_gas, 2),
        "compressor_power_kw":  round(compressor_power, 2),
        "recovery_rate":        round(recovery_rate, 2),
        "co2_avoided":          round(co2_avoided, 2),
        "status":               status,
    }
