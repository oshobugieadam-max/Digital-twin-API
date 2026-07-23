"""
schemas.py

Pydantic request and response models for the
Digital Twin API.

These schemas define the contract between the
Lovable frontend and the FastAPI backend.
"""

from typing import List

from pydantic import BaseModel, Field


# ==========================================================
# REQUEST MODEL
# ==========================================================

class SimulationRequest(BaseModel):
    """
    Input parameters supplied by the frontend.
    """

    # -------------------------
    # Oil & Gas
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
    # Geothermal
    # -------------------------

    steam_flow_proxy: float = Field(
        ..., ge=1000, le=20000,
        description="Steam flow proxy (kg/h)"
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
        description="H₂S abatement efficiency (%)"
    )

    permit_limit_ppm: float = Field(
        ..., ge=5, le=200,
        description="Permit limit (ppm)"
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


# ==========================================================
# OIL & GAS RESULTS
# ==========================================================

class OilGasResults(BaseModel):

    gas_recovered: float

    gas_flared: float

    compressor_power_kw: float

    recovery_rate: float

    co2_avoided: float


# ==========================================================
# GEOTHERMAL RESULTS
# ==========================================================

class GeothermalResults(BaseModel):

    ncg_flow: float

    h2s_out_ppm: float

    extraction_power_kw: float

    power_penalty_percent: float

    compliance: str

    h2s_reduction: float


# ==========================================================
# COMPARISON RESULTS
# ==========================================================

class ComparisonResults(BaseModel):

    released_gas: float

    total_power: float

    compliance_indicator: int


# ==========================================================
# DIGITAL TWIN HEALTH SCORE
# ==========================================================

class HealthScore(BaseModel):

    score: float

    status: str


# ==========================================================
# ENGINEERING RECOMMENDATIONS
# ==========================================================

class Recommendation(BaseModel):

    priority: str

    category: str

    message: str


# ==========================================================
# CHART DATA
# ==========================================================

class ChartData(BaseModel):

    title: str

    labels: List[str]

    values: List[float]


# ==========================================================
# METADATA
# ==========================================================

class Metadata(BaseModel):

    model: str

    version: str

    simulation_type: str

    timestamp: str


# ==========================================================
# SUMMARY
# ==========================================================

class SimulationSummary(BaseModel):

    overall_status: str

    key_message: str


# ==========================================================
# COMPLETE RESPONSE
# ==========================================================

class SimulationResponse(BaseModel):

    metadata: Metadata

    summary: SimulationSummary

    oil_gas: OilGasResults

    geothermal: GeothermalResults

    comparison: ComparisonResults

    health_score: HealthScore

    recommendations: List[Recommendation]

    charts: List[ChartData]
