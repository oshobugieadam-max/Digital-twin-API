"""
Pydantic schemas for the Digital Twin API.

These models define the request and response structure exchanged
between the frontend (Lovable) and the FastAPI backend.
"""

from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    """
    Input parameters supplied by the frontend.
    """

    # -------------------------
    # Oil & Gas Inputs
    # -------------------------

    flare_gas_flow: float = Field(
        ..., ge=100, le=5000,
        description="Flare gas flow (kg/h)"
    )

    suction_pressure: float = Field(
        ..., ge=0.8, le=2.0,
        description="Compressor suction pressure (bar)"
    )

    discharge_pressure: float = Field(
        ..., ge=2.0, le=10.0,
        description="Compressor discharge pressure (bar)"
    )

    compressor_efficiency: float = Field(
        ..., ge=40, le=80,
        description="Compressor efficiency (%)"
    )

    fuel_gas_demand: float = Field(
        ..., ge=0, le=5000,
        description="Fuel gas demand (kg/h)"
    )

    uptime: float = Field(
        ..., ge=50, le=100,
        description="Plant uptime (%)"
    )

    # -------------------------
    # Geothermal Inputs
    # -------------------------

    steam_flow_proxy: float = Field(
        ..., ge=1000, le=20000,
        description="Steam production proxy (kg/h)"
    )

    ncg_fraction: float = Field(
        ..., ge=0.1, le=10,
        description="NCG fraction (%)"
    )

    h2s_in_ppm: float = Field(
        ..., ge=0, le=2000,
        description="Incoming H₂S concentration (ppm)"
    )

    abatement_efficiency: float = Field(
        ..., ge=70, le=99.9,
        description="H₂S removal efficiency (%)"
    )

    permit_limit_ppm: float = Field(
        ..., ge=5, le=200,
        description="Environmental permit limit (ppm)"
    )

    ambient_temp: float = Field(
        ..., ge=15, le=40,
        description="Ambient temperature (°C)"
    )

    # -------------------------
    # Scenario Toggles
    # -------------------------

    upset_event: bool = False

    compressor_trip: bool = False

    hot_day: bool = False

    abatement_drop: bool = False
