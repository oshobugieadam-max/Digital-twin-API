"""
app.py

Digital Twin API — FastAPI Application

Single endpoint:  POST /simulate
Health check:     GET  /health
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    SimulationRequest,
    SimulationResponse,
    OilGasResults,
    GeothermalResults,
    ComparisonResults,
    HealthScore,
    Recommendation,
    ChartData,
    Metadata,
    SimulationSummary,
)

from engine.oil_gas        import simulate_oil_gas
from engine.geothermal     import simulate_geothermal
from engine.health         import calculate_health_score
from engine.recommendations import generate_recommendations
from engine.charts         import build_charts


# ──────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────

app = FastAPI(
    title="Digital Twin API",
    description=(
        "Oil & Gas FGRU and Geothermal H₂S Abatement "
        "Digital Twin — Hackathon Edition"
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────

@app.get("/health", tags=["Meta"])
def health_check():
    """Liveness probe."""
    return {"status": "ok"}


@app.post(
    "/simulate",
    response_model=SimulationResponse,
    tags=["Simulation"],
)
def simulate(request: SimulationRequest) -> SimulationResponse:
    """
    Run the Digital Twin simulation.

    Accepts a SimulationRequest with Oil & Gas and Geothermal
    parameters, runs both engines, and returns a complete
    SimulationResponse.
    """

    inputs = request.model_dump()

    # ── Run engines ───────────────────────────────────────
    try:
        og  = simulate_oil_gas(inputs)
        geo = simulate_geothermal(inputs)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation engine error: {exc}",
        )

    # ── Derived metrics ───────────────────────────────────
    health  = calculate_health_score(og, geo)
    recs    = generate_recommendations(og, geo, inputs)
    charts  = build_charts(og, geo, inputs)

    # ── Comparison block ──────────────────────────────────
    total_power = round(
        og["compressor_power_kw"] + geo["extraction_power_kw"],
        2,
    )

    # Very small gas mass tied to residual H₂S in NCG stream
    released_gas = round(
        og["gas_flared"]
        + geo["ncg_flow"] * geo["h2s_out_ppm"] / 1_000_000,
        4,
    )

    compliance_indicator = 1 if geo["compliance"] == "Compliant" else 0

    # ── Summary message ───────────────────────────────────
    status_map = {
        "Healthy":  ("Operational", (
            f"Plant operating well — "
            f"recovery {og['recovery_rate']:.1f} %, "
            f"H₂S outlet {geo['h2s_out_ppm']:.1f} ppm ({geo['compliance']})."
        )),
        "Moderate": ("Caution", (
            "Performance is moderate. "
            "Review recommendations to improve efficiency and compliance."
        )),
        "At Risk":  ("Alert", (
            "Elevated risk detected. "
            "Address flagged parameters before conditions worsen."
        )),
        "Critical": ("Alert", (
            "Critical issues detected. "
            "Immediate review of flagged parameters required."
        )),
    }

    overall_status, key_message = status_map.get(
        health["status"],
        ("Unknown", "Unable to determine plant status."),
    )

    # ── Assemble response ─────────────────────────────────
    return SimulationResponse(
        metadata=Metadata(
            model="digital-twin-v1.0",
            version="1.0.0",
            simulation_type="oil_gas_geothermal_combined",
            timestamp=datetime.now(timezone.utc).isoformat(),
        ),
        summary=SimulationSummary(
            overall_status=overall_status,
            key_message=key_message,
        ),
        oil_gas=OilGasResults(
            gas_recovered       = og["gas_recovered"],
            gas_flared          = og["gas_flared"],
            compressor_power_kw = og["compressor_power_kw"],
            recovery_rate       = og["recovery_rate"],
            co2_avoided         = og["co2_avoided"],
        ),
        geothermal=GeothermalResults(
            ncg_flow              = geo["ncg_flow"],
            h2s_out_ppm           = geo["h2s_out_ppm"],
            extraction_power_kw   = geo["extraction_power_kw"],
            power_penalty_percent = geo["power_penalty_percent"],
            compliance            = geo["compliance"],
            h2s_reduction         = geo["h2s_reduction"],
        ),
        comparison=ComparisonResults(
            released_gas         = released_gas,
            total_power          = total_power,
            compliance_indicator = compliance_indicator,
        ),
        health_score=HealthScore(
            score  = health["score"],
            status = health["status"],
        ),
        recommendations=[Recommendation(**r) for r in recs],
        charts=[ChartData(**c) for c in charts],
    )
